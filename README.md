# echo360-transcripts

A focused command-line interface for downloading all available transcripts in an Echo360 Cloud course. It uses the course discovery, SSO/browser authentication, and transcript parsing implemented by [soraxas/echo360](https://github.com/soraxas/echo360), including the transcript-download changes merged in PR #104.

The command downloads transcript text files (`.txt`) and WebVTT captions (`.vtt`) when available. It does not download lecture videos.

## Requirements

- Python 3.9 or newer
- Google Chrome and a compatible ChromeDriver (or Firefox and geckodriver with `--firefox`)
- An account with access to the course

## Install

```sh
python -m pip install git+https://github.com/rufus-gh/echo360-transcripts.git
```

The install pulls the current `master` branch of the upstream Echo360 downloader for its authentication and download implementation.

## Use

```sh
echo360-transcripts 'https://echo360.org.uk/section/<course-id>' --output ./transcripts
```

A browser window opens for institutional sign-in when needed. After login, the downloader continues automatically. You can reuse the login profile on later runs:

```sh
echo360-transcripts '<course-url-or-uuid>' --output ./transcripts --persistent-session
```

Filter lectures by date:

```sh
echo360-transcripts '<course-url>' --after-date 2025-01-01 --before-date 2025-06-30
```

Use `echo360-transcripts --help` for all options. `--stealth` is available for institutions whose SSO flow blocks ordinary automated Chrome; it requires the upstream tool's optional `undetected-chromedriver` dependency.

## Notes

- Transcript download is supported by Echo360 Cloud courses when a transcript is available.
- The course UUID can be passed instead of a URL for the upstream tool's default Echo360 host. For other hosts, pass the full course URL.
- This project is a small CLI wrapper. Authentication, course lookup, transcript conversion, and `.txt`/`.vtt` output are provided by [soraxas/echo360](https://github.com/soraxas/echo360).

## License

MIT. The upstream Echo360 project is separately licensed; see its repository for its license and notices.
