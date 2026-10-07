import matplotlib.pyplot as plt

def continuous_plot(signal, title) :
    plt.plot(signal.indices, signal.samples)
    plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

def discrete_plot(signal, title):
    markerline, stemlines, baseline = plt.stem(
        signal.indices,
        signal.samples
    )

    plt.setp(markerline, markersize=3)
    plt.setp(stemlines, linewidth=0.5)

    plt.title(title)
    plt.xlabel("Index")
    plt.ylabel("Amplitude")
    plt.grid()

    plt.show()

def plot_signal(signal, title):
    continuous_plot(signal, title + " - Continuous")
    discrete_plot(signal, title + " - Discrete")

def plot_two_signals(signal1, signal2) :
    plt.plot(signal1.indices, signal1.samples, label="Signal 1")

    plt.plot(signal2.indices, signal2.samples, label="Signal 2")

    plt.title("Two Signals - Continuous")
    plt.xlabel("Index")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()

    plt.stem(signal1.indices, signal1.samples, label="Signal 1")
    plt.stem(signal2.indices, signal2.samples, label="Signal 2")
    plt.title("Two Signals - Discrete")
    plt.xlabel("Index")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid()
    plt.show()