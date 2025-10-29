import logging
import time
from iqoptionapi.stable_api import IQ_Option
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

class IQConnector:
    """
    Handles the connection and data fetching from the IQ Option API.
    """
    def __init__(self):
        self.api = None

    def connect(self):
        """
        Connects and logs in to the IQ Option account.
        """
        logging.info("Connecting to IQ Option...")
        self.api = IQ_Option(config.IQ_OPTION_USERNAME, config.IQ_OPTION_PASSWORD)
        check, reason = self.api.connect()

        if check:
            logging.info("Successfully connected to IQ Option.")
            self.api.change_balance(config.ACCOUNT_TYPE.upper())
            logging.info(f"Switched to {config.ACCOUNT_TYPE.upper()} account.")
            return True
        else:
            logging.error(f"Failed to connect: {reason}")
            return False

    def get_market_data(self, asset='EURUSD', time_period=60, num_candles=10):
        """
        Fetches the latest market data (candlestick patterns).

        Args:
            asset (str): The asset to fetch data for (e.g., 'EURUSD').
            time_period (int): The time period for each candle in seconds (e.g., 60 for 1 minute).
            num_candles (int): The number of recent candles to fetch.

        Returns:
            list: A list of candlestick data, or None if fetching fails.
        """
        if not self.api or not self.api.check_connect():
            logging.error("Not connected to IQ Option. Please connect first.")
            return None

        logging.info(f"Fetching last {num_candles} candles for {asset}...")
        candles = self.api.get_candles(asset, time_period, num_candles, time.time())

        if candles:
            logging.info("Successfully fetched market data.")
            return candles
        else:
            logging.error("Failed to fetch market data.")
            return None

if __name__ == '__main__':
    # This is for testing the connector directly.
    # To run this, you need to fill in your credentials in config.py

    # IMPORTANT: Never run this test with a real account until you are
    # absolutely sure the bot behaves as expected on a practice account.

    if config.IQ_OPTION_USERNAME == "YOUR_USERNAME" or config.IQ_OPTION_PASSWORD == "YOUR_PASSWORD":
        print("Please fill in your IQ Option credentials in config.py before running this test.")
    else:
        connector = IQConnector()
        if connector.connect():
            # Example: Fetching data
            market_data = connector.get_market_data()
            if market_data:
                print(f"Successfully fetched {len(market_data)} candles.")
                # You can uncomment the line below to see the raw data
                # for candle in market_data:
                #     print(candle)
