
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import cmath
import math

from Signal import Signal
from test import ReadSignalFile

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ===================== COLORS =====================

BG = "#111827"
PANEL = "#1F2937"
CARD = "#273449"
PURPLE = "#8B5CF6"
CYAN = "#06B6D4"
GREEN = "#10B981"
WHITE = "#F9FAFB"
MUTED = "#9CA3AF"


class SignalProcessingApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Processing Studio")
        self.root.geometry("1200x850")
        self.root.minsize(950, 700)
        self.root.configure(bg=BG)

        self.signals = {}
        self.selected_operation = None
        self.selected_category = None

        self.fs_var = tk.StringVar(value="1000")
        self.frequency_var = tk.StringVar()
        self.amplitude_var = tk.StringVar()
        self.phase_var = tk.StringVar()

        self.original_samples = []
        self.sample_indices = []
        self.coefficients = []
        self.original_coefficients = []
        self.frequencies = []
        self.normalized_amplitudes = []
        self.phases = []

        self.reconstructed_samples = []
        self.dc_removed = False

        # Mouse interaction state
        self.dragging_point = None

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
            "DFT / IDFT / Remove DC": {
                "Analyze Fourier Transform": ["DFT Input"],
                "Calculate IDFT": ["IDFT Input"],
                "Remove DC Component": ["DC Input"],
            },
        }

        # Build the GUI first
        self.setup_styles()
        self.build_header()
        self.build_tabs()
        self.build_operation_panel()
        self.build_footer()



    # ===================== STYLES =====================

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background=PANEL,
            foreground=WHITE,
            padding=(14, 9),
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", PURPLE)],
            foreground=[("selected", WHITE)]
        )

        style.configure(
            "Accent.TButton",
            background=PURPLE,
            foreground=WHITE,
            padding=8,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#7C3AED")]
        )

        style.configure(
            "Secondary.TButton",
            background=CARD,
            foreground=WHITE,
            padding=6,
            borderwidth=0
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#374151")]
        )

        style.configure(
            "Treeview",
            background=CARD,
            foreground=WHITE,
            fieldbackground=CARD,
            rowheight=25,
            font=("Segoe UI", 9)
        )
        style.configure(
            "Treeview.Heading",
            background=PANEL,
            foreground=CYAN,
            font=("Segoe UI", 9, "bold")
        )
        style.map(
            "Treeview",
            background=[("selected", PURPLE)]
        )

    # ===================== HEADER =====================

    def build_header(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=22, pady=(16, 10))

        tk.Label(
            header,
            text="Signal Processing Studio",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Signal operations • Quantization • Fourier analysis",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

    # ===================== TABS =====================

    def build_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=5
        )

        self.listboxes = {}

        colors = {
            "Signal Operations": PURPLE,
            "Quantization": CYAN,
            "DFT / IDFT / Remove DC": GREEN,
        }

        for category, operations in self.operations.items():
            tab = tk.Frame(self.notebook, bg=PANEL)
            self.notebook.add(tab, text=category)

            tk.Label(
                tab,
                text=category,
                bg=PANEL,
                fg=colors[category],
                font=("Segoe UI", 14, "bold")
            ).pack(anchor="w", padx=18, pady=(14, 4))

            tk.Label(
                tab,
                text="Select an operation.",
                bg=PANEL,
                fg=MUTED
            ).pack(anchor="w", padx=18, pady=(0, 10))

            frame = tk.Frame(tab, bg=CARD)
            frame.pack(
                fill="both",
                expand=True,
                padx=18,
                pady=(0, 18)
            )

            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side="right", fill="y")

            lb = tk.Listbox(
                frame,
                bg=CARD,
                fg=WHITE,
                selectbackground=colors[category],
                selectforeground=WHITE,
                font=("Segoe UI", 11),
                activestyle="none",
                highlightthickness=0,
                relief="flat",
                yscrollcommand=scrollbar.set
            )
            lb.pack(
                side="left",
                fill="both",
                expand=True,
                padx=8,
                pady=8
            )
            scrollbar.config(command=lb.yview)

            for operation in operations:
                lb.insert(tk.END, operation)

            lb.bind(
                "<<ListboxSelect>>",
                lambda event, cat=category:
                    self.select_operation(cat)
            )

            self.listboxes[category] = lb

    # ===================== OPERATION PANEL =====================

    def build_operation_panel(self):
        self.op_panel = tk.Frame(self.root, bg=PANEL)
        self.op_panel.pack(
            fill="x",
            padx=22,
            pady=(8, 5)
        )

        self.op_title = tk.Label(
            self.op_panel,
            text="Choose an operation",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 13, "bold")
        )
        self.op_title.pack(anchor="w", padx=15, pady=(10, 3))

        self.input_frame = tk.Frame(self.op_panel, bg=PANEL)
        self.input_frame.pack(fill="x", padx=15, pady=5)

        self.run_button = ttk.Button(
            self.op_panel,
            text="Run Operation",
            style="Accent.TButton",
            command=self.run_operation
        )
        self.run_button.pack(anchor="e", padx=15, pady=(0, 10))

    def select_operation(self, category):
        lb = self.listboxes[category]
        selection = lb.curselection()

        if not selection:
            return

        self.selected_category = category
        self.selected_operation = lb.get(selection[0])

        self.op_title.config(text=self.selected_operation)

        for widget in self.input_frame.winfo_children():
            widget.destroy()

        required = self.operations[category][self.selected_operation]

        for name in required:
            row = tk.Frame(self.input_frame, bg=PANEL)
            row.pack(fill="x", pady=3)

            tk.Label(
                row,
                text=name,
                width=20,
                anchor="w",
                bg=PANEL,
                fg=WHITE
            ).pack(side="left")

            existing = self.signals.get(name)
            label = tk.Label(
                row,
                text=Path(existing["path"]).name
                if existing else "No file selected",
                bg=PANEL,
                fg=GREEN if existing else MUTED
            )
            label.pack(side="left", padx=8, fill="x", expand=True)

            ttk.Button(
                row,
                text="Choose File",
                style="Secondary.TButton",
                command=lambda n=name, l=label: self.choose_file(n, l)
            ).pack(side="right")

        if self.selected_operation == "Analyze Fourier Transform":
            self.add_sampling_frequency()

        if self.selected_operation in (
            "Calculate IDFT", "Remove DC Component"
        ):
            tk.Label(
                self.input_frame,
                text="These operations also run the corresponding Signal "
                     "class test functions.",
                bg=PANEL,
                fg=MUTED,
                wraplength=700,
                justify="left"
            ).pack(anchor="w", pady=5)

    def add_sampling_frequency(self):
        row = tk.Frame(self.input_frame, bg=PANEL)
        row.pack(fill="x", pady=5)

        tk.Label(
            row,
            text="Sampling frequency (Hz)",
            bg=PANEL,
            fg=CYAN,
            width=23,
            anchor="w"
        ).pack(side="left")

        tk.Entry(
            row,
            textvariable=self.fs_var,
            bg=CARD,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            width=15
        ).pack(side="left", padx=8)

    # ===================== FILE LOADING =====================

    def choose_file(self, name, label):
        filename = filedialog.askopenfilename(
            title=f"Choose {name}",
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
            messagebox.showerror("File Error", str(error))
            return

        self.signals[name] = {
            "object": signal,
            "path": filename
        }

        label.config(text=Path(filename).name, fg=GREEN)

    # ===================== RUN OPERATIONS =====================

    def run_operation(self):
        if not self.selected_operation:
            return

        required = self.operations[
            self.selected_category
        ][self.selected_operation]

        missing = [n for n in required if n not in self.signals]

        if missing:
            messagebox.showerror(
                "Missing Inputs",
                "Choose a file for:\n" + "\n".join(missing)
            )
            return

        operation = self.selected_operation
        loaded = {
            name: self.signals[name]["object"]
            for name in required
        }

        try:
            if operation == "Analyze Fourier Transform":
                self.analyze_fourier(
                    self.signals["DFT Input"]["path"]
                )
                return

            if operation == "Calculate IDFT":
                result = loaded["IDFT Input"].calcIDFT()
                self.show_result(
                    "IDFT",
                    result,
                    self.signals["IDFT Input"]["path"]
                )
                return

            if operation == "Remove DC Component":
                result = loaded["DC Input"].RemoveDC()
                self.show_result(
                    "DC-removed signal",
                    result,
                    self.signals["DC Input"]["path"]
                )
                return

            actions = {
                "Multiply Signal 1 by 5":
                    lambda: loaded["Signal 1"].MultiplyByConst(5),

                "Multiply Signal 2 by 10":
                    lambda: loaded["Signal 2"].MultiplyByConst(10),

                "Add Signal 1 + Signal 2":
                    lambda: loaded["Signal 1"].AddSignals(loaded["Signal 2"]),

                "Add Signal 1 + Signal 3":
                    lambda: loaded["Signal 1"].AddSignals(loaded["Signal 3"]),

                "Subtract Signal 1 - Signal 2":
                    lambda: loaded["Signal 1"].SubSignals(loaded["Signal 2"]),

                "Subtract Signal 1 - Signal 3":
                    lambda: loaded["Signal 1"].SubSignals(loaded["Signal 3"]),

                "Square Signal 1":
                    lambda: loaded["Signal 1"].squaringsignals(),

                "Accumulate Signal 1":
                    lambda: loaded["Signal 1"].accumulation(),

                "Normalize Signal 1 (-1 to 1)":
                    lambda: loaded["Signal 1"].normalization_MinusOneToOne(),

                "Normalize Signal 2 (0 to 1)":
                    lambda: loaded["Signal 2"].normalization_ZeroToOne(),

                "Quantize Signal":
                    lambda: loaded["Quantization Input"].quantize(),
            }

            actions[operation]()

            messagebox.showinfo(
                "Completed",
                f"{operation} completed.\n"
                "Check your Signal method for its output."
            )

        except Exception as error:
            messagebox.showerror(
                "Operation Error",
                f"{operation} failed:\n{error}"
            )

    # ===================== FOURIER ANALYSIS =====================

    def analyze_fourier(self, filename):
        try:
            fs = float(self.fs_var.get())

            if not math.isfinite(fs) or fs <= 0:
                raise ValueError(
                    "Sampling frequency must be a positive number."
                )

            indices, samples = ReadSignalFile(filename)

            if len(samples) == 0:
                raise ValueError("The signal contains no samples.")

            self.sample_indices = list(indices)
            self.original_samples = [float(x) for x in samples]

            # calcDFT also runs your assignment's existing test.
            signal_object = self.signals["DFT Input"]["object"]
            self.coefficients = signal_object.calcDFT()

            if len(self.coefficients) != len(self.original_samples):
                raise ValueError(
                    "The DFT coefficient count does not match the sample count."
                )

            self.original_coefficients = list(self.coefficients)
            self.dc_removed = False

            N = len(self.coefficients)

            # Full DFT bins: appropriate for editing all complex coefficients.
            # Fundamental angular frequency (rad/s)
            self.fundamental_frequency = (2 * math.pi * fs) / N

            # Angular frequency of each DFT component (rad/s)
            self.frequencies = [
                k * self.fundamental_frequency
                for k in range(N)
            ]

            raw_amplitudes = [
                abs(x) for x in self.coefficients
            ]

            max_amplitude = max(raw_amplitudes, default=0)

            if max_amplitude == 0:
                self.normalized_amplitudes = [0.0] * N
            else:
                self.normalized_amplitudes = [
                    a / max_amplitude for a in raw_amplitudes
                ]

            self.phases = [
                cmath.phase(x) for x in self.coefficients
            ]

            self.show_fourier_window()

        except Exception as error:
            messagebox.showerror(
                "Fourier Analysis Error",
                str(error)
            )

    # ===================== FOURIER WINDOW =====================

    def show_fourier_window(self):
        win = tk.Toplevel(self.root)
        win.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.close_fourier_window(win)
        )
        win.title("Fourier Transform Studio")
        win.geometry("1150x850")
        win.configure(bg=BG)

        tk.Label(
            win,
            text="Fourier Transform Studio",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w", padx=18, pady=(15, 3))

        tk.Label(
            win,
            text=f"Sampling frequency: {self.fs_var.get()} Hz  |  "
                 f"Samples: {len(self.original_samples)}",
            bg=BG,
            fg=CYAN
        ).pack(anchor="w", padx=18, pady=(0, 10))

        # Two dot plots
        fig = Figure(figsize=(10, 4.5), dpi=100)
        fig.patch.set_facecolor(PANEL)

        self.ax_amp = fig.add_subplot(121)
        self.ax_phase = fig.add_subplot(122)

        self.ax_amp.set_facecolor(CARD)
        self.ax_phase.set_facecolor(CARD)

        self.canvas = FigureCanvasTkAgg(fig, master=win)
        
        # Connect mouse events after the canvas has been created
        
        self.canvas.mpl_connect(
            "pick_event", self.on_point_pick
        )
        self.canvas.mpl_connect(
            "motion_notify_event", self.on_point_drag
        )
        self.canvas.mpl_connect(
            "button_release_event", self.on_point_release
        )
        
        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=12,
            pady=8
        )

        self.fig = fig
        self.refresh_plots()

        # Dominant frequency list
        dominant_frame = tk.Frame(win, bg=PANEL)
        dominant_frame.pack(fill="x", padx=12, pady=5)

        tk.Label(
            dominant_frame,
            text="Dominant frequencies (normalized amplitude > 0.5)",
            bg=PANEL,
            fg=GREEN,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=10, pady=7)

        self.dominant_label = tk.Label(
            dominant_frame,
            text="",
            bg=PANEL,
            fg=WHITE,
            justify="left",
            anchor="w",
            wraplength=1000
        )
        self.dominant_label.pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )

        self.update_dominant_frequencies()

        # Component editing
        editor = tk.Frame(win, bg=PANEL)
        editor.pack(fill="x", padx=12, pady=5)

        tk.Label(
            editor,
            text="Edit a Fourier component",
            bg=PANEL,
            fg=CYAN,
            font=("Segoe UI", 11, "bold")
        ).grid(row=0, column=0, columnspan=6, sticky="w",
               padx=10, pady=8)

        tk.Label(
            editor, text="Bin index", bg=PANEL, fg=WHITE
        ).grid(row=1, column=0, padx=8, pady=5)

        self.bin_box = ttk.Combobox(
            editor,
            width=10,
            state="readonly",
            values=list(range(len(self.coefficients)))
        )
        self.bin_box.grid(row=1, column=1, padx=5, pady=5)
        self.bin_box.bind("<<ComboboxSelected>>", self.load_component)

        tk.Label(
            editor, text="Amplitude", bg=PANEL, fg=WHITE
        ).grid(row=1, column=2, padx=8, pady=5)

        tk.Entry(
            editor,
            textvariable=self.amplitude_var,
            width=14
        ).grid(row=1, column=3, padx=5, pady=5)

        tk.Label(
            editor, text="Phase (radians)", bg=PANEL, fg=WHITE
        ).grid(row=1, column=4, padx=8, pady=5)

        tk.Entry(
            editor,
            textvariable=self.phase_var,
            width=14
        ).grid(row=1, column=5, padx=5, pady=5)

        buttons = tk.Frame(win, bg=BG)
        buttons.pack(fill="x", padx=12, pady=8)

        ttk.Button(
            buttons,
            text="Apply Component Changes",
            style="Accent.TButton",
            command=self.apply_component
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons,
            text="Remove DC (X[0] = 0)",
            style="Secondary.TButton",
            command=self.remove_dc_gui
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons,
            text="Reconstruct with IDFT",
            style="Accent.TButton",
            command=self.reconstruct_gui
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons,
            text="Save Reconstructed Signal",
            style="Secondary.TButton",
            command=self.save_reconstructed
        ).pack(side="left", padx=4)

        if self.coefficients:
            self.bin_box.current(0)
            self.load_component()
            
    def close_fourier_window(self, win):
        try:
            if win.winfo_exists():
                win.destroy()
        except tk.TclError:
            pass

        self.dragging_point = None

    # ===================== PLOT UPDATES =====================
    
    def on_point_pick(self, event):
        if event.artist == self.amp_scatter:
            plot_type = "amplitude"
        elif event.artist == self.phase_scatter:
            plot_type = "phase"
        else:
            return

        if len(event.ind) > 0:
            self.dragging_point = (plot_type, int(event.ind[0]))

    
    def on_point_drag(self, event):
        if self.dragging_point is None or event.ydata is None:
            return

        plot_type, k = self.dragging_point
        ax = self.ax_amp if plot_type == "amplitude" else self.ax_phase

        if event.inaxes != ax:
            return

        N = len(self.coefficients)
        if N == 0:
            return

        partner = (-k) % N
        coefficient = self.coefficients[k]
        magnitude = abs(coefficient)
        phase = cmath.phase(coefficient)

        if plot_type == "amplitude":
            maximum = max(abs(c) for c in self.coefficients)

            if maximum == 0:
                return

            new_magnitude = max(0.0, min(1.0, event.ydata)) * maximum

            if partner == k:
                sign = -1 if coefficient.real < 0 else 1
                self.coefficients[k] = complex(sign * new_magnitude, 0)
            else:
                self.coefficients[k] = cmath.rect(new_magnitude, phase)
                self.coefficients[partner] = self.coefficients[k].conjugate()

        else:
            new_phase = max(-math.pi, min(math.pi, event.ydata))

            if partner == k:
                # DC and Nyquist coefficients must be real.
                sign = -1 if math.cos(new_phase) < 0 else 1
                self.coefficients[k] = complex(sign * magnitude, 0)
            else:
                self.coefficients[k] = cmath.rect(magnitude, new_phase)
                self.coefficients[partner] = self.coefficients[k].conjugate()

        self.refresh_plots()

    
    def on_point_release(self, event):
        self.dragging_point = None
    
    def refresh_plots(self):
        frequencies = self.frequencies
        amplitudes = [abs(c) for c in self.coefficients]

        maximum = max(amplitudes, default=0)
        normalized = (
            [a / maximum for a in amplitudes]
            if maximum > 0 else [0.0] * len(amplitudes)
        )
        phases = [cmath.phase(c) for c in self.coefficients]

        self.normalized_amplitudes = normalized
        self.phases = phases

        self.ax_amp.clear()
        self.ax_phase.clear()

        self.amp_scatter = self.ax_amp.scatter(
            frequencies, normalized,
            color="#06B6D4", s=35, picker=5
        )
        self.ax_amp.axhline(
            0.5, color="#F59E0B", linestyle="--", linewidth=1
        )
        self.ax_amp.set_title(
            "Angular Frequency vs Normalized Amplitude", color=WHITE
        )
        self.ax_amp.set_xlabel("Angular Frequency (rad/s)", color=WHITE)
        self.ax_amp.set_ylabel("Normalized Amplitude", color=WHITE)
        self.ax_amp.set_ylim(-0.05, 1.05)

        self.phase_scatter = self.ax_phase.scatter(
            frequencies, phases,
            color="#A78BFA", s=35, picker=5
        )
        self.ax_phase.set_title(
            "Angular Frequency vs Phase", color=WHITE
        )
        self.ax_phase.set_xlabel("Angular Frequency (rad/s)", color=WHITE)
        self.ax_phase.set_ylabel("Phase (radians)", color=WHITE)
        self.ax_phase.set_ylim(-math.pi - 0.1, math.pi + 0.1)

        for ax in (self.ax_amp, self.ax_phase):
            ax.tick_params(colors=WHITE)
            ax.xaxis.label.set_color(WHITE)
            ax.yaxis.label.set_color(WHITE)
            ax.title.set_color(WHITE)
            ax.grid(True, alpha=0.2)

            for spine in ax.spines.values():
                spine.set_color(MUTED)

        self.fig.tight_layout()
        self.canvas.draw_idle()

        if hasattr(self, "dominant_label"):
            self.update_dominant_frequencies()



    def update_dominant_frequencies(self):
        dominant = [
            f"{self.frequencies[k]:.4f} rad/s "
            f"(normalized amplitude {self.normalized_amplitudes[k]:.3f})"
            for k in range(len(self.coefficients))
            if self.normalized_amplitudes[k] > 0.5
        ]

        if (
            getattr(self, "dominant_label", None) is not None
            and self.dominant_label.winfo_exists()
        ):
            self.dominant_label.config(
                text="\n".join(dominant)
                if dominant
                else "No frequency bins have normalized amplitude > 0.5."
            )

    # ===================== EDIT COMPONENTS =====================

    def load_component(self, event=None):
        selection = self.bin_box.get()

        if not selection:
            return

        k = int(selection)
        coefficient = self.coefficients[k]

        self.amplitude_var.set(f"{abs(coefficient):.8f}")
        self.phase_var.set(f"{cmath.phase(coefficient):.8f}")

    def apply_component(self):
        try:
            if not self.bin_box.get():
                raise ValueError("Select a frequency bin first.")

            k = int(self.bin_box.get())
            amplitude = float(self.amplitude_var.get())
            phase = float(self.phase_var.get())

            if not math.isfinite(amplitude) or amplitude < 0:
                raise ValueError("Amplitude must be finite and non-negative.")

            if not math.isfinite(phase):
                raise ValueError("Phase must be a finite number.")

            # Editing uses actual coefficient magnitude, not normalized display.
            # If applying an amplitude change:
            self.update_coefficient_with_symmetry(
                k, magnitude=amplitude
            )

            # If applying a phase change:
            self.update_coefficient_with_symmetry(
                k, phase=phase
            )

            self.refresh_plots()
            self.load_component()

        except Exception as error:
            messagebox.showerror("Invalid Component", str(error))

    # ===================== DC REMOVAL =====================

    def remove_dc_gui(self):
        if not self.coefficients:
            return

        # Zero-frequency component is the first DFT coefficient.
        self.coefficients[0] = 0j
        self.dc_removed = True

        self.refresh_plots()

        messagebox.showinfo(
            "DC Removed",
            "The zero-frequency Fourier coefficient X[0] has been set to zero."
        )

    # ===================== RECONSTRUCTION =====================

    def reconstruct_gui(self):
        try:
            N = len(self.coefficients)

            if N == 0:
                raise ValueError("No Fourier coefficients are available.")

            result = []

            for n in range(N):
                sample = 0j

                for k in range(N):
                    sample += self.coefficients[k] * cmath.exp(
                        2j * math.pi * k * n / N
                    )

                result.append(sample.real / N)

            self.reconstructed_samples = result

            # Display the reconstructed time-domain signal.
            self.show_result(
                "Reconstructed Signal",
                result,
                None
            )

        except Exception as error:
            messagebox.showerror("IDFT Error", str(error))

    def show_result(self, title, samples, source_path=None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("850x500")
        win.configure(bg=BG)

        fig = Figure(figsize=(8, 4), dpi=100)
        fig.patch.set_facecolor(PANEL)

        ax = fig.add_subplot(111)
        ax.set_facecolor(CARD)

        ax.scatter(
            range(len(samples)),
            samples,
            color="#06B6D4",
            s=24
        )

        ax.set_title(title, color=WHITE)
        ax.set_xlabel("Sample index", color=WHITE)
        ax.set_ylabel("Amplitude", color=WHITE)
        ax.tick_params(colors=WHITE)
        ax.grid(True, alpha=0.2)

        for spine in ax.spines.values():
            spine.set_color(MUTED)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )
        canvas.draw()

        tk.Button(
            win,
            text="Save Result",
            bg=PURPLE,
            fg=WHITE,
            relief="flat",
            command=lambda: self.save_samples(samples, title)
        ).pack(pady=(0, 10))

    def save_reconstructed(self):
        if not self.reconstructed_samples:
            messagebox.showwarning(
                "No Reconstruction",
                "Run IDFT reconstruction first."
            )
            return

        self.save_samples(
            self.reconstructed_samples,
            "Reconstructed Signal"
        )

    def save_samples(self, samples, title):
        filename = filedialog.asksaveasfilename(
            title="Save Signal",
            defaultextension=".txt",
            initialfile=title.lower().replace(" ", "_") + ".txt",
            filetypes=[("Text files", "*.txt")]
        )

        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write("0\n0\n")
                file.write(f"{len(samples)}\n")

                for i, sample in enumerate(samples):
                    file.write(f"{i} {sample:.10f}\n")

            messagebox.showinfo(
                "Saved",
                f"Result saved to:\n{filename}"
            )

        except Exception as error:
            messagebox.showerror("Save Error", str(error))

    # ===================== FOOTER =====================

    def build_footer(self):
        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=22, pady=(4, 12))

        tk.Label(
            footer,
            text="DIGITAL SIGNAL PROCESSING",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(side="left")

        tk.Label(
            footer,
            text="Python • Tkinter • Matplotlib",
            bg=BG,
            fg=CYAN
        ).pack(side="right")
        
        
    def update_coefficient_with_symmetry(self, k, magnitude=None, phase=None):
        N = len(self.coefficients)
        if N == 0 or not (0 <= k < N):
            return

        partner = (-k) % N
        current = self.coefficients[k]

        new_magnitude = abs(current) if magnitude is None else max(0.0, magnitude)
        new_phase = cmath.phase(current) if phase is None else phase

        if partner == k:
            # DC and Nyquist bins must be real for a real-valued signal.
            real_value = new_magnitude * math.cos(new_phase)
            self.coefficients[k] = complex(real_value, 0.0)
        else:
            self.coefficients[k] = cmath.rect(new_magnitude, new_phase)
            self.coefficients[partner] = self.coefficients[k].conjugate()

        self.refresh_plots()



if __name__ == "__main__":
    root = tk.Tk()
    app = SignalProcessingApp(root)
    root.mainloop()
