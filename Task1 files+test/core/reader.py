from .signal_model import Signal


def read_signal(file_path):
    with open(file_path, "r") as file:
        signal_type = int(file.readline())
        is_periodic = int(file.readline())
        n = int(file.readline())

        signal = Signal(signal_type, is_periodic, n)

        for i in range(n):
            data = file.readline().split()

            if signal_type == 0:
                signal.indices.append(int(data[0]))
                signal.samples.append(float(data[1]))
            else:
                signal.frequencies.append(float(data[0]))
                signal.amplitudes.append(float(data[1]))
                signal.phases.append(float(data[2]))

        return signal