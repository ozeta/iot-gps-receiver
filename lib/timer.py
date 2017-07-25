"""Simple Timer Module."""
import utime


class Timer:
    """Timer class."""
    def __init__(self):
        """Initialize class."""
        self.startms = 0

    def start(self):
        """Initialize count."""
        self.startms = utime.ticks_ms()
        return self.startms

    def stop(self):
        """Stop count."""
        return self.count()

    def wait(self, millis):
        """Wait for millis."""
        utime.sleep_ms(millis)

    def count(self):
        """Count elapsed millis."""
        return utime.ticks_ms() - self.startms

    def reset(self):
        """Reset timer."""
        self.startms = 0
