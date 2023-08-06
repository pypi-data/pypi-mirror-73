from .errors import ConfigurationError


class ZengaPayConfig(object):
    def __init__(self, config):
        """
        config = {
            ZENGAPAY_ENVIRONMENT: os.environ.get("ZENGAPAY_APP_SETTINGS", "sandbox"),
            ZENGAPAY_BASE_URL: os.environ.get("ZENGAPAY_BASE_URL", "https://api.sandbox.zengapay.com/v1/"),
            ZENGAPAY_USER_API_TOKEN: os.environ.get("ZENGAPAY_USER_API_TOKEN")
        }
        """

        self.config = config

    @property
    def environment(self):
        env = self.config["ZENGAPAY_ENVIRONMENT"]
        if not env:
            raise ConfigurationError(
                "ZENGAPAY_ENVIRONMENT is missing in configuration."
            )
        return env

    @property
    def base_url(self):
        base_url = self.config["ZENGAPAY_BASE_URL"]
        if not base_url:
            raise ConfigurationError("ZENGAPAY BASE URL is missing in configuration.")
        return base_url

    @property
    def api_token(self):
        token = self.config["ZENGAPAY_USER_API_TOKEN"]
        if not token:
            raise ConfigurationError(
                "ZENGAPAY_USER_API_TOKEN is missing in configuration."
            )
        return token
