class TelegramAPIException(Exception):
    """
    Raised when Telegram API returns an error

    Note:
        In case if http client library doesn't provide `Response.raise_for_status()`
        method, this exception is raised if response status code is >= 400
    """

    pass
