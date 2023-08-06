from signal import signal, SIGINT, SIGTERM, SIG_DFL

class Handler:
    def __init__(self):
        self._terminated = False

    @property
    def terminated(self):
        return self._terminated

    def terminate(self):
        self._terminated = True

    def __call__(self, sig, frame):
        self.terminate()

def setup():
    hdlr = Handler()
    signal(SIGINT, hdlr)
    signal(SIGTERM, hdlr)
    return hdlr

def reset():
    signal(SIGINT, SIG_DFL)
    signal(SIGTERM, SIG_DFL)