class OversizedMarkerError (Exception):
    def __init__(self, message: str):
        self.m = message

    def __str__(self):
        return self.m
