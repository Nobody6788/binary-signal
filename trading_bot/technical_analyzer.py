import pandas as pd
import pandas_ta as ta_patterns
from ta.volatility import BollingerBands
from ta.trend import MACD, SMAIndicator
from ta.momentum import RSIIndicator, StochasticOscillator

class TechnicalAnalyzer:
    """
    Handles the calculation of technical indicators and candlestick patterns.
    """
    def __init__(self, market_data):
        """
        Initializes the TechnicalAnalyzer with market data.

        Args:
            market_data (list): A list of candlestick data from the IQ Option API.
        """
        self.df = self._prepare_dataframe(market_data)
        self.analysis = {}

    def _prepare_dataframe(self, market_data):
        """Prepares a pandas DataFrame from the raw market data."""
        df = pd.DataFrame(market_data)
        df = df[['open', 'max', 'min', 'close', 'volume']]
        df.rename(columns={'max': 'high', 'min': 'low'}, inplace=True)
        return df

    def analyze(self):
        """
        Performs a full technical analysis, calculating indicators and patterns.
        """
        self._calculate_indicators()
        self._identify_patterns()
        return self.analysis

    def _calculate_indicators(self):
        """Calculates all the technical indicators."""
        # Moving Average
        sma = SMAIndicator(close=self.df["close"], window=14)
        self.df['sma_14'] = sma.sma_indicator()

        # RSI
        rsi = RSIIndicator(close=self.df["close"], window=14)
        self.df['rsi_14'] = rsi.rsi()

        # Bollinger Bands
        bollinger = BollingerBands(close=self.df["close"], window=20, window_dev=2)
        self.df['bollinger_upper'] = bollinger.bollinger_hband()
        self.df['bollinger_lower'] = bollinger.bollinger_lband()

        # MACD
        macd = MACD(close=self.df["close"], window_slow=26, window_fast=12, window_sign=9)
        self.df['macd'] = macd.macd()

        # Stochastic Oscillator
        stochastic = StochasticOscillator(high=self.df['high'], low=self.df['low'], close=self.df['close'], window=14, smooth_window=3)
        self.df['stochastic_oscillator'] = stochastic.stoch()

        # Store the latest indicator values
        latest_indicators = self.df.iloc[-1]
        self.analysis['indicators'] = {
            'sma_14': latest_indicators.get('sma_14'),
            'rsi_14': latest_indicators.get('rsi_14'),
            'bollinger_upper': latest_indicators.get('bollinger_upper'),
            'bollinger_lower': latest_indicators.get('bollinger_lower'),
            'macd': latest_indicators.get('macd'),
            'stochastic_oscillator': latest_indicators.get('stochastic_oscillator'),
        }

    def _identify_patterns(self):
        """Identifies all candlestick patterns using pandas-ta."""
        # Use the candlestick pattern recognition feature of pandas-ta
        self.df.ta.cdl_pattern(name="all", append=True)

        # Find which patterns were detected in the last candle
        latest_patterns = self.df.iloc[-1]
        detected_patterns = []
        for col in latest_patterns.index:
            if col.startswith('CDL_') and latest_patterns[col] != 0:
                detected_patterns.append(col)

        self.analysis['patterns'] = detected_patterns

if __name__ == '__main__':
    # This is for testing the analyzer directly.
    dummy_data = [
        {'open': 1.10, 'close': 1.12, 'max': 1.13, 'min': 1.09, 'volume': 100},
        {'open': 1.12, 'close': 1.15, 'max': 1.16, 'min': 1.11, 'volume': 120},
        {'open': 1.15, 'close': 1.13, 'max': 1.16, 'min': 1.12, 'volume': 110},
        {'open': 1.13, 'close': 1.18, 'max': 1.19, 'min': 1.12, 'volume': 130},
        {'open': 1.18, 'close': 1.22, 'max': 1.23, 'min': 1.17, 'volume': 140},
        {'open': 1.22, 'close': 1.20, 'max': 1.23, 'min': 1.19, 'volume': 125},
        {'open': 1.20, 'close': 1.25, 'max': 1.26, 'min': 1.19, 'volume': 150},
        {'open': 1.25, 'close': 1.28, 'max': 1.29, 'min': 1.24, 'volume': 160},
        {'open': 1.28, 'close': 1.26, 'max': 1.29, 'min': 1.25, 'volume': 145},
        {'open': 1.26, 'close': 1.30, 'max': 1.31, 'min': 1.25, 'volume': 170},
        {'open': 1.30, 'close': 1.28, 'max': 1.31, 'min': 1.27, 'volume': 165},
        {'open': 1.28, 'close': 1.32, 'max': 1.33, 'min': 1.27, 'volume': 180},
        {'open': 1.32, 'close': 1.35, 'max': 1.36, 'min': 1.31, 'volume': 190},
        {'open': 1.35, 'close': 1.33, 'max': 1.36, 'min': 1.32, 'volume': 175},
        {'open': 1.33, 'close': 1.38, 'max': 1.39, 'min': 1.32, 'volume': 200},
        {'open': 1.38, 'close': 1.42, 'max': 1.43, 'min': 1.37, 'volume': 210},
        {'open': 1.42, 'close': 1.40, 'max': 1.43, 'min': 1.39, 'volume': 195},
        {'open': 1.40, 'close': 1.45, 'max': 1.46, 'min': 1.39, 'volume': 220},
        {'open': 1.45, 'close': 1.48, 'max': 1.49, 'min': 1.44, 'volume': 230},
        {'open': 1.48, 'close': 1.46, 'max': 1.49, 'min': 1.45, 'volume': 215},
        {'open': 1.46, 'close': 1.50, 'max': 1.51, 'min': 1.45, 'volume': 240},
        {'open': 1.50, 'close': 1.52, 'max': 1.53, 'min': 1.49, 'volume': 250},
        {'open': 1.52, 'close': 1.55, 'max': 1.56, 'min': 1.51, 'volume': 260},
        {'open': 1.55, 'close': 1.53, 'max': 1.56, 'min': 1.52, 'volume': 245},
        {'open': 1.53, 'close': 1.58, 'max': 1.59, 'min': 1.52, 'volume': 270},
        {'open': 1.58, 'close': 1.60, 'max': 1.61, 'min': 1.57, 'volume': 280},
        {'open': 1.60, 'close': 1.58, 'max': 1.61, 'min': 1.57, 'volume': 275},
        {'open': 1.58, 'close': 1.62, 'max': 1.63, 'min': 1.57, 'volume': 290},
        {'open': 1.62, 'close': 1.65, 'max': 1.66, 'min': 1.61, 'volume': 300},
        {'open': 1.65, 'close': 1.63, 'max': 1.66, 'min': 1.62, 'volume': 285},
    ]

    analyzer = TechnicalAnalyzer(dummy_data)
    analysis_results = analyzer.analyze()

    print("--- Technical Analysis Results ---")
    print("\nIndicators:")
    for key, value in analysis_results.get('indicators', {}).items():
        print(f"- {key}: {value}")

    print("\nDetected Patterns:")
    patterns = analysis_results.get('patterns', [])
    if patterns:
        for pattern in patterns:
            print(f"- {pattern}")
    else:
        print("- No patterns detected in the latest candle.")

    print("\n--------------------------------")
