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

def remove_DC_component(signal):
    updated_signal = Signal(signal.signal_type, signal.is_periodic, signal.n)
    updated_signal.indices = signal.indices.copy()

    mean_value = sum(signal.samples) / len(signal.samples)

    for sample in signal.samples:
        updated_signal.samples.append(sample - mean_value)

    return updated_signal

def idft(amplitudes, phases):
    n = len(amplitudes)
    if n == 0:
        raise ValueError("No frequency components provided")

    if len(phases) != n:
        raise ValueError("Amplitudes and phases must have the same length")

    samples = []
    for i in range(n):
        real = 0
        for k in range(n):
            angle = 2 * math.pi * k * i / n
            real += amplitudes[k] * math.cos(angle + phases[k])
        samples.append(real / n)

    return samples

def calculate_first_derivative(signal):
    result = Signal(signal.signal_type, signal.is_periodic, signal.n - 1)
    result.indices = signal.indices[1:].copy()

    for i in range(1, signal.n):
        result.samples.append(signal.samples[i] - signal.samples[i - 1])

    return result


def calculate_second_derivative(signal):
    result = Signal(signal.signal_type, signal.is_periodic, signal.n - 2)
    result.indices = signal.indices[1:-1].copy()

    for i in range(1, signal.n - 1):
        result.samples.append(
            signal.samples[i + 1]
            - 2 * signal.samples[i]
            + signal.samples[i - 1]
        )

    return result


def moving_average(signal, window_size):
    if window_size <= 0:
        raise ValueError("Window size must be positive")

    if window_size > len(signal.samples):
        raise ValueError("Window size cannot exceed the number of samples")

    result_n = len(signal.samples) - window_size + 1

    result = Signal(
        signal.signal_type,
        signal.is_periodic,
        result_n
    )

    result.indices = signal.indices[:result_n].copy()

    for i in range(result_n):
        total = 0

        for j in range(window_size):
            total += signal.samples[i + j]

        result.samples.append(total / window_size)

    return result


def fold_signal(signal):
    result = Signal(
        signal.signal_type,
        signal.is_periodic,
        signal.n
    )

    result.indices = signal.indices.copy()
    result.samples = signal.samples[::-1].copy()

    return result


def shift_signal(signal, shift_amount):
    result = Signal(
        signal.signal_type,
        signal.is_periodic,
        signal.n
    )

    result.indices = [
        index + shift_amount
        for index in signal.indices
    ]

    result.samples = signal.samples.copy()

    return result
