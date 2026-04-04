import os

APP_ENV = os.environ.get("APP_ENV", "production")

# Load from environment variable; only use insecure default in development
SECRET_KEY = os.environ.get("FALSEFRONT_SECRET_KEY")
if not SECRET_KEY:
    if APP_ENV == "development":
        SECRET_KEY = "dev-insecure-key-change-me"
    else:
        raise RuntimeError(
            "FALSEFRONT_SECRET_KEY must be set when APP_ENV is not 'development'"
        )

# Anthropic API key for AI profiling
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")