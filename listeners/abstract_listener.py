import time
from abc import ABC


class Listener(ABC):
    last_update = time.time()

    def red(self):
        pass
