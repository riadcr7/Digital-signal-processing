import tkinter as tk
from tkinter import filedialog, messagebox

from Signal import Signal


signal1 = None
signal2 = None
signal3 = None
input1 = None
input2 = None



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
        
def read_signal3():
    global signal3

    fileName = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if fileName:
        signal3 = Signal(fileName)
        label3.config(text="Signal 3: " + fileName)

def multiply_signal1_by5():
    if signal1 is None:
        messagebox.showerror("Error", "Read Signal 1 first")
        return

    result = signal1.MultiplyByConst(5)

def multiply_signal2_by10():
    if signal2 is None:
        messagebox.showerror("Error", "Read Signal 1 first")
        return
    result = signal2.MultiplyByConst(10)

def add_signal1_signal2():
    if signal1 is None or signal2 is None:
        messagebox.showerror(
            "Error",
            "Read both signals first"
        )
        return

    result = signal1.AddSignals(signal2)
    
def add_signal1_signal3():
    if signal1 is None or signal3 is None:
        messagebox.showerror(
            "Error",
            "Read both signals first"
        )
        return

    result = signal1.AddSignals(signal3)

def sub_signal1_signal2():
    if signal1 is None or signal2 is None:
        messagebox.showerror(
            "Error",
            "Read both signals first"
        )
        return

    result = signal1.SubSignals(signal2)
    
def sub_signal1_signal3():
    if signal1 is None or signal3 is None:
        messagebox.showerror(
            "Error",
            "Read both signals first"
        )
        return

    result = signal1.SubSignals(signal3)

def squaring_signal1():
    if signal1 is None:
        messagebox.showerror(
            "Error",
            "Read Signal 1 first"
        )
        return

    result = signal1.squaringsignals()
    
def accumulation_signal1():
    if signal1 is None:
        messagebox.showerror(
            "Error",
            "Read Signal 1 first"
        )
        return

    result = signal1.accumulation()

def normalize_signal1():
    if signal1 is None:
        messagebox.showerror(
            "Error",
            "Read Signal 1 first"
        )
        return

    result = signal1.normalization_MinusOneToOne()

def normalize_signal2():
    if signal2 is None:
        messagebox.showerror(
            "Error",
            "Read Signal 2 first"
        )
        return

    result = signal2.normalization_ZeroToOne()

def read_input1():
    global input1

    fileName = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if fileName:
        input1 = Signal(fileName)
        label4.config(text="Input 1: " + fileName)

def quantize_input1():
    if input1 is None:
        messagebox.showerror(
            "Error",
            "Read Input 1 first"
        )
        return

    result = input1.quantize_1()  
    
def read_input2():
    global input2

    fileName = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if fileName:
        input2 = Signal(fileName)
        label5.config(text="Input 2: " + fileName)

def quantize_input2():
    if input2 is None:
        messagebox.showerror(
            "Error",
            "Read Input 2 first"
        )
        return

    result = input2.quantize_2()        
    
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

button1.pack(pady=5)

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

button2.pack(pady=5)

label2 = tk.Label(
    window,
    text="Signal 2: Not selected"
)

label2.pack()


# Signal 3
button3 = tk.Button(
    window,
    text="Read Signal 3",
    command=read_signal3
)

button3.pack(pady=5)

label3 = tk.Label(
    window,
    text="Signal 3: Not selected"
)

label3.pack()


# input 1
button4 = tk.Button(
    window,
    text="Read Input 1",
    command=read_input1
)

button4.pack(pady=5)

label4 = tk.Label(
    window,
    text="input 1: Not selected"
)

label4.pack()


# input 2
button5 = tk.Button(
    window,
    text="Read Input 2",
    command=read_input2
)

button5.pack(pady=5)

label5 = tk.Label(
    window,
    text="input 2: Not selected"
)

label5.pack()

# multiply signal 1 by 5
multiply_button1 = tk.Button(
    window,
    text="Multiply Signal 1 by 5",
    command=multiply_signal1_by5
)

multiply_button1.pack(pady=5)

# multiply signal 2 by 10
multiply_button2 = tk.Button(
    window,
    text="Multiply Signal 2 by 10",
    command=multiply_signal2_by10
)

multiply_button2.pack(pady=5)


# Addition signal 1 + signal 2
add_button1 = tk.Button(
    window,
    text="Add Signal 1 + Signal 2",
    command=add_signal1_signal2
)

add_button1.pack(pady=5)

# Addition signal 1 + signal 3
add_button2 = tk.Button(
    window,
    text="Add Signal 1 + Signal 3",
    command=add_signal1_signal3
)

add_button2.pack(pady=5)

# Subtraction signal 1 - signal 2
sub_button1 = tk.Button(
    window,
    text="Subtract Signal 1 - Signal 2",
    command=sub_signal1_signal2
)

sub_button1.pack(pady=5)

# Subtraction signal 1 - signal 3
sub_button2 = tk.Button(
    window,
    text="Subtract Signal 1 - Signal 3",
    command=sub_signal1_signal3
)

sub_button2.pack(pady=5)

# Squaring signal 1
squaring_button = tk.Button(
    window,
    text="Square Signal 1",
    command=squaring_signal1
)

squaring_button.pack(pady=5)

# Accumulation signal 1
accumulation_button = tk.Button(
    window,
    text="Accumulate Signal 1",
    command=accumulation_signal1
) 

accumulation_button.pack(pady=5)

# Normalization signal 1
normalize_button1 = tk.Button(
    window,
    text="Normalize Signal 1 (-1 to 1)",
    command=normalize_signal1
)

normalize_button1.pack(pady=5)

# Normalization signal 2
normalize_button2 = tk.Button(
    window,
    text="Normalize Signal 2 (0 to 1)",
    command=normalize_signal2
)

normalize_button2.pack(pady=5)

# Quantization input 1
quantize_button = tk.Button(
    window,
    text="Quantize Input 1",
    command=quantize_input1
)

quantize_button.pack(pady=5)

# Quantization input 2
quantize_button2 = tk.Button(
    window,
    text="Quantize Input 2",
    command=quantize_input2
)

quantize_button2.pack(pady=5)


window.mainloop()
