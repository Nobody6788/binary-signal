import openai
import google.generativeai as genai
import config
import logging

class LLMSignalGenerator:
    """
    Handles communication with an LLM to generate trading signals.
    """
    def __init__(self):
        self.provider = config.LLM_PROVIDER.lower()
        if self.provider == "openai":
            if not config.OPENAI_API_KEY or config.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
                raise ValueError("OpenAI API key is not set in config.py")
            self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        elif self.provider == "gemini":
            if not config.GEMINI_API_KEY or config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
                raise ValueError("Gemini API key is not set in config.py")
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.client = genai.GenerativeModel('gemini-pro')
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate_signal(self, analysis_data):
        """
        Generates a trading signal based on the provided technical analysis data.

        Args:
            analysis_data (dict): A dictionary containing technical indicators and patterns.

        Returns:
            str: A trading signal ("CALL", "PUT", or "HOLD"), or None if an error occurs.
        """
        if not analysis_data:
            logging.warning("Analysis data is empty. Cannot generate a signal.")
            return None

        prompt = self._build_prompt(analysis_data)

        try:
            logging.info(f"Sending request to {self.provider} for a trading signal...")
            if self.provider == "openai":
                return self._get_openai_signal(prompt)
            elif self.provider == "gemini":
                return self._get_gemini_signal(prompt)
        except Exception as e:
            logging.error(f"An error occurred while communicating with the LLM: {e}")
            return None

    def _build_prompt(self, analysis_data):
        """Builds the prompt for the LLM."""
        indicators = analysis_data.get('indicators', {})
        patterns = analysis_data.get('patterns', [])

        prompt_data = "--- Market Analysis ---\n"
        prompt_data += "Technical Indicators:\n"
        for key, value in indicators.items():
            prompt_data += f"- {key}: {value:.2f}\n" if isinstance(value, float) else f"- {key}: {value}\n"

        prompt_data += "\nDetected Candlestick Patterns:\n"
        if patterns:
            for pattern in patterns:
                prompt_data += f"- {pattern}\n"
        else:
            prompt_data += "- None\n"

        system_prompt = (
            "You are a financial analyst specializing in binary options trading. "
            "Your task is to analyze the provided market data, including technical "
            "indicators and candlestick patterns, to predict the next market "
            "movement for the next 60 seconds. Respond with only one of the "
            "following commands: 'CALL' (if you predict the price will go up), "
            "'PUT' (if you predict the price will go down), or 'HOLD' (if you are "
            "uncertain or predict no significant movement)."
        )
        return f"{system_prompt}\n\n{prompt_data}"

    def _get_openai_signal(self, prompt):
        """Gets a signal from the OpenAI API."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5,
            temperature=0.5,
        )
        signal = response.choices[0].message.content.strip().upper()
        return self._validate_signal(signal)

    def _get_gemini_signal(self, prompt):
        """Gets a signal from the Gemini API."""
        response = self.client.generate_content(prompt)
        signal = response.text.strip().upper()
        return self._validate_signal(signal)

    def _validate_signal(self, signal):
        """Validates the signal received from the LLM."""
        logging.info(f"Received signal from {self.provider}: {signal}")
        if signal in ["CALL", "PUT", "HOLD"]:
            return signal
        else:
            logging.warning(f"Received an invalid signal: {signal}")
            return "HOLD"  # Default to a safe action

if __name__ == '__main__':
    # This is for testing the signal generator directly.
    # To run this, you need to fill in your LLM API key in config.py

    provider = config.LLM_PROVIDER.lower()
    api_key_set = False
    if provider == "openai":
        if config.OPENAI_API_KEY and config.OPENAI_API_KEY != "YOUR_OPENAI_API_KEY":
            api_key_set = True
    elif provider == "gemini":
        if config.GEMINI_API_KEY and config.GEMINI_API_KEY != "YOUR_GEMINI_API_KEY":
            api_key_set = True

    if not api_key_set:
        print(f"Please fill in your {provider.upper()} API key in config.py before running this test.")
    else:
        # Example with dummy analysis data
        dummy_analysis = {
            'indicators': {
                'sma_14': 1.55,
                'rsi_14': 60.0,
                'bollinger_upper': 1.65,
                'bollinger_lower': 1.45,
                'macd': 0.05,
                'stochastic_oscillator': 80.0,
            },
            'patterns': ['CDL_DOJI'],
        }

        signal_generator = LLMSignalGenerator()
        signal = signal_generator.generate_signal(dummy_analysis)

        if signal:
            print(f"Generated Signal: {signal}")
        else:
            print("Failed to generate a signal.")
