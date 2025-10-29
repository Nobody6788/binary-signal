import time
import logging
import config
from iq_connector import IQConnector
from llm_signal_generator import LLMSignalGenerator

def main():
    """
    The main application loop for the trading bot.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # --- Initial Checks ---
    if config.IQ_OPTION_USERNAME == "YOUR_USERNAME" or config.IQ_OPTION_PASSWORD == "YOUR_PASSWORD":
        logging.error("Please fill in your IQ Option credentials in config.py before running the bot.")
        return

    if config.LLM_API_KEY == "YOUR_API_KEY":
        logging.error("Please fill in your LLM API key in config.py before running the bot.")
        return

    # --- Initialization ---
    iq_connector = IQConnector()
    llm_signal_generator = LLMSignalGenerator()

    if not iq_connector.connect():
        logging.error("Failed to connect to IQ Option. Exiting.")
        return

    logging.info("Trading Bot is now running. Press Ctrl+C to stop.")
    logging.info("The bot will provide a new trading signal every 60 seconds.")

    # --- Main Loop ---
    try:
        while True:
            # 1. Fetch market data
            market_data = iq_connector.get_market_data(asset='EURUSD', time_period=60, num_candles=10)

            if market_data:
                # 2. Generate a signal
                signal = llm_signal_generator.generate_signal(market_data)

                if signal:
                    # 3. Display the signal to the user
                    logging.info(f"--- TRADING SIGNAL ---")
                    logging.info(f"Asset: EURUSD")
                    logging.info(f"Signal: {signal}")
                    logging.info(f"----------------------")
                else:
                    logging.warning("Could not retrieve a valid signal from the LLM.")
            else:
                logging.warning("Could not retrieve market data. Skipping this cycle.")

            # Wait for the next cycle
            time.sleep(60)

    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        logging.info("Shutting down.")

if __name__ == "__main__":
    main()
