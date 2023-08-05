import webbrowser
import argparse
import urllib.request
from urllib.error import HTTPError

parser = argparse.ArgumentParser()
parser.add_argument(
    "service", help="AWS service you want to get the developer guide for"
)
args = parser.parse_args()


def check_code(url):
    try:
        urllib.request.urlopen(url).getcode()
    except HTTPError:
        return False
    else:
        return True


def main():
    url = f"https://docs.aws.amazon.com/{args.service}/index.html"
    if check_code(url):
        webbrowser.open(url, new=1)  # new window
    else:
        print(f"No developer guide for {args.service}")


if __name__ == "__main__":
    main()
