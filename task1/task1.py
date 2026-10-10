import tkinter as tk
from tkinter import filedialog, messagebox

from signal import Signal


signal1 = None
signal2 = None


def read_signal1():
    global signal1

    fileName = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if fileName:
        signal1 = Signal(fileName)
        label1.config(text="Signal 1: " + fileName)


def read_signal2():
    global signal2

    fileName = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if fileName:
        signal2 = Signal(fileName)
        label2.config(text="Signal 2: " + fileName)


def multiply_signal():
    if signal1 is None:
        messagebox.showerror("Error", "Read Signal 1 first")
        return

    try:
        const = float(const_entry.get())

        result = signal1.MultiplyByConst(const)


    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid number"
        )


def add_signals():
    if signal1 is None or signal2 is None:
        messagebox.showerror(
            "Error",
            "Read both signals first"
        )
        return

    result = signal1.AddSignals(signal2)



# ---------------- GUI ----------------

window = tk.Tk()
window.title("Signal Processing")
window.geometry("500x350")


# Signal 1
button1 = tk.Button(
    window,
    text="Read Signal 1",
    command=read_signal1
)

button1.pack(pady=10)

label1 = tk.Label(
    window,
    text="Signal 1: Not selected"
)

label1.pack()


# Signal 2
button2 = tk.Button(
    window,
    text="Read Signal 2",
    command=read_signal2
)

button2.pack(pady=10)

label2 = tk.Label(
    window,
    text="Signal 2: Not selected"
)

label2.pack()


# Constant
const_entry = tk.Entry(window)
const_entry.pack(pady=10)

const_entry.insert(0, "1")

multiply_button = tk.Button(
    window,
    text="Multiply Signal 1",
    command=multiply_signal
)

multiply_button.pack(pady=10)


# Addition
add_button = tk.Button(
    window,
    text="Add Signal 1 + Signal 2",
    command=add_signals
)

add_button.pack(pady=10)


window.mainloop()
