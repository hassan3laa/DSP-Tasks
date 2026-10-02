import tkinter as tk
from tkinter import filedialog, messagebox

from reader import *
from operations import *
from plot import *
from writer import *


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
            "Multiplication"
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
        if operation == "Multiplication":
            self.constant_frame.pack(pady=5)
        else:
            self.constant_frame.pack_forget()

    def execute(self):
        operation = self.operation.get()

        if operation == "Display Signal":
            self.display_signal()

        elif operation == "Display Two Signals":
            self.display_two_signals()

        elif operation == "Addition":
            self.addition()

        elif operation == "Multiplication":
            self.multiplication()

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
            write_signal(
                result,
                output_path
            )

        plot_signal(
            result,
            "Addition Result"
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
            write_signal(
                result,
                output_path
            )

        plot_signal(
            result,
            "Multiplication Result"
        )


root = tk.Tk()

app = SignalGUI(root)

root.mainloop()