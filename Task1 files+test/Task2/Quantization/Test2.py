from Quantization import quantize_signal
from QuanTest2 import QuantizationTest2

samples = []
with open("Quan2_input.txt", "r") as f:
    for _ in range(3):
        f.readline()
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            samples.append(float(parts[1]))

interval_indices ,quantized_vals, encoded_vals, errors = quantize_signal(samples, num_of_bits=2)
QuantizationTest2("Quan2_Out.txt",interval_indices, encoded_vals, quantized_vals,errors)