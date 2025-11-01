from flask import Flask, render_template
import logging
import config
from iq_connector import IQConnector
from llm_signal_generator import LLMSignalGenerator
from technical_analyzer import TechnicalAnalyzer

app = Flask(__name__)

# --- Global Variables ---
# We initialize these once to avoid reconnecting on every page refresh.
iq_connector = None
llm_signal_generator = None

def initialize_bot():
    """Initializes all the bot components."""
    global iq_connector, llm_signal_generator

    logging.info("Initializing bot components...")

    # --- Initial Checks ---
    if config.IQ_OPTION_USERNAME == "YOUR_USERNAME" or config.IQ_OPTION_PASSWORD == "YOUR_PASSWORD":
        raise Exception("Please fill in your IQ Option credentials in config.py")

    provider = config.LLM_PROVIDER.lower()
    if provider == "openai" and (not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY"):
        raise Exception("Please fill in your OpenAI API key in config.py")
    elif provider == "gemini" and (not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY"):
        raise Exception("Please fill in your Gemini API key in config.py")

    # --- Initialization ---
    iq_connector = IQConnector()
    if not iq_connector.connect():
        raise Exception("Failed to connect to IQ Option.")

    llm_signal_generator = LLMSignalGenerator()
    logging.info("Bot components initialized successfully.")

@app.route('/')
def home():
    """
    Renders the main page with the latest trading signal.
    """
    try:
        # 1. Fetch market data
        market_data = iq_connector.get_market_data(asset='EURUSD', time_period=60, num_candles=50)

        if not market_data:
            return render_template('index.html', error="Could not retrieve market data.")

        # 2. Analyze the market data
        analyzer = TechnicalAnalyzer(market_data)
        analysis_results = analyzer.analyze()

        # 3. Generate a signal
        signal = llm_signal_generator.generate_signal(analysis_results)

        if not signal:
            return render_template('index.html', error="Could not retrieve a valid signal from the LLM.")

        # 4. Render the page with the signal
        return render_template('index.html', asset='EURUSD', signal=signal)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        initialize_bot()
        # Note: In a production environment, you would use a proper WSGI server instead of the Flask dev server.
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"Failed to start the application: {e}")
