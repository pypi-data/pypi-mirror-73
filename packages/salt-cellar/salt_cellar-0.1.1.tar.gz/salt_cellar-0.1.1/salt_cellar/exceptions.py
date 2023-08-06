class SaltCellarError(Exception):
    pass


class DatabaseUnavailableError(SaltCellarError):
    pass


class BlobCorruptionError(SaltCellarError):
    pass
