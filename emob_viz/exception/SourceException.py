class SourceException(Exception):
    def __init__(self, msg: str, cause: Exception):
        self.msg = msg
        self.cause = cause
        super().__init__(self.msg, self.cause)
