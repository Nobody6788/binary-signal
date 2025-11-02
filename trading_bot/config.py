# -- IQ Option Configuration --
# IMPORTANT: It is strongly recommended to use a practice account for development and testing.
# Trading with real money carries significant risk. This bot is designed for a practice account.
# To use a real account, change ACCOUNT_TYPE to "real". You assume all risks if you do so.
ACCOUNT_TYPE = "practice"  # or "real"
IQ_OPTION_USERNAME = "YOUR_USERNAME"
IQ_OPTION_PASSWORD = "YOUR_PASSWORD"

# -- Trading Configuration --
# Set the asset you want to monitor (e.g., "EURUSD", "GBPUSD", etc.)
ASSET = "EURUSD"

# -- LLM Provider Configuration --
# Choose your LLM provider. Supported options: "openai", "gemini", "openrouter"
# Make sure to fill in the corresponding API key and settings below.
LLM_PROVIDER = "openrouter"  # or "openai", "gemini"

# -- API Keys --
# Fill in the API key for the provider you selected above.
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"

# -- OpenRouter Specific Settings --
# If you are using OpenRouter, specify the model you want to use.
# A good free option is "google/gemma-7b-it".
# For a full list of models, see: https://openrouter.ai/models
OPENROUTER_MODEL = "google/gemma-7b-it"
