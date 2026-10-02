def write_signal(signal, filepath):
    with open(filepath, "w") as file:
        file.write(str(signal.signal_type) + "\n")
        file.write(str(signal.is_periodic) + "\n")
        file.write(str(signal.n) + "\n")

        if signal.signal_type == 0:
            for i in range(signal.n):
                file.write(
                    str(signal.indices[i]) + " " +
                    format(signal.samples[i], "g") + "\n"
                )
        else:
            for i in range(signal.n):
                file.write(
                    format(signal.frequencies[i], "g") + " " +
                    format(signal.amplitudes[i], "g") + " " +
                    format(signal.phases[i], "g") + "\n"
                )