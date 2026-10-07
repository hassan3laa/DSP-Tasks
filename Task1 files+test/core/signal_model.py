class Signal:
    def __init__(self, signal_type, is_periodic, n):
        self.signal_type = signal_type
        self.is_periodic = is_periodic
        self.n = n

        self.indices = []
        self.samples = []

        self.frequencies = []
        self.amplitudes = []
        self.phases = []