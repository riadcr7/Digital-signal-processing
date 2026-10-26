
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from Signal import Signal


# ===================== COLORS =====================

BG = "#111827"
PANEL = "#1F2937"
CARD = "#273449"
ACCENT = "#8B5CF6"
CYAN = "#06B6D4"
GREEN = "#10B981"
WHITE = "#F9FAFB"
MUTED = "#9CA3AF"


# ===================== APPLICATION =====================

class SignalProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing Studio")
        self.root.geometry("1050x680")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG)

        # Loaded signals, stored by input name
        self.signals = {}

        # Input requirements for every operation
        self.operations = {
            "Signal Operations": {
                "Multiply Signal 1 by 5": ["Signal 1"],
                "Multiply Signal 2 by 10": ["Signal 2"],
                "Add Signal 1 + Signal 2": ["Signal 1", "Signal 2"],
                "Add Signal 1 + Signal 3": ["Signal 1", "Signal 3"],
                "Subtract Signal 1 - Signal 2": ["Signal 1", "Signal 2"],
                "Subtract Signal 1 - Signal 3": ["Signal 1", "Signal 3"],
                "Square Signal 1": ["Signal 1"],
                "Accumulate Signal 1": ["Signal 1"],
                "Normalize Signal 1 (-1 to 1)": ["Signal 1"],
                "Normalize Signal 2 (0 to 1)": ["Signal 2"],
            },
            "Quantization": {
                "Quantize Signal": ["Quantization Input"],
            },
            "Frequency Operations": {
                "Calculate DFT": ["DFT Input"],
                "Calculate IDFT": ["IDFT Input"],
                "Remove DC Component": ["DC Input"],
            },
        }

        self.selected_operation = None
        self.file_labels = {}
        self.file_buttons = {}

        self.setup_styles()
        self.build_header()
        self.build_main_area()
        self.build_input_area()
        self.build_footer()

    # ===================== STYLING =====================

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TFrame",
            background=BG
        )

        style.configure(
            "Panel.TFrame",
            background=PANEL
        )

        style.configure(
            "TLabel",
            background=BG,
            foreground=WHITE,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Title.TLabel",
            background=BG,
            foreground=WHITE,
            font=("Segoe UI", 23, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background=BG,
            foreground=MUTED,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Section.TLabel",
            background=PANEL,
            foreground=WHITE,
            font=("Segoe UI", 13, "bold")
        )

        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            padding=9,
            borderwidth=0
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#7C3AED")]
        )

        style.configure(
            "Choose.TButton",
            background=CARD,
            foreground=WHITE,
            padding=6,
            borderwidth=0
        )
        style.map(
            "Choose.TButton",
            background=[("active", "#374151")]
        )

        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background=PANEL,
            foreground=WHITE,
            padding=(16, 10),
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", ACCENT)],
            foreground=[("selected", WHITE)]
        )

    # ===================== HEADER =====================

    def build_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=25, pady=(22, 15))

        ttk.Label(
            header,
            text="Signal Processing Studio",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Load your signals, choose an operation, and run it.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(5, 0))

    # ===================== MAIN AREA =====================

    def build_main_area(self):
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=25, pady=5)

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill="both", expand=True)

        self.listboxes = {}

        tab_colors = {
            "Signal Operations": ACCENT,
            "Quantization": CYAN,
            "Frequency Operations": GREEN,
        }

        for category, operations in self.operations.items():
            tab = tk.Frame(self.notebook, bg=PANEL)
            self.notebook.add(tab, text=category)

            color = tab_colors[category]

            tk.Label(
                tab,
                text=category,
                bg=PANEL,
                fg=color,
                font=("Segoe UI", 15, "bold")
            ).pack(anchor="w", padx=20, pady=(18, 5))

            tk.Label(
                tab,
                text="Select an operation from the list below.",
                bg=PANEL,
                fg=MUTED,
                font=("Segoe UI", 10)
            ).pack(anchor="w", padx=20, pady=(0, 12))

            list_frame = tk.Frame(tab, bg=CARD)
            list_frame.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=(0, 20)
            )

            scrollbar = tk.Scrollbar(list_frame)
            scrollbar.pack(side="right", fill="y")

            listbox = tk.Listbox(
                list_frame,
                bg=CARD,
                fg=WHITE,
                selectbackground=color,
                selectforeground=WHITE,
                font=("Segoe UI", 11),
                relief="flat",
                borderwidth=0,
                activestyle="none",
                highlightthickness=0,
                selectmode=tk.SINGLE,
                yscrollcommand=scrollbar.set
            )
            listbox.pack(
                side="left",
                fill="both",
                expand=True,
                padx=8,
                pady=8
            )

            scrollbar.config(command=listbox.yview)

            for operation in operations:
                listbox.insert(tk.END, operation)

            listbox.bind(
                "<<ListboxSelect>>",
                lambda event, cat=category:
                    self.on_operation_selected(cat)
            )

            self.listboxes[category] = listbox

    # ===================== INPUT AREA =====================

    def build_input_area(self):
        self.input_panel = tk.Frame(
            self.root,
            bg=PANEL,
            highlightbackground="#374151",
            highlightthickness=1
        )
        self.input_panel.pack(
            fill="x",
            padx=25,
            pady=(12, 5)
        )

        self.operation_title = tk.Label(
            self.input_panel,
            text="Choose an operation",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 13, "bold")
        )
        self.operation_title.pack(
            anchor="w",
            padx=18,
            pady=(12, 4)
        )

        self.input_description = tk.Label(
            self.input_panel,
            text="The required file inputs will appear here.",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.input_description.pack(
            anchor="w",
            padx=18,
            pady=(0, 8)
        )

        self.dynamic_inputs = tk.Frame(
            self.input_panel,
            bg=PANEL
        )
        self.dynamic_inputs.pack(
            fill="x",
            padx=18,
            pady=(0, 10)
        )

        self.run_button = ttk.Button(
            self.input_panel,
            text="Run Operation",
            style="Accent.TButton",
            command=self.run_operation,
            state="disabled"
        )
        self.run_button.pack(
            anchor="e",
            padx=18,
            pady=(0, 14)
        )

    def on_operation_selected(self, category):
        listbox = self.listboxes[category]
        selection = listbox.curselection()

        if not selection:
            return

        operation = listbox.get(selection[0])
        self.selected_operation = operation
        self.selected_category = category

        required_inputs = self.operations[category][operation]

        self.operation_title.config(text=operation)
        self.input_description.config(
            text=f"Select {len(required_inputs)} required "
                 f"signal file(s)."
        )

        # Clear the old inputs. Only show inputs for this operation.
        for widget in self.dynamic_inputs.winfo_children():
            widget.destroy()

        self.file_labels.clear()
        self.file_buttons.clear()

        for input_name in required_inputs:
            row = tk.Frame(self.dynamic_inputs, bg=PANEL)
            row.pack(fill="x", pady=4)

            tk.Label(
                row,
                text=input_name,
                width=22,
                anchor="w",
                bg=PANEL,
                fg=WHITE,
                font=("Segoe UI", 10)
            ).pack(side="left")

            label = tk.Label(
                row,
                text="No file selected",
                bg=PANEL,
                fg=MUTED,
                anchor="w",
                font=("Segoe UI", 9)
            )
            label.pack(
                side="left",
                fill="x",
                expand=True,
                padx=8
            )

            button = ttk.Button(
                row,
                text="Choose File",
                style="Choose.TButton",
                command=lambda name=input_name:
                    self.choose_file(name)
            )
            button.pack(side="right")

            self.file_labels[input_name] = label
            self.file_buttons[input_name] = button

            # Preserve the file if it was loaded earlier.
            if input_name in self.signals:
                path = self.signals[input_name]["path"]
                label.config(
                    text=Path(path).name,
                    fg=GREEN
                )

        self.run_button.config(state="normal")

    # ===================== FILE SELECTION =====================

    def choose_file(self, input_name):
        filename = filedialog.askopenfilename(
            parent=self.root,
            title=f"Choose {input_name}",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )

        if not filename:
            return

        try:
            signal = Signal(filename)
        except Exception as error:
            messagebox.showerror(
                "File Error",
                f"Could not load the signal:\n{error}",
                parent=self.root
            )
            return

        self.signals[input_name] = {
            "object": signal,
            "path": filename
        }

        self.file_labels[input_name].config(
            text=Path(filename).name,
            fg=GREEN
        )

    # ===================== RUN OPERATIONS =====================

    def run_operation(self):
        if not self.selected_operation:
            messagebox.showwarning(
                "Select Operation",
                "Choose an operation first.",
                parent=self.root
            )
            return

        required_inputs = self.operations[
            self.selected_category
        ][self.selected_operation]

        missing = [
            name for name in required_inputs
            if name not in self.signals
        ]

        if missing:
            messagebox.showerror(
                "Missing Input",
                "Please select a file for:\n"
                + "\n".join(missing),
                parent=self.root
            )
            return

        loaded = {
            name: self.signals[name]["object"]
            for name in required_inputs
        }

        operation = self.selected_operation

        # Map each GUI operation to your existing Signal methods.
        actions = {
            "Multiply Signal 1 by 5": lambda:
                loaded["Signal 1"].MultiplyByConst(5),

            "Multiply Signal 2 by 10": lambda:
                loaded["Signal 2"].MultiplyByConst(10),

            "Add Signal 1 + Signal 2": lambda:
                loaded["Signal 1"].AddSignals(
                    loaded["Signal 2"]
                ),

            "Add Signal 1 + Signal 3": lambda:
                loaded["Signal 1"].AddSignals(
                    loaded["Signal 3"]
                ),

            "Subtract Signal 1 - Signal 2": lambda:
                loaded["Signal 1"].SubSignals(
                    loaded["Signal 2"]
                ),

            "Subtract Signal 1 - Signal 3": lambda:
                loaded["Signal 1"].SubSignals(
                    loaded["Signal 3"]
                ),

            "Square Signal 1": lambda:
                loaded["Signal 1"].squaringsignals(),

            "Accumulate Signal 1": lambda:
                loaded["Signal 1"].accumulation(),

            "Normalize Signal 1 (-1 to 1)": lambda:
                loaded["Signal 1"].normalization_MinusOneToOne(),

            "Normalize Signal 2 (0 to 1)": lambda:
                loaded["Signal 2"].normalization_ZeroToOne(),

            "Quantize Signal": lambda:
                loaded["Quantization Input"].quantize(),

            "Calculate DFT": lambda:
                loaded["DFT Input"].calcDFT(),

            "Calculate IDFT": lambda:
                loaded["IDFT Input"].calcIDFT(),

            "Remove DC Component": lambda:
                loaded["DC Input"].RemoveDC(),
        }

        try:
            result = actions[operation]()

            # The Signal methods may save or plot their own results.
            # None can be a valid return value for those methods.
            messagebox.showinfo(
                "Operation Completed",
                f"{operation} finished successfully.",
                parent=self.root
            )

        except Exception as error:
            messagebox.showerror(
                "Operation Error",
                f"{operation} failed:\n{error}",
                parent=self.root
            )

    # ===================== FOOTER =====================

    def build_footer(self):
        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=25, pady=(5, 15))

        tk.Label(
            footer,
            text="DIGITAL SIGNAL PROCESSING",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(side="left")

        tk.Label(
            footer,
            text="Python • Tkinter",
            bg=BG,
            fg=CYAN,
            font=("Segoe UI", 9)
        ).pack(side="right")


# ===================== START =====================

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()
