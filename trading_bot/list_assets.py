import logging
from iq_connector import IQConnector
import config

def list_all_assets():
    """
    Connects to the IQ Option API and lists all available assets.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # --- Initial Checks ---
    if config.IQ_OPTION_USERNAME == "YOUR_USERNAME" or config.IQ_OPTION_PASSWORD == "YOUR_PASSWORD":
        logging.error("Please fill in your IQ Option credentials in config.py before running this script.")
        return

    # --- Initialization and Connection ---
    iq_connector = IQConnector()
    if not iq_connector.connect():
        logging.error("Failed to connect to IQ Option. Exiting.")
        return

    logging.info("Successfully connected. Fetching list of all available assets...")

    # --- Fetch and Display Assets ---
    try:
        all_assets = iq_connector.api.get_all_open_time()

        print("\n--- Currently Available Assets ---")

        # Forex Assets
        print("\nForex:")
        forex_assets = all_assets.get("forex", {})
        if forex_assets:
            for asset, details in forex_assets.items():
                if details.get("open"):
                    print(f"- {asset}")
        else:
            print("- None available right now.")

        # Digital Assets
        print("\nDigital:")
        digital_assets = all_assets.get("digital", {})
        if digital_assets:
            for asset, details in digital_assets.items():
                if details.get("open"):
                    print(f"- {asset}")
        else:
            print("- None available right now.")

        # Crypto Assets
        print("\nCrypto:")
        crypto_assets = all_assets.get("crypto", {})
        if crypto_assets:
            for asset, details in crypto_assets.items():
                if details.get("open"):
                    print(f"- {asset}")
        else:
            print("- None available right now.")

        print("\n------------------------------------")
        logging.info("Note: The list of available assets can change based on market hours.")

    except Exception as e:
        logging.error(f"An error occurred while fetching assets: {e}")

if __name__ == "__main__":
    list_all_assets()
