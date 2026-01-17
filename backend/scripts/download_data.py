"""
Sovereign Data Downloader Module.

This module is responsible for securely acquiring SEC 10-K filings
without relying on external API keys (beyond the SEC's public access).
It uses the `sec-edgar-downloader` library to fetch filings for specific tickers.
"""

import os
import sys
from sec_edgar_downloader import Downloader


class SECFilingFetcher:
    """
    A specialized fetcher for SEC filings designed for local ingestion.
    """

    def __init__(self, download_dir: str = "data/sec_edgar_filings", email: str = "user@example.com"):
        """
        Initialize the fetcher.

        Args:
            download_dir (str): The local directory to store downloaded filings.
            email (str): User agent email required by SEC EDGAR.
        """
        self.download_dir = download_dir
        self.email = email
        self._ensure_directory()

    def _ensure_directory(self):
        """Creates the download directory if it does not exist."""
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            print(f"[INFO] Created data directory: {self.download_dir}")

    def fetch_10k(self, ticker: str, amount: int = 1):
        """
        Downloads the latest 10-K filings for a given ticker.

        Args:
            ticker (str): The stock ticker symbol (e.g., "NVDA").
            amount (int): Number of recent filings to download.
        """
        print(f"[INFO] Initializing download for {ticker} (10-K)...")
        
        dl = Downloader("MyCompany", self.email, self.download_dir)
        
        try:
            count = dl.get("10-K", ticker, limit=amount)
            print(f"[SUCCESS] Downloaded {count} 10-K filing(s) for {ticker} to {self.download_dir}")
        except Exception as e:
            print(f"[ERROR] Failed to download filings for {ticker}: {e}")
            sys.exit(1)


def main():
    """
    Main execution entry point.
    """
    # Configuration
    # Ideally, email should be from env vars or config, but hardcoded for this prototype
    # as per "Sovereign" specs (no external dependencies if possible).
    # Using a placeholder valid email format is required by SEC.
    USER_EMAIL = "sovereign_rag@localhost.com" 
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

    fetcher = SECFilingFetcher(download_dir=DATA_DIR, email=USER_EMAIL)

    # Targets defined in specs
    targets = ["NVDA", "MSFT"]

    for ticker in targets:
        fetcher.fetch_10k(ticker, amount=1)

if __name__ == "__main__":
    main()
