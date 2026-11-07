"""CLI focused on downloading Echo360 Cloud course transcripts."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="echo360-transcripts",
        description="Download every available caption or transcript in an Echo360 Cloud course.",
    )
    parser.add_argument("course", help="Echo360 Cloud course URL or course UUID")
    parser.add_argument(
        "-o", "--output", default=".", metavar="DIR",
        help="directory for downloaded files (default: current directory)",
    )
    formats = parser.add_mutually_exclusive_group()
    formats.add_argument(
        "--txt", action="store_true",
        help="save text transcripts as well as the default VTT captions",
    )
    formats.add_argument(
        "--txt-only", action="store_true",
        help="save only plain-text transcripts (.txt), without VTT captions",
    )
    parser.add_argument(
        "--zip", nargs="?", const="transcripts.zip", metavar="PATH",
        help="also bundle selected files into a ZIP (default: OUTPUT/transcripts.zip)",
    )
    parser.add_argument("--after-date", metavar="YYYY-MM-DD", help="include lectures from this date onward")
    parser.add_argument("--before-date", metavar="YYYY-MM-DD", help="include lectures through this date")
    parser.add_argument("--firefox", action="store_true", help="use Firefox/geckodriver instead of Chrome")
    parser.add_argument("--stealth", action="store_true", help="use undetected Chrome for SSO flows that need it")
    parser.add_argument(
        "--persistent-session", action="store_true",
        help="reuse Echo360 login state in a local browser profile",
    )
    parser.add_argument("--debug", action="store_true", help="enable detailed downloader logging")
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.firefox and args.stealth:
        parser.error("--firefox and --stealth cannot be used together")

    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    save_vtt = not args.txt_only
    save_txt = args.txt or args.txt_only
    selected_files: list[tuple[Path, Path]] = []

    # Reuse upstream authentication and downloads, then expose only formats
    # selected here. A temporary destination avoids removing or overwriting
    # unrelated files in the user's output directory.
    with tempfile.TemporaryDirectory(prefix="echo360-transcripts-") as staging:
        upstream_args = [
            args.course,
            "--output", staging,
            "--echo360cloud",
            "--transcripts-only",
            "--auto",
        ]
        upstream_args.append("--firefox" if args.firefox else "--stealth" if args.stealth else "--chrome")
        if args.persistent_session:
            upstream_args.append("--persistent-session")
        if args.debug:
            upstream_args.append("--debug")
        if args.after_date:
            upstream_args.extend(["--after-date", args.after_date])
        if args.before_date:
            upstream_args.extend(["--before-date", args.before_date])

        from echo360.main import main as echo360_main

        original_argv = sys.argv
        try:
            sys.argv = ["echo360-transcripts", *upstream_args]
            echo360_main()
        finally:
            sys.argv = original_argv

        staging_path = Path(staging)
        for path in staging_path.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".txt", ".vtt"}:
                continue
            if path.suffix.lower() == ".vtt" and not save_vtt:
                continue
            if path.suffix.lower() == ".txt" and not save_txt:
                continue
            relative = path.relative_to(staging_path)
            destination = output_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            selected_files.append((destination, relative))

    if args.zip is not None:
        archive_path = Path(args.zip).expanduser()
        if not archive_path.is_absolute():
            archive_path = output_dir / archive_path
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for source, relative in selected_files:
                archive.write(source, arcname=relative.as_posix())
        print("Created ZIP: {} ({} files)".format(archive_path, len(selected_files)))
    print("Saved {} selected transcript/caption files to {}".format(len(selected_files), output_dir))
