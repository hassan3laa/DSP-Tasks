from .signal_model import *

def add_signals(signals):
    first_signal = signals[0]

    for signal in signals:
        if signal.n != first_signal.n:
            raise ValueError("Signals must have the same number of samples")

    for signal in signals:
        if signal.indices != first_signal.indices:
            raise ValueError("Signals must have the same indices")

    ans=Signal(first_signal.signal_type, first_signal.is_periodic, first_signal.n)
    ans.indices = first_signal.indices.copy()

    for i in range(first_signal.n):
        total=0

        for signal in signals:
            total+= signal.samples[i]
        ans.samples.append(total)

    return ans

def subtract_signals(signals):
    first_signal = signals[0]

    for signal in signals:
        if signal.n != first_signal.n:
            raise ValueError("Signals must have the same number of samples")

    for signal in signals:
        if signal.indices != first_signal.indices:
            raise ValueError("Signals must have the same indices")

    ans = Signal(first_signal.signal_type, first_signal.is_periodic, first_signal.n)
    ans.indices = first_signal.indices.copy()

    for i in range(first_signal.n):
        total = first_signal.samples[i]

        for j in range(1, len(signals)):
            total -= signals[j].samples[i]

        ans.samples.append(abs(total))

    return ans

def multiply_signal(signal, const):
    ans = Signal(signal.signal_type, signal.is_periodic, signal.n)

    ans.indices = signal.indices.copy()

    for sample in signal.samples:
        ans.samples.append(const*sample)

    return ans

def square_signal(signal):
    ans=Signal(signal.signal_type, signal.is_periodic, signal.n)

    ans.indices = signal.indices.copy()

    for sample in signal.samples:
        ans.samples.append(sample**2)

    return ans

def normalize_signal(signal, option):
    ans = Signal(signal.signal_type, signal.is_periodic, signal.n)
    ans.indices = signal.indices.copy()

    minimum = min(signal.samples)
    maximum = max(signal.samples)

    if maximum == minimum:
        for sample in signal.samples:
            ans.samples.append(0)
        return ans

    for sample in signal.samples:
        if option == "-1 to 1":
            value = 2*(sample-minimum)/(maximum-minimum)-1
        else:
            value = (sample-minimum)/(maximum-minimum)
        ans.samples.append(value)
    return ans


def accumulate_signal(signal):
    ans = Signal(signal.signal_type, signal.is_periodic, signal.n)
    ans.indices = signal.indices.copy()

    total = 0
    for sample in signal.samples:
        total += sample
        ans.samples.append(total)

    return ans