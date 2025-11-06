# LLM Trading Signal Bot for IQ Option

This project is a Python-based trading bot that generates trading signals for the IQ Option platform using a Large Language Model (LLM). The bot is designed to be a **signal provider**, not an automated trading system. It can be run in two modes: as a console application or as a web-based user interface.

**Disclaimer:** Trading carries significant risk. This bot is intended for educational purposes and should be used with a **practice account**. The creators of the `iqoptionapi` library strongly advise against using it with a real money account. If you choose to use a real account, you assume all risks involved.

## Features--------------

-   Connects to your IQ Option account (practice or real).
-   Fetches real-time candlestick data for a user-configurable asset.
-   Performs technical analysis with 5 indicators and candlestick pattern recognition.
-   Integrates with LLM providers (OpenAI, Gemini, and OpenRouter) to generate trading signals.
-   Provides both a console-based and a web-based user interface.
-   Configurable and extensible.

## Setup Instructions

Follow these steps to get the bot up and running:

### Prerequisites

- **Python 3.7.2 or higher:** This project requires a specific Python version due to the `iqoptionapi` library.
- **TA-Lib:** This project uses the `TA-Lib` library for technical analysis, which requires the underlying C library to be installed first.

  **On Linux (Debian/Ubuntu):**
  ```bash
  sudo apt-get update && sudo apt-get install -y libta-lib0-dev
  ```

  **On macOS:**
  ```bash
  brew install ta-lib
  ```

  **On Windows:**
  Download and install `ta-lib-0.4.0-msvc.zip` from [SourceForge](https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/).

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

3.  **Set the Trading Asset**:
    -   `ASSET`: The asset you want to monitor (e.g., `"EURUSD"`, `"GBPUSD"`).

4.  **Choose your LLM Provider**:
    -   `LLM_PROVIDER`: Set to `"openai"`, `"gemini"`, or `"openrouter"`.

5.  **Set your API Key(s)**:
    -   If you chose `"openai"`, fill in `OPENAI_API_KEY`.
    -   If you chose `"gemini"`, fill in `GEMINI_API_KEY`.
    -   If you chose `"openrouter"`, fill in `OPENROUTER_API_KEY`.

6.  **(Optional) Configure OpenRouter Model**:
    -   If you are using OpenRouter, you can specify which model to use in the `OPENROUTER_MODEL` variable. A good free option is `"google/gemma-7b-it"`.

## How to Run the Bot

You can run the bot in two modes:

### Mode 1: Console-Based (for logging and debugging)

This mode prints the signals directly to your console.

```bash
python3 trading_bot/main.py
```

### Mode 2: Web-Based User Interface

This mode launches a local web server so you can view the signals in your browser.

1.  **Run the Flask application:**
    ```bash
    python3 trading_bot/app.py
    ```

2.  **Open your web browser** and go to the following address:
    ```
    http://127.0.0.1:5000
    ```

The web page will display the latest signal and will automatically refresh every 60 seconds.

To stop the bot in either mode, press `Ctrl+C` in your terminal.
