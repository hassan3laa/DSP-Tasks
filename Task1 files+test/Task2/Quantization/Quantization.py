import numpy as np
import math

from signal_model import Signal

#Quantization steps: ha5od mn el user el number of bits aw number of levels, number of levels (L)=2(power)(number of bits (b))
#Get min and max, delta = (max-min)/number of levels
#Make our ranges, starting from min and adding k every time until we reach the max
#midpoint of each range = (start+end)/2 w di el bn3ml assign 3ndha

def quantize_signal(signals, num_of_levels=None, num_of_bits=None):
    if num_of_bits is not None:
        num_of_levels=2**num_of_bits
    elif num_of_levels is not None:
        num_of_bits=math.ceil(math.log2(num_of_levels))
    else:
        print("Invalid number of levels/bits")

    signals=np.array(signals,dtype=float)
    range_min=signals.min()
    range_max=signals.max()

    d=(range_max-range_min)/num_of_levels #delta

    midpoints=[]
    binary_codes = []

    for i in range(num_of_levels):
        q_i = round(range_min + (i + 0.5) * d, 3)
        midpoints.append(q_i)
        binary_codes.append(format(i, f'0{num_of_bits}b'))

    interval_indices = []
    quantized_signals = []
    encoded_signals = []
    quantization_errors = []

    for x in signals:
        k = int((x - range_min) / d)

        if k >= num_of_levels:
            k = num_of_levels - 1

        q_val = midpoints[k]
        code = binary_codes[k]
        err = round(q_val - x, 3)

        interval_indices.append(k + 1)
        quantized_signals.append(q_val)
        encoded_signals.append(code)
        quantization_errors.append(err)

    return  interval_indices,quantized_signals,encoded_signals, quantization_errors