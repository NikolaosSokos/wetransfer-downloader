import argparse
from wetransfer_downloader.downloader import WeTransferDownloader

def main():
    parser = argparse.ArgumentParser(description="Download a file from a WeTransfer link")
    parser.add_argument("url", help="The WeTransfer URL to download from")
    args = parser.parse_args()

    downloader = WeTransferDownloader(headless=True)
    result = downloader.download(args.url)
    print(f"Saved to: {result}")
