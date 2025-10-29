# LLM Trading Signal Bot for IQ Option

This project is a Python-based trading bot that generates trading signals for the IQ Option platform using a Large Language Model (LLM). The bot is designed to be a **signal provider**, not an automated trading system. It fetches market data, sends it to an LLM for analysis, and then displays the resulting signal (CALL, PUT, or HOLD) in the console.

**Disclaimer:** Trading carries significant risk. This bot is intended for educational purposes and should be used with a **practice account**. The creators of the `iqoptionapi` library strongly advise against using it with a real money account. If you choose to use a real account, you assume all risks involved.

## Features

-   Connects to your IQ Option account (practice or real).
-   Fetches real-time candlestick data.
-   Integrates with LLM providers (OpenAI and Gemini) to generate trading signals.
-   Configurable and extensible.

## Setup Instructions

Follow these steps to get the bot up and running:

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a Python virtual environment to manage the project's dependencies.

```bash
# Create the virtual environment
python3 -m venv trading_bot/venv

# Activate the virtual environment
source trading_bot/venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python libraries using the `requirements.txt` file.

```bash
pip install -r trading_bot/requirements.txt
```

### 4. Configure the Bot

Before running the bot, you need to configure your credentials and API keys in the `trading_bot/config.py` file.

1.  **Open `trading_bot/config.py`** in a text editor.

2.  **Set your IQ Option credentials**:
    -   `IQ_OPTION_USERNAME`: Your IQ Option email address.
    -   `IQ_OPTION_PASSWORD`: Your IQ Option password.
    -   `ACCOUNT_TYPE`: Set to `"practice"` (recommended) or `"real"`.

3.  **Choose your LLM Provider**:
    -   `LLM_PROVIDER`: Set to `"openai"` or `"gemini"`.

4.  **Set your API Key**:
    -   If you chose `"openai"`, fill in `OPENAI_API_KEY`.
    -   If you chose `"gemini"`, fill in `GEMINI_API_KEY`.

## How to Run the Bot

Once you have completed the setup and configuration, you can run the bot with the following command from the root of the repository:

```bash
python3 trading_bot/main.py
```

The bot will connect to your IQ Option account, fetch market data, and start generating signals every 60 seconds. The signals will be displayed in your console.

To stop the bot, press `Ctrl+C`.
