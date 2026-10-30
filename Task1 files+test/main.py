import os
import tkinter as tk
from tkinter import filedialog, messagebox

from core.reader import *
from core.operations import *
from core.plot import *
from core.writer import *
from Task1.Task1Test import *

from Task2.Quantization.Quantization import quantize_signal
from Task2.Quantization.QuanTest1 import QuantizationTest1
from Task2.Quantization.QuanTest2 import QuantizationTest2

import sys
from docx import Document

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Task4", "Test Cases"))

from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift


from Task5.Shifting_and_Folding.Shift_Fold_Signal import Shift_Fold_Signal




def read_amp_phase(path):
    if path.endswith(".docx"):
        lines = [p.text for p in Document(path).paragraphs]
    else:
        lines = open(path).read().splitlines()

    amps, phases = [], []
    for line in lines[3:]:
        parts = line.replace("f", "").split()
        if len(parts) == 2:
            amps.append(float(parts[0]))
            phases.append(float(parts[1]))
    return amps, phases

class SignalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing Framework")
        self.root.geometry("600x500")

        self.signal_paths = []

        title = tk.Label(
            root,
            text="Signal Processing Framework",
            font=("Arial", 18)
        )
        title.pack(pady=20)

        number_frame = tk.Frame(root)
        number_frame.pack(pady=10)

        tk.Label(
            number_frame,
            text="Number of Signals:"
        ).pack(side=tk.LEFT)

        self.number_entry = tk.Entry(number_frame, width=10)
        self.number_entry.pack(side=tk.LEFT, padx=10)

        tk.Button(
            number_frame,
            text="Set",
            command=self.set_number_of_signals
        ).pack(side=tk.LEFT)

        self.signals_frame = tk.Frame(root)
        self.signals_frame.pack(pady=10)

        operation_frame = tk.Frame(root)
        operation_frame.pack(pady=15)

        tk.Label(
            operation_frame,
            text="Operation:"
        ).pack(side=tk.LEFT)

        self.operation = tk.StringVar()
        self.operation.set("Display Signal")

        operations = [
            "Display Signal",
            "Display Two Signals",
            "Addition",
            "Subtraction",
            "Multiplication",
            "Squaring",
            "Normalization",
            "Accumulation",
            "Quantization",
            "DFT",
            "IDFT",
            "Modify Components",
            "Remove DC Component",
            "First Derivative",
            "Second Derivative",
            "Moving Average",
            "Folding",
            "Shifting and Folding",
            "Delay/Advance Folded Signal",
            "Remove DC (Time Domain)"

        ]

        self.operation_menu = tk.OptionMenu(
            operation_frame,
            self.operation,
            *operations,
            command=self.operation_changed
        )

        self.operation_menu.pack(side=tk.LEFT, padx=10)

        self.constant_frame = tk.Frame(root)

        tk.Label(
            self.constant_frame,
            text="Constant:"
        ).pack(side=tk.LEFT)

        self.constant_entry = tk.Entry(
            self.constant_frame,
            width=10
        )

        self.constant_entry.pack(side=tk.LEFT, padx=10)

        self.normalization_frame = tk.Frame(root)

        tk.Label(
            self.normalization_frame,
            text="Normalization:"
        ).pack(side=tk.LEFT)

        self.normalization_option = tk.StringVar()
        self.normalization_option.set("-1 to 1")

        normalization_options = [
            "-1 to 1",
            "0 to 1"
        ]

        tk.OptionMenu(
            self.normalization_frame,
            self.normalization_option,
            *normalization_options
        ).pack(side=tk.LEFT, padx=10)

        self.quantization_frame = tk.Frame(root)

        tk.Label(
            self.quantization_frame,
            text="Choose:"
        ).pack(side=tk.LEFT)

        self.quantization_type = tk.StringVar()
        self.quantization_type.set("Number of Bits")

        tk.OptionMenu(
            self.quantization_frame,
            self.quantization_type,
            "Number of Bits",
            "Number of Levels"
        ).pack(side=tk.LEFT, padx=5)

        self.quantization_entry = tk.Entry(
            self.quantization_frame,
            width=10
        )

        self.quantization_entry.pack(side=tk.LEFT, padx=5)

        self.sampling_frame = tk.Frame(root)

        tk.Label(
            self.sampling_frame,
            text="Sampling Frequency (Hz):"
        ).pack(side=tk.LEFT)

        self.sampling_entry = tk.Entry(
            self.sampling_frame,
            width=10
        )
        self.sampling_entry.pack(side=tk.LEFT, padx=5)

        self.modify_frame = tk.Frame(root)

        tk.Label(self.modify_frame, text="Index k:").pack(side=tk.LEFT)
        self.index_entry = tk.Entry(self.modify_frame, width=6)
        self.index_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.modify_frame, text="New Amplitude:").pack(side=tk.LEFT)
        self.new_amp_entry = tk.Entry(self.modify_frame, width=8)
        self.new_amp_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.modify_frame, text="New Phase (rad):").pack(side=tk.LEFT)
        self.new_phase_entry = tk.Entry(self.modify_frame, width=8)
        self.new_phase_entry.pack(side=tk.LEFT, padx=5)

        self.moving_average_frame = tk.Frame(root)

        tk.Label(
            self.moving_average_frame,
            text="Window Size:"
        ).pack(side=tk.LEFT)

        self.window_size_entry = tk.Entry(
            self.moving_average_frame,
            width=10
        )
        self.window_size_entry.pack(side=tk.LEFT, padx=10)

        self.shift_frame = tk.Frame(root)

        tk.Label(
            self.shift_frame,
            text="Shift Amount:"
        ).pack(side=tk.LEFT)

        self.shift_entry = tk.Entry(
            self.shift_frame,
            width=10
        )
        self.shift_entry.pack(side=tk.LEFT, padx=10)

        self.delay_frame = tk.Frame(root)

        self.delay_direction = tk.StringVar()
        self.delay_direction.set("Delay")

        tk.OptionMenu(
            self.delay_frame,
            self.delay_direction,
            "Delay",
            "Advance"
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            self.delay_frame,
            text="By (samples):"
        ).pack(side=tk.LEFT)

        self.delay_entry = tk.Entry(
            self.delay_frame,
            width=10
        )
        self.delay_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            root,
            text="Execute",
            command=self.execute,
            width=15
        ).pack(pady=25)

    def set_number_of_signals(self):
        try:
            number = int(self.number_entry.get())

            if number <= 0:
                messagebox.showerror("Error","Number of signals must be greater than 0.")
                return

        except ValueError:
            messagebox.showerror("Error","Please enter a valid number.")
            return

        for widget in self.signals_frame.winfo_children():
            widget.destroy()

        self.signal_paths = []

        for i in range(number):
            frame = tk.Frame(self.signals_frame)
            frame.pack(pady=5)

            tk.Label(
                frame,
                text="Signal " + str(i + 1) + ":"
            ).pack(side=tk.LEFT)

            path_label = tk.Label(
                frame,
                text="No file selected",
                width=30,
                anchor="w"
            )

            path_label.pack(side=tk.LEFT, padx=10)

            tk.Button(
                frame,
                text="Browse",
                command=lambda index=i, label=path_label:
                self.choose_file(index, label)
            ).pack(side=tk.LEFT)

            self.signal_paths.append("")

    def choose_file(self, index, label):
        file_path = filedialog.askopenfilename(
            title="Select Signal File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.signal_paths[index] = file_path

            file_name = file_path.split("/")[-1]
            label.config(text=file_name)

    def operation_changed(self, operation):
        self.constant_frame.pack_forget()
        self.normalization_frame.pack_forget()
        self.quantization_frame.pack_forget()
        self.sampling_frame.pack_forget()
        self.modify_frame.pack_forget()
        self.moving_average_frame.pack_forget()
        self.shift_frame.pack_forget()
        self.shift_frame.pack_forget()
        self.delay_frame.pack_forget()

        if operation == "Multiplication":
            self.constant_frame.pack(pady=5)

        elif operation == "Normalization":
            self.normalization_frame.pack(pady=5)

        elif operation == "Quantization":
            self.quantization_frame.pack(pady=5)

        elif operation == "DFT":
            self.sampling_frame.pack(pady=5)

        elif operation == "Modify Components":
            self.sampling_frame.pack(pady=5)
            self.modify_frame.pack(pady=5)

        elif operation == "Moving Average":
            self.moving_average_frame.pack(pady=5)

        elif operation == "Shifting and Folding":
            self.shift_frame.pack(pady=5)

        elif operation == "Shifting and Folding":
            self.shift_frame.pack(pady=5)

        elif operation == "Delay/Advance Folded Signal":
            self.delay_frame.pack(pady=5)

    def execute(self):
        operation = self.operation.get()

        if operation == "Display Signal":
            self.display_signal()

        elif operation == "Display Two Signals":
            self.display_two_signals()

        elif operation == "Addition":
            self.addition()

        elif operation == "Subtraction":
            self.subtraction()

        elif operation == "Multiplication":
            self.multiplication()

        elif operation == "Squaring":
            self.squaring()

        elif operation == "Normalization":
            self.normalization()

        elif operation == "Accumulation":
            self.accumulation()

        elif operation == "Quantization":
            self.quantization()

        elif operation == "DFT":
            self.dft()

        elif operation == "IDFT":
            self.idft()

        elif operation == "Modify Components":
            self.modify_components()

        elif operation == "Remove DC Component":
            self.remove_DC_component()

        elif operation == "First Derivative":
            self.first_derivative()

        elif operation == "Second Derivative":
            self.second_derivative()

        elif operation == "Moving Average":
            self.moving_average()

        elif operation == "Folding":
            self.shifting_and_folding(fold_only=True)

        elif operation == "Shifting and Folding":
            self.shifting_and_folding(fold_only=False)

        elif operation == "Delay/Advance Folded Signal":
            self.delay_advance_folded()

        elif operation == "Remove DC (Time Domain)":
            self.remove_dc_time_domain()

    def display_signal(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror("Error","Please set the number of signals to 1.")
            return

        if self.signal_paths[0] == "":
            messagebox.showerror("Error","Please select a signal file.")
            return

        signal = read_signal(self.signal_paths[0])

        plot_signal(signal,"Signal")

    def display_two_signals(self):
        if len(self.signal_paths) != 2:
            messagebox.showerror("Error","Please set the number of signals to 2.")
            return

        if self.signal_paths[0] == "" or self.signal_paths[1] == "":
            messagebox.showerror("Error","Please select both signal files.")
            return

        signal1 = read_signal(self.signal_paths[0])

        signal2 = read_signal(self.signal_paths[1])

        plot_two_signals(signal1,signal2)

    def addition(self):
        if len(self.signal_paths) == 0:
            messagebox.showerror("Error","Please set the number of signals.")
            return

        signals = []

        for path in self.signal_paths:
            if path == "":
                messagebox.showerror("Error","Please select all signal files.")
                return

            signals.append(read_signal(path))

        result = add_signals(signals)

        if result is None:
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Addition Result",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if output_path:
            write_signal(result,output_path)
            AddSignalSamplesAreEqual(
                os.path.basename(self.signal_paths[0]),
                os.path.basename(self.signal_paths[1]),
                result.indices,
                result.samples
            )

        plot_signal(
            result,
            "Addition Result"
        )

    def subtraction(self):
        if len(self.signal_paths) == 0:
            messagebox.showerror("Error", "Please set the number of signals.")
            return

        signals = []

        for path in self.signal_paths:
            if path == "":
                messagebox.showerror("Error", "Please select all signal files.")
                return

            signals.append(read_signal(path))

        result = subtract_signals(signals)

        if os.path.basename(self.signal_paths[1]) == "signal3.txt":
            expected_file = os.path.join(
                "Task2",
                "OUTPUT Arithmetic operations",
                "signal1-signal3.txt"
            )
        else:
            expected_file = os.path.join(
                "Task2",
                "OUTPUT Arithmetic operations",
                "signal1-signal2.txt"
            )

        SignalSamplesAreEqual(
            "Subtraction",
            expected_file,
            result.indices,
            result.samples
        )

        if result is None:
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Subtraction Result",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(
            result,
            "Subtraction Result"
        )

    def multiplication(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if self.signal_paths[0] == "":
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        try:
            constant = float(
                self.constant_entry.get()
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid constant."
            )
            return

        signal = read_signal(
            self.signal_paths[0]
        )

        result = multiply_signal(
            signal,
            constant
        )

        output_path = filedialog.asksaveasfilename(
            title="Save Multiplication Result",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if output_path:
            write_signal(result,output_path)
            MultiplySignalByConst(
                constant,
                result.indices,
                result.samples
            )

        plot_signal(
            result,
            "Multiplication Result"
        )

    def squaring(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if self.signal_paths[0] == "":
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        signal = read_signal(self.signal_paths[0])

        result = square_signal(signal)

        SignalSamplesAreEqual("Squaring",
                              os.path.join(
                                  "Task2",
                                  "OUTPUT Arithmetic operations",
                                  "Output squaring signal 1.txt"),
                              result.indices, result.samples)

        output_path = filedialog.asksaveasfilename(
            title="Save Squaring Result",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(
            result,
            "Squaring Result"
        )


    def normalization(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if self.signal_paths[0] == "":
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        signal = read_signal(self.signal_paths[0])

        option = self.normalization_option.get()

        result = normalize_signal(signal, option)

        if option == "-1 to 1":
            expected_file = os.path.join(
                "Task2",
                "OUTPUT Arithmetic operations",
                "normalize of signal 1 (from -1 to 1)-- output.txt"
            )
        else:
            expected_file = os.path.join(
                "Task2",
                "OUTPUT Arithmetic operations",
                "normlize signal 2 (from 0 to 1 )-- output.txt"
            )

        SignalSamplesAreEqual(
            "Normalization " + option,
            expected_file,
            result.indices,
            result.samples
        )

        output_path = filedialog.asksaveasfilename(
            title="Save Normalization Result",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(
            result,
            "Normalization Result"
        )

    def accumulation(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if self.signal_paths[0] == "":
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        signal = read_signal(self.signal_paths[0])

        result = accumulate_signal(signal)

        SignalSamplesAreEqual("Accumulation",
                              os.path.join(
                                  "Task2",
                                  "OUTPUT Arithmetic operations",
                                  "output accumulation for signal1.txt"
                              ),
                              result.indices,
                              result.samples
                              )

        output_path = filedialog.asksaveasfilename(
            title="Save Accumulation Result",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(
            result,
            "Accumulation Result"
        )

    def quantization(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if self.signal_paths[0] == "":
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        try:
            number = int(self.quantization_entry.get())

            if number <= 0:
                messagebox.showerror(
                    "Error",
                    "Number must be greater than 0."
                )
                return

            if (
                    self.quantization_type.get() == "Number of Bits"
                    and number > 16
            ):
                messagebox.showerror(
                    "Error",
                    "Please enter a reasonable number of bits."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid integer."
            )
            return

        signal = read_signal(self.signal_paths[0])

        if not signal.samples:
            messagebox.showerror(
                "Error",
                "The selected signal has no samples."
            )
            return

        if self.quantization_type.get() == "Number of Bits":
            interval_indices, quantized_values, encoded_values, errors = (
                quantize_signal(
                    signal.samples,
                    num_of_bits=number
                )
            )
        else:
            interval_indices, quantized_values, encoded_values, errors = (
                quantize_signal(
                    signal.samples,
                    num_of_levels=number
                )
            )

        input_name = os.path.basename(self.signal_paths[0])

        test_folder = os.path.join(
            os.path.dirname(__file__),
            "Task2",
            "Quantization"
        )

        if input_name == "Quan1_input.txt" and number == 3 and self.quantization_type.get() == "Number of Bits":
            QuantizationTest1(
                os.path.join(test_folder, "Quan1_Out.txt"),
                encoded_values,
                quantized_values
            )

        elif input_name == "Quan2_input.txt" and (
                (
                        self.quantization_type.get() == "Number of Bits"
                        and number == 2
                )
                or
                (
                        self.quantization_type.get() == "Number of Levels"
                        and number == 4
                )
        ):
            QuantizationTest2(
                os.path.join(test_folder, "Quan2_Out.txt"),
                interval_indices,
                encoded_values,
                quantized_values,
                errors
            )

        plot_quantization(
            signal.indices,
            signal.samples,
            quantized_values,
            errors
        )

        result_text = "Index | Encoded | Quantized | Error\n\n"

        for i in range(len(signal.samples)):
            result_text += (
                    str(interval_indices[i])
                    + " | "
                    + str(encoded_values[i])
                    + " | "
                    + str(quantized_values[i])
                    + " | "
                    + str(errors[i])
                    + "\n"
            )

        messagebox.showinfo(
            "Quantization Result",
            result_text
        )

    def dft(self):
        if len(self.signal_paths) != 1 or not self.signal_paths[0]:
            messagebox.showerror("Error", "Please select one signal file.")
            return

        try:
            sampling_frequency = float(self.sampling_entry.get())

            if sampling_frequency <= 0:
                raise ValueError

            signal = read_signal(self.signal_paths[0])

            if signal.signal_type != 0:
                messagebox.showerror(
                    "Error",
                    "DFT requires a time-domain signal."
                )
                return

            frequencies, amplitudes, phases = dft(
                signal, sampling_frequency
            )

            normalized_amplitudes = normalize_amplitudes(amplitudes)

            dominant = get_dominant_frequencies(frequencies, normalized_amplitudes)

            output_path = filedialog.asksaveasfilename(
                title="Save DFT Result",
                defaultextension=".txt",
                filetypes=[
                    ("Text Files", "*.txt")
                ]
            )

            if output_path:
                with open(output_path, "w") as f:
                    f.write("1\n0\n" + str(len(amplitudes)) + "\n")
                    for a, p in zip(amplitudes, phases):
                        f.write(f"{a} {p}\n")

                if os.path.basename(self.signal_paths[0]) == "input_Signal_DFT.txt":
                    expected = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "Task4", "Test Cases", "DFT", "Output_Signal_DFT_A,Phase.docx"
                    )
                    my_amps, my_phases = read_amp_phase(output_path)
                    exp_amps, exp_phases = read_amp_phase(expected)

                    if SignalComapreAmplitude(my_amps, exp_amps) and SignalComaprePhaseShift(my_phases, exp_phases):
                        messagebox.showinfo("DFT Test", "DFT Test case passed successfully")
                    else:
                        messagebox.showerror("DFT Test", "DFT Test case failed")

            plot_dft(frequencies, normalized_amplitudes, phases)

            messagebox.showinfo(
                "Dominant Frequencies",
                "Frequencies above 0.5 normalized amplitude:\n"
                + (
                    "\n".join(f"{frequency:.3f} Hz" for frequency in dominant)
                    if dominant else "No dominant frequencies found."
                )
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid positive sampling frequency."
            )

    def modify_components(self):
        if len(self.signal_paths) != 1 or not self.signal_paths[0]:
            messagebox.showerror("Error", "Please select one signal file.")
            return

        try:
            sampling_frequency = float(self.sampling_entry.get())
            k = int(self.index_entry.get())

            new_amplitude = None
            if self.new_amp_entry.get().strip() != "":
                new_amplitude = float(self.new_amp_entry.get())

            new_phase = None
            if self.new_phase_entry.get().strip() != "":
                new_phase = float(self.new_phase_entry.get())

            signal = read_signal(self.signal_paths[0])
            frequencies, amplitudes, phases = dft(signal, sampling_frequency)

            amplitudes, phases = modify_component(
                amplitudes, phases, k, new_amplitude, new_phase
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid sampling frequency, component index and values."
            )
            return

        result = Signal(1, signal.is_periodic, len(amplitudes))
        result.frequencies = frequencies
        result.amplitudes = amplitudes
        result.phases = phases

        output_path = filedialog.asksaveasfilename(
            title="Save Modified Components",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if output_path:
            write_signal(result, output_path)

        plot_dft(frequencies, normalize_amplitudes(amplitudes), phases)

    def remove_DC_component(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if self.signal_paths[0] == "":
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        signal = read_signal(self.signal_paths[0])

        if not signal.samples:
            messagebox.showerror(
                "Error",
                "The selected signal has no samples."
            )
            return

        result = remove_DC_component(signal)

        output_path = filedialog.asksaveasfilename(
            title="Save DC Removal Result",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(
            result,
            "DC Component Removed"
        )

    def idft(self):
        if len(self.signal_paths) != 1 or not self.signal_paths[0]:
            messagebox.showerror("Error", "Please select one signal file.")
            return

        file_path = self.signal_paths[0]

        file_path = self.signal_paths[0]

        try:
            amps, phases = read_amp_phase(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read the file: {e}")
            return

        if not amps:
            messagebox.showerror("Error", "No amplitude/phase data found in the file.")
            return

        try:
            reconstructed = idft(amps, phases)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compute IDFT: {e}")
            return

        indices = list(range(len(reconstructed)))
        result_signal = Signal(0, 0, len(reconstructed))
        result_signal.indices = indices
        result_signal.samples = reconstructed

        output_path = filedialog.asksaveasfilename(
            title="Save IDFT Result",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if output_path:
            write_signal(result_signal, output_path)

            expected_txt = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "Task4", "Test Cases", "IDFT", "Output_Signal_IDFT.txt"
            )
            if os.path.exists(expected_txt):
                SignalSamplesAreEqual("IDFT", expected_txt, indices, reconstructed)

        plot_signal(result_signal, "Reconstructed Time-Domain Signal (IDFT)")

    def first_derivative(self):
        if len(self.signal_paths) != 1 or not self.signal_paths[0]:
            messagebox.showerror("Error", "Please select one signal file.")
            return

        signal = read_signal(self.signal_paths[0])

        if signal.n < 2:
            messagebox.showerror("Error", "Signal must have at least 2 samples.")
            return

        result = calculate_first_derivative(signal)

        plot_signal(result, "First Derivative")

        output_path = filedialog.asksaveasfilename(
            title="Save First Derivative",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if output_path:
            write_signal(result, output_path)

    def second_derivative(self):
        if len(self.signal_paths) != 1 or not self.signal_paths[0]:
            messagebox.showerror("Error", "Please select one signal file.")
            return

        signal = read_signal(self.signal_paths[0])

        if signal.n < 3:
            messagebox.showerror("Error", "Signal must have at least 3 samples.")
            return

        result = calculate_second_derivative(signal)

        plot_signal(result, "Second Derivative")

        output_path = filedialog.asksaveasfilename(
            title="Save Second Derivative",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if output_path:
            write_signal(result, output_path)

    def moving_average(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if self.signal_paths[0] == "":
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        try:
            window_size = int(self.window_size_entry.get())

            signal = read_signal(self.signal_paths[0])
            result = moving_average(signal, window_size)

        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        output_path = filedialog.asksaveasfilename(
            title="Save Moving Average Result",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(result, "Moving Average Result")

    def shifting_and_folding(self, fold_only=False):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if not self.signal_paths[0]:
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        try:
            signal = read_signal(self.signal_paths[0])

            if not signal.samples:
                raise ValueError("The selected signal has no samples.")

            result = fold_signal(signal)

            if fold_only:
                expected_file = os.path.join(
                    os.path.dirname(__file__),
                    "Task5",
                    "Shifting_and_Folding",
                    "Output_fold.txt"
                )
                title = "Folding Result"

            else:
                shift_amount = int(self.shift_entry.get())
                result = shift_signal(result, shift_amount)

                expected_files = {
                    500: "Output_ShifFoldedby500.txt",
                    -500: "Output_ShiftFoldedby-500.txt"
                }

                if shift_amount in expected_files:
                    expected_file = os.path.join(
                        os.path.dirname(__file__),
                        "Task5",
                        "Shifting_and_Folding",
                        expected_files[shift_amount]
                    )
                else:
                    expected_file = None

                title = "Shifting and Folding Result"

        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return

        if expected_file is not None:
            try:
                Shift_Fold_Signal(
                    expected_file,
                    result.indices,
                    result.samples
                )
            except (OSError, ValueError) as error:
                print(f"Could not run Shift/Fold test: {error}")
        else:
            print(
                "No expected output file for this shift amount. "
                "The result was not compared."
            )

        output_path = filedialog.asksaveasfilename(
            title=f"Save {title}",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(result, title)

    def delay_advance_folded(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if not self.signal_paths[0]:
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        try:
            amount = int(self.delay_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid integer amount."
            )
            return

        if amount < 0:
            messagebox.showerror(
                "Error",
                "The amount must be zero or positive."
            )
            return

        signal = read_signal(self.signal_paths[0])

        if not signal.samples:
            messagebox.showerror(
                "Error",
                "The selected signal has no samples."
            )
            return

        if self.delay_direction.get() == "Delay":
            shift_amount = amount
        else:
            shift_amount = -amount

        result = shift_folded_signal(signal, shift_amount)

        output_path = filedialog.asksaveasfilename(
            title="Save Delayed/Advanced Folded Signal",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(
            result,
            self.delay_direction.get() + "ed Folded Signal"
            if self.delay_direction.get() == "Delay"
            else "Advanced Folded Signal"
        )

    def remove_dc_time_domain(self):
        if len(self.signal_paths) != 1:
            messagebox.showerror(
                "Error",
                "Please set the number of signals to 1."
            )
            return

        if not self.signal_paths[0]:
            messagebox.showerror(
                "Error",
                "Please select a signal file."
            )
            return

        signal = read_signal(self.signal_paths[0])

        if not signal.samples:
            messagebox.showerror(
                "Error",
                "The selected signal has no samples."
            )
            return

        result = remove_dc_time_domain(signal)

        output_path = filedialog.asksaveasfilename(
            title="Save DC Removal Result (Time Domain)",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if output_path:
            write_signal(result, output_path)

        plot_signal(
            result,
            "DC Removed (Time Domain)"
        )


root = tk.Tk()

app = SignalGUI(root)

root.mainloop()