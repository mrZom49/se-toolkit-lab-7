"""Configuration loading from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Bot configuration settings."""

    model_config = SettingsConfigDict(
        env_file=".env.bot.secret",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Telegram
    bot_token: str = ""

    # LMS API
    lms_api_base_url: str = ""
    lms_api_key: str = ""

    # LLM API
    llm_api_key: str = ""
    llm_api_base_url: str = ""
    llm_api_model: str = "coder-model"

    @property
    def is_test_mode(self) -> bool:
        """Check if running in test mode (no Telegram connection)."""
        return not self.bot_token

    def validate_for_telegram(self) -> None:
        """Validate settings for Telegram mode.
        
        Raises:
            ValueError: If required settings are missing.
        """
        if not self.bot_token:
            raise ValueError("BOT_TOKEN is required for Telegram mode")
        if not self.lms_api_base_url:
            raise ValueError("LMS_API_BASE_URL is required")
        if not self.lms_api_key:
            raise ValueError("LMS_API_KEY is required")


def load_settings() -> BotSettings:
    """Load bot settings from environment.
    
    Returns:
        BotSettings instance with loaded configuration.
    """
    return BotSettings()
