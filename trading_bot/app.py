from flask import Flask, render_template, request, redirect, url_for
import logging
import config
from iq_connector import IQConnector
from llm_signal_generator import LLMSignalGenerator
from technical_analyzer import TechnicalAnalyzer

app = Flask(__name__)

# --- Global Variables ---
iq_connector = None
llm_signal_generator = None
# Use an in-memory variable for the asset, initialized from the config file.
current_asset = config.ASSET

def initialize_bot():
    """Initializes all the bot components."""
    global iq_connector, llm_signal_generator

    logging.info("Initializing bot components...")

    if config.IQ_OPTION_USERNAME == "YOUR_USERNAME" or config.IQ_OPTION_PASSWORD == "YOUR_PASSWORD":
        raise Exception("Please fill in your IQ Option credentials in config.py")

    provider = config.LLM_PROVIDER.lower()
    # Add other provider checks as needed

    iq_connector = IQConnector()
    if not iq_connector.connect():
        raise Exception("Failed to connect to IQ Option.")

    llm_signal_generator = LLMSignalGenerator()
    logging.info("Bot components initialized successfully.")

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Renders the main page and handles asset change requests.
    """
    global current_asset
    if request.method == 'POST':
        new_asset = request.form.get('asset')
        if new_asset:
            current_asset = new_asset.upper()
        return redirect(url_for('home'))

    try:
        market_data = iq_connector.get_market_data(asset=current_asset, time_period=60, num_candles=50)

        if not market_data:
            return render_template('index.html', asset=current_asset, error=f"Could not retrieve market data for {current_asset}.")

        analyzer = TechnicalAnalyzer(market_data)
        analysis_results = analyzer.analyze()
        signal = llm_signal_generator.generate_signal(analysis_results)

        if not signal:
            return render_template('index.html', asset=current_asset, error="Could not retrieve a valid signal from the LLM.")

        return render_template('index.html', asset=current_asset, signal=signal)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return render_template('index.html', asset=current_asset, error=str(e))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        initialize_bot()
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"Failed to start the application: {e}")
