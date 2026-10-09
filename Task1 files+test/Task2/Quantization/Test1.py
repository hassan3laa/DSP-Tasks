from Quantization import quantize_signal
from QuanTest1 import QuantizationTest1

samples = []
with open("Quan1_input.txt", "r") as f:
    for _ in range(3):
        f.readline()
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            samples.append(float(parts[1]))

interval_indices ,quantized_vals, encoded_vals, errors = quantize_signal(samples, num_of_bits=3)
QuantizationTest1("Quan1_Out.txt", encoded_vals, quantized_vals)