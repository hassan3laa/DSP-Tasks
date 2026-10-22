from numpy.ma.core import maximum

from .signal_model import *
import math

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

def dft(signal, sampling_frequency):
    n = len(signal.samples)
    if n == 0:
        raise ValueError("Signal has no samples")

    if sampling_frequency <= 0:
        raise ValueError("Sampling frequency has to be positive")

    frequencies = []
    amplitudes = []
    phases = []
    for k in range(n):
        real = 0
        imagin = 0
        for i in range(n):
            angel = 2*math.pi*k*i/n
            real += signal.samples[i]*math.cos(angel)
            imagin -= signal.samples[i]*math.sin(angel)
        amplitude = math.sqrt(real**2+imagin**2)
        phase=math.atan2(imagin,real)

        frequencies.append(k * sampling_frequency / n)
        amplitudes.append(amplitude)
        phases.append(phase)

    return frequencies, amplitudes, phases


def normalize_amplitudes(amplitudes):
    maximum = max(amplitudes)
    if maximum == 0:
        return [0] * len(amplitudes)
    return [amplitude / maximum for amplitude in amplitudes]

def get_dominant_frequencies(frequencies, normalized_amplitudes):
    dominant=[]
    for frequency, amplitude in zip(frequencies, normalized_amplitudes):
        if amplitude>0.5:
            dominant.append(frequency)

    return dominant

def modify_component (amplitudes, phases, k ,new_amplitude = None, new_phase = None):
    if k<0 or k>=len(amplitudes):
        raise ValueError("Component index out of range")

    amplitudes = amplitudes.copy()
    phases = phases.copy()

    if new_amplitude is not None:
        amplitudes[k]=new_amplitude

    if new_phase is not None:
        phases[k]=new_phase
    return amplitudes, phases