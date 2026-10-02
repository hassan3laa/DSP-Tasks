from signal_model import *

def add_signals(signals):
    first_signal = signals[0]

    ans=Signal(first_signal.signal_type, first_signal.is_periodic, first_signal.n)
    ans.indices = first_signal.indices.copy()

    for i in range(first_signal.n):
        total=0

        for signal in signals:
            total+= signal.samples[i]
        ans.samples.append(total)

    return ans

def multiply_signal(signal, const):
    ans = Signal(signal.signal_type, signal.is_periodic, signal.n)

    ans.indices = signal.indices.copy()

    for sample in signal.samples:
        ans.samples.append(const*sample)

    return ans