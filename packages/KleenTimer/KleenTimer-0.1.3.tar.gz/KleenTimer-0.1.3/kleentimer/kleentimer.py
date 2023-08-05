from time import time


class KleenTimer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.fmt = "{hours:02d}:{minutes:02d}:{secondes:02d}"

    def init_timer(self, fmt):
        self.fmt = fmt

    def start_timer(self):
        self.start_time = time()

    def end_timer(self):
        self.end_time = time()

    def elapsed_time(self):
        total_s = int(self.end_time - self.start_time)
        secondes = total_s % 60
        minutes = (total_s / 60) % 60
        minutes = int(minutes)
        hours = (total_s / (60 * 60)) % 24
        hours = int(hours)
        return self.fmt.format(hours=hours, minutes=minutes, secondes=secondes)


kleentimer = KleenTimer()
