import os

# Load from environment variable; fall back to a default only in development
SECRET_KEY = os.environ.get("FALSEFRONT_SECRET_KEY", "dev-insecure-key-change-me")

# Anthropic API key for AI profiling
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")