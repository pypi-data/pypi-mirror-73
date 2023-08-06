from .api import Api
import argparse
import os


parser = argparse.ArgumentParser("Download today's NHK easy news")
parser.add_argument(
    "-m",
    "--mp3",
    help="Download mp3 audio instead of m3u8 playlist (ffmpeg required)",
    action="store_true",
)
parser.add_argument("-d", "--directory", help="directory")
parser.add_argument(
    "-F", "--no-furigana", action="store_false", help="disable furigana",
)
parser.add_argument(
    "-H", "--html", action="store_true", help="HTML output (default is txt)"
)
args = parser.parse_args()


def main():
    if args.directory:
        os.chdir(args.directory)
    api = Api()
    api.download_top_news(args.no_furigana, args.html, args.mp3)


if __name__ == "__main__":
    main()
