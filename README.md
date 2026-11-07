# echo360-transcripts

A focused command-line interface for downloading captions and transcripts from an Echo360 Cloud course. It uses the course discovery, SSO/browser authentication, and transcript parsing implemented by [soraxas/echo360](https://github.com/soraxas/echo360), including the transcript-download changes merged in PR #104.

By default, the command saves WebVTT caption files (`.vtt`) only. Use `--txt` to also save plain-text transcripts or `--txt-only` to save just `.txt` files. The optional `--zip` flag bundles the selected files from the current download into one ZIP archive.

## Requirements

- Python 3.9 or newer
- Google Chrome (or Firefox and geckodriver with `--firefox`)
- An account with access to the course

## Quick install

Clone this repo, then run the installer. It checks the Python version, creates an isolated `.venv`, and installs the CLI and its dependencies, including the upstream Echo360 downloader.

```sh
git clone https://github.com/rufus-gh/echo360-transcripts.git
cd echo360-transcripts
./install.sh
```

The installer reports an error with a Python download link if Python 3.9 or newer is not available.

## Use

```sh
.venv/bin/echo360-transcripts 'https://echo360.org.uk/section/<course-id>' --output ./transcripts
```

Add text transcripts as well as VTT captions:

```sh
.venv/bin/echo360-transcripts '<course-url-or-uuid>' --txt
```

Save text only:

```sh
.venv/bin/echo360-transcripts '<course-url-or-uuid>' --txt-only
```

Create a ZIP alongside the downloaded files:

```sh
.venv/bin/echo360-transcripts '<course-url-or-uuid>' --output ./transcripts --zip
```

Choose a ZIP path with `--zip ./course-captions.zip`. A browser window opens for institutional sign-in when needed; after login, the downloader continues automatically. Reuse the login profile on later runs with `--persistent-session`.

Filter lectures by date:

```sh
.venv/bin/echo360-transcripts '<course-url>' --after-date 2025-01-01 --before-date 2025-06-30
```

Use `.venv/bin/echo360-transcripts --help` for all options. `--stealth` is available for institutions whose SSO flow blocks ordinary automated Chrome; it requires the upstream tool's optional `undetected-chromedriver` dependency.

## Notes

- Caption download is supported by Echo360 Cloud courses when VTT captions are available.
- The course UUID can be passed instead of a URL for the upstream tool's default Echo360 host. For other hosts, pass the full course URL.
- Authentication, course lookup, and caption/transcript extraction are provided by [soraxas/echo360](https://github.com/soraxas/echo360).

## License

MIT. The upstream Echo360 project is separately licensed; see its repository for its license and notices.
