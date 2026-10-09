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
            "Quantization"
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

        if operation == "Multiplication":
            self.constant_frame.pack(pady=5)

        elif operation == "Normalization":
            self.normalization_frame.pack(pady=5)

        elif operation == "Quantization":
            self.quantization_frame.pack(pady=5)

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
                    str(signal.indices[i])
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



root = tk.Tk()

app = SignalGUI(root)

root.mainloop()