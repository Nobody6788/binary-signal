import openai
import config
import logging

class LLMSignalGenerator:
    """
    Handles communication with an LLM to generate trading signals.
    """
    def __init__(self):
        if config.LLM_PROVIDER.lower() == "openai":
            self.client = openai.OpenAI(api_key=config.LLM_API_KEY)
        else:
            # In the future, you can add more providers here.
            # For example:
            # if config.LLM_PROVIDER.lower() == "gemini":
            #     self.client = gemini.GenerativeModel(...)
            raise ValueError(f"Unsupported LLM provider: {config.LLM_PROVIDER}")

    def generate_signal(self, market_data):
        """
        Generates a trading signal based on the provided market data.

        Args:
            market_data (list): A list of candlestick data from the IQ Option API.

        Returns:
            str: A trading signal ("CALL", "PUT", or "HOLD"), or None if an error occurs.
        """
        if not market_data:
            logging.warning("Market data is empty. Cannot generate a signal.")
            return None

        # Format the market data into a clear prompt for the LLM.
        prompt_data = "Candlestick data (open, close, high, low):\n"
        for candle in market_data:
            prompt_data += f"- Open: {candle['open']}, Close: {candle['close']}, High: {candle['max']}, Low: {candle['min']}\n"

        system_prompt = (
            "You are a financial analyst specializing in binary options trading. "
            "Your task is to analyze the provided candlestick data and predict the "
            "next market movement for the next 60 seconds. Respond with only one "
            "of the following commands: 'CALL' (if you predict the price will go up), "
            "'PUT' (if you predict the price will go down), or 'HOLD' (if you are "
            "uncertain or predict no significant movement)."
        )

        try:
            logging.info("Sending request to LLM for a trading signal...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt_data}
                ],
                max_tokens=5,
                temperature=0.5,
            )

            signal = response.choices[0].message.content.strip().upper()
            logging.info(f"Received signal from LLM: {signal}")

            if signal in ["CALL", "PUT", "HOLD"]:
                return signal
            else:
                logging.warning(f"Received an invalid signal from the LLM: {signal}")
                return "HOLD" # Default to a safe action

        except Exception as e:
            logging.error(f"An error occurred while communicating with the LLM: {e}")
            return None

if __name__ == '__main__':
    # This is for testing the signal generator directly.
    # To run this, you need to fill in your LLM API key in config.py

    if config.LLM_API_KEY == "YOUR_API_KEY":
        print("Please fill in your LLM API key in config.py before running this test.")
    else:
        # Example with dummy market data
        dummy_data = [
            {'open': 1.1, 'close': 1.2, 'max': 1.25, 'min': 1.05},
            {'open': 1.2, 'close': 1.3, 'max': 1.35, 'min': 1.15},
            {'open': 1.3, 'close': 1.25, 'max': 1.32, 'min': 1.22},
        ]

        signal_generator = LLMSignalGenerator()
        signal = signal_generator.generate_signal(dummy_data)

        if signal:
            print(f"Generated Signal: {signal}")
        else:
            print("Failed to generate a signal.")
