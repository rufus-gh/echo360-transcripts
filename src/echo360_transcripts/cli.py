"""CLI focused on downloading Echo360 Cloud course transcripts."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="echo360-transcripts",
        description="Download every available transcript in an Echo360 Cloud course.",
    )
    parser.add_argument("course", help="Echo360 Cloud course URL or course UUID")
    parser.add_argument(
        "-o", "--output", default=".", metavar="DIR",
        help="directory for transcript .txt and .vtt files (default: current directory)",
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
    args = build_parser().parse_args(argv)
    if args.firefox and args.stealth:
        build_parser().error("--firefox and --stealth cannot be used together")

    os.makedirs(args.output, exist_ok=True)

    # Reuse the upstream project's authentication, course discovery and
    # transcript/VTT handling. Force transcript-only Cloud mode so no videos
    # or video feeds are downloaded.
    upstream_args = [
        args.course,
        "--output", args.output,
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
