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

def plot_quantization(indices, original, quantized, errors):
    fig, axes = plt.subplots(2, 1, figsize=(9, 7))

    # Original signal and quantized signal
    axes[0].stem(
        indices,
        original,
        linefmt="b-",
        markerfmt="bo",
        basefmt="k-",
        label="Original Signal"
    )

    axes[0].step(
        indices,
        quantized,
        where="mid",
        color="red",
        label="Quantized Signal"
    )

    axes[0].set_title("Original vs Quantized Signal")
    axes[0].set_xlabel("Sample Index")
    axes[0].set_ylabel("Amplitude")
    axes[0].legend()
    axes[0].grid(True)

    # Quantization error
    axes[1].stem(
        indices,
        errors,
        linefmt="g-",
        markerfmt="go",
        basefmt="k-"
    )

    axes[1].set_title("Quantization Error")
    axes[1].set_xlabel("Sample Index")
    axes[1].set_ylabel("Error")
    axes[1].grid(True)

    fig.tight_layout()
    plt.show()