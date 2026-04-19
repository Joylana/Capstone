import tkinter as tk
from tkinter import ttk, messagebox
import math

# ── Palette ──────────────────────────────────────────────────────────────────
BG          = "#F5F4F0"
CARD        = "#FFFFFF"
ACCENT      = "#2D6A4F"
ACCENT_LITE = "#D8F3DC"
TEXT        = "#1A1A2E"
MUTED       = "#8D99AE"
BORDER      = "#E0E0E0"
DANGER      = "#E63946"
STEP_DONE   = "#52B788"

FONT_TITLE  = ("Georgia", 22, "bold")
FONT_HEAD   = ("Georgia", 13, "bold")
FONT_LABEL  = ("Helvetica", 10)
FONT_LABEL_B= ("Helvetica", 10, "bold")
FONT_ENTRY  = ("Helvetica", 11)
FONT_BTN    = ("Helvetica", 11, "bold")
FONT_SMALL  = ("Helvetica", 9)
FONT_STEP   = ("Helvetica", 8, "bold")

# ── Variable storage ──────────────────────────────────────────────────────────
vars_ = {}

def make_var(name, default=""):
    v = tk.StringVar(value=default)
    vars_[name] = v
    return v

# ── App ───────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("LifeScore · Health Assessment")
root.geometry("620x700")
root.configure(bg=BG)
root.resizable(False, False)

root.update_idletasks()
x = (root.winfo_screenwidth()  - 620) // 2
y = (root.winfo_screenheight() - 700) // 2
root.geometry(f"620x700+{x}+{y}")

# ── Helper widgets ────────────────────────────────────────────────────────────
def labeled_entry(parent, label, var, row, hint="", width=22):
    tk.Label(parent, text=label, font=FONT_LABEL_B,
             bg=CARD, fg=TEXT).grid(row=row, column=0, sticky="w",
                                    padx=(24,8), pady=(10,0))
    if hint:
        tk.Label(parent, text=hint, font=FONT_SMALL,
                 bg=CARD, fg=MUTED).grid(row=row+1, column=0, sticky="w",
                                         padx=(24,8), pady=(0,2))
    e = tk.Entry(parent, textvariable=var, font=FONT_ENTRY,
                 bg=BG, fg=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT, width=width, bd=4)
    if hint:
        e.grid(row=row, column=1, rowspan=2, sticky="w", padx=(0,24))
    else:
        e.grid(row=row, column=1, sticky="w", padx=(0,24), pady=(10,0))
    return e

def labeled_combo(parent, label, var, options, row, hint="", width=20):
    tk.Label(parent, text=label, font=FONT_LABEL_B,
             bg=CARD, fg=TEXT).grid(row=row, column=0, sticky="w",
                                    padx=(24,8), pady=(10,0))
    if hint:
        tk.Label(parent, text=hint, font=FONT_SMALL,
                 bg=CARD, fg=MUTED).grid(row=row+1, column=0, sticky="w",
                                         padx=(24,8), pady=(0,2))
    style_name = f"Custom{row}.TCombobox"
    style = ttk.Style()
    style.configure(style_name, font=FONT_ENTRY,
                    fieldbackground=BG, background=BG,
                    foreground=TEXT, arrowcolor=ACCENT)
    c = ttk.Combobox(parent, textvariable=var, values=options,
                     style=style_name, width=width, state="readonly")
    if hint:
        c.grid(row=row, column=1, rowspan=2, sticky="w", padx=(0,24))
    else:
        c.grid(row=row, column=1, sticky="w", padx=(0,24), pady=(10,0))
    return c

def section_divider(parent, row):
    tk.Frame(parent, bg=BORDER, height=1).grid(
        row=row, column=0, columnspan=2, sticky="ew", padx=24, pady=(14,2))

def yn_combo(parent, label, var, row):
    return labeled_combo(parent, label, var, ["No", "Yes"], row)

# ── Unit toggle button helper ─────────────────────────────────────────────────
def unit_toggle_btn(parent, var, opt_a, opt_b, on_toggle=None):
    """A pill-style toggle between two unit options."""
    frame = tk.Frame(parent, bg=CARD)

    def make_btn(text):
        return tk.Button(frame, text=text,
                         relief="flat", bd=0, cursor="hand2",
                         font=("Helvetica", 9, "bold"),
                         padx=10, pady=3,
                         highlightthickness=0,  # removes focus ring
                         overrelief="flat")      # prevents OS hover styling

    btn_a = make_btn(opt_a)
    btn_b = make_btn(opt_b)

    def refresh():
        if var.get() == opt_a:
            btn_a.config(bg=ACCENT_LITE, fg=ACCENT)
            btn_b.config(bg="#C8CDD4",   fg=TEXT)
        else:
            btn_a.config(bg="#C8CDD4",   fg=TEXT)
            btn_b.config(bg=ACCENT_LITE, fg=ACCENT)

    def select_a():
        var.set(opt_a)
        refresh()
        if on_toggle:
            on_toggle()

    def select_b():
        var.set(opt_b)
        refresh()
        if on_toggle:
            on_toggle()

    btn_a.config(command=select_a)
    btn_b.config(command=select_b)
    btn_a.pack(side="left")
    btn_b.pack(side="left", padx=(2, 0))
    refresh()
    return frame

# ── Step management ───────────────────────────────────────────────────────────
STEPS = ["Personal", "Lifestyle", "Medical"]
current_step = tk.IntVar(value=0)
step_labels, step_dots, connector_lines = [], [], []

def build_stepper(parent):
    frame = tk.Frame(parent, bg=CARD)
    frame.pack(fill="x")
    inner = tk.Frame(frame, bg=CARD)
    inner.pack(pady=(18, 6))
    for i, name in enumerate(STEPS):
        col = tk.Frame(inner, bg=CARD)
        col.grid(row=0, column=i*2, padx=0)
        dot = tk.Label(col, text=str(i+1), font=FONT_STEP,
                       bg=MUTED, fg="white", width=3, relief="flat", pady=4)
        dot.pack()
        lbl = tk.Label(col, text=name, font=FONT_SMALL, bg=CARD, fg=MUTED)
        lbl.pack(pady=(2,0))
        step_dots.append(dot)
        step_labels.append(lbl)
        if i < len(STEPS) - 1:
            line = tk.Frame(inner, bg=BORDER, height=2, width=60)
            line.grid(row=0, column=i*2+1, sticky="n", pady=10)
            connector_lines.append(line)
    update_stepper()

def update_stepper():
    s = current_step.get()
    for i, (dot, lbl) in enumerate(zip(step_dots, step_labels)):
        if i < s:
            dot.config(bg=STEP_DONE, text="✓")
            lbl.config(fg=STEP_DONE, font=FONT_SMALL)
        elif i == s:
            dot.config(bg=ACCENT, text=str(i+1))
            lbl.config(fg=ACCENT, font=("Helvetica", 9, "bold"))
        else:
            dot.config(bg=MUTED, text=str(i+1))
            lbl.config(fg=MUTED, font=FONT_SMALL)
    for i, line in enumerate(connector_lines):
        line.config(bg=STEP_DONE if i < s else BORDER)

# ── Pages ─────────────────────────────────────────────────────────────────────
pages = []

def build_page_personal(parent):
    frame = tk.Frame(parent, bg=CARD)

    tk.Label(frame, text="About You", font=FONT_HEAD,
             bg=CARD, fg=TEXT).grid(row=0, column=0, columnspan=2,
                                    sticky="w", padx=24, pady=(20,4))
    tk.Label(frame, text="Basic demographic and physical information",
             font=FONT_SMALL, bg=CARD, fg=MUTED).grid(
             row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0,8))
    section_divider(frame, 2)

    # Gender & Age
    labeled_combo(frame, "Gender", make_var("Gender"), ["Female", "Male"], 3)
    labeled_entry(frame, "Age", make_var("Age"), 5, hint="years")

    # ── Height ────────────────────────────────────────────────────────────────
    height_unit = make_var("_height_unit", "Imperial")   # Imperial | Metric

    # widgets we'll show/hide
    height_imperial_frame = tk.Frame(frame, bg=CARD)
    height_metric_frame   = tk.Frame(frame, bg=CARD)

    feet_var   = make_var("_feet")
    inches_var = make_var("_inches")
    cm_var     = make_var("_cm")

    # Imperial: ft + in entries
    tk.Entry(height_imperial_frame, textvariable=feet_var, font=FONT_ENTRY,
             bg=BG, fg=TEXT, relief="flat", highlightthickness=1,
             highlightbackground=BORDER, highlightcolor=ACCENT,
             width=5, bd=4).pack(side="left")
    tk.Label(height_imperial_frame, text=" ft  ", font=FONT_SMALL,
             bg=CARD, fg=MUTED).pack(side="left")
    tk.Entry(height_imperial_frame, textvariable=inches_var, font=FONT_ENTRY,
             bg=BG, fg=TEXT, relief="flat", highlightthickness=1,
             highlightbackground=BORDER, highlightcolor=ACCENT,
             width=5, bd=4).pack(side="left")
    tk.Label(height_imperial_frame, text=" in", font=FONT_SMALL,
             bg=CARD, fg=MUTED).pack(side="left")

    # Metric: cm entry
    tk.Entry(height_metric_frame, textvariable=cm_var, font=FONT_ENTRY,
             bg=BG, fg=TEXT, relief="flat", highlightthickness=1,
             highlightbackground=BORDER, highlightcolor=ACCENT,
             width=8, bd=4).pack(side="left")
    tk.Label(height_metric_frame, text=" cm", font=FONT_SMALL,
             bg=CARD, fg=MUTED).pack(side="left")

    def refresh_height_ui():
        if height_unit.get() == "Imperial":
            height_metric_frame.grid_remove()
            height_imperial_frame.grid(row=7, column=1, sticky="w",
                                       padx=(0,24), pady=(10,0))
        else:
            height_imperial_frame.grid_remove()
            height_metric_frame.grid(row=7, column=1, sticky="w",
                                     padx=(0,24), pady=(10,0))

    # Label + toggle in same row via a compound frame
    height_label_frame = tk.Frame(frame, bg=CARD)
    tk.Label(height_label_frame, text="Height", font=FONT_LABEL_B,
             bg=CARD, fg=TEXT).pack(side="left")
    unit_toggle_btn(height_label_frame, height_unit,
                    "Imperial", "Metric",
                    on_toggle=refresh_height_ui).pack(side="left", padx=(10,0))

    height_label_frame.grid(row=7, column=0, sticky="w", padx=(24,8), pady=(10,0))
    height_imperial_frame.grid(row=7, column=1, sticky="w", padx=(0,24), pady=(10,0))

    # ── Weight ────────────────────────────────────────────────────────────────
    weight_unit = make_var("_weight_unit", "Imperial")   # Imperial (lbs) | Metric (kg)

    weight_imperial_var = make_var("_weight_imperial")
    weight_metric_var   = make_var("_weight_metric")

    weight_imperial_frame = tk.Frame(frame, bg=CARD)
    weight_metric_frame   = tk.Frame(frame, bg=CARD)

    tk.Entry(weight_imperial_frame, textvariable=weight_imperial_var, font=FONT_ENTRY,
             bg=BG, fg=TEXT, relief="flat", highlightthickness=1,
             highlightbackground=BORDER, highlightcolor=ACCENT,
             width=8, bd=4).pack(side="left")
    tk.Label(weight_imperial_frame, text=" lbs", font=FONT_SMALL,
             bg=CARD, fg=MUTED).pack(side="left")

    tk.Entry(weight_metric_frame, textvariable=weight_metric_var, font=FONT_ENTRY,
             bg=BG, fg=TEXT, relief="flat", highlightthickness=1,
             highlightbackground=BORDER, highlightcolor=ACCENT,
             width=8, bd=4).pack(side="left")
    tk.Label(weight_metric_frame, text=" kg", font=FONT_SMALL,
             bg=CARD, fg=MUTED).pack(side="left")

    def refresh_weight_ui():
        if weight_unit.get() == "Imperial":
            weight_metric_frame.grid_remove()
            weight_imperial_frame.grid(row=9, column=1, sticky="w",
                                       padx=(0,24), pady=(10,0))
        else:
            weight_imperial_frame.grid_remove()
            weight_metric_frame.grid(row=9, column=1, sticky="w",
                                     padx=(0,24), pady=(10,0))

    weight_label_frame = tk.Frame(frame, bg=CARD)
    tk.Label(weight_label_frame, text="Weight", font=FONT_LABEL_B,
             bg=CARD, fg=TEXT).pack(side="left")
    unit_toggle_btn(weight_label_frame, weight_unit,
                    "Imperial", "Metric",
                    on_toggle=refresh_weight_ui).pack(side="left", padx=(10,0))

    weight_label_frame.grid(row=9, column=0, sticky="w", padx=(24,8), pady=(10,0))
    weight_imperial_frame.grid(row=9, column=1, sticky="w", padx=(0,24), pady=(10,0))

    # BMI
    labeled_entry(frame, "BMI", make_var("BMI"), 11,
                  hint="optional — leave blank to auto-calculate")

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    return frame

def build_page_lifestyle(parent):
    frame = tk.Frame(parent, bg=CARD)
    tk.Label(frame, text="Lifestyle Habits", font=FONT_HEAD,
             bg=CARD, fg=TEXT).grid(row=0, column=0, columnspan=2,
                                    sticky="w", padx=24, pady=(20,4))
    tk.Label(frame, text="Your daily habits and activity patterns",
             font=FONT_SMALL, bg=CARD, fg=MUTED).grid(
             row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0,8))
    section_divider(frame, 2)
    labeled_combo(frame, "Physical Activity", make_var("Physical_Activity", "Low"),
                  ["Low", "Medium", "High"], 3, hint="Your typical weekly exercise level")
    labeled_combo(frame, "Smoking Status", make_var("Smoking_Status", "Never"),
                  ["Never", "Former", "Current"], 5)
    labeled_combo(frame, "Alcohol Consumption", make_var("Alcohol_Consumption", "None"),
                  ["None", "Moderate", "High"], 7)
    labeled_combo(frame, "Diet Quality", make_var("Diet", "Average"),
                  ["Poor", "Average", "Healthy"], 9)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    return frame

def build_page_medical(parent):
    frame = tk.Frame(parent, bg=CARD)
    tk.Label(frame, text="Medical History", font=FONT_HEAD,
             bg=CARD, fg=TEXT).grid(row=0, column=0, columnspan=2,
                                    sticky="w", padx=24, pady=(20,4))
    tk.Label(frame, text="Current health conditions and measurements",
             font=FONT_SMALL, bg=CARD, fg=MUTED).grid(
             row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0,8))
    section_divider(frame, 2)
    labeled_combo(frame, "Blood Pressure", make_var("Blood_Pressure", "Normal"),
                  ["Low", "Normal", "High"], 3)
    labeled_entry(frame, "Cholesterol", make_var("Cholesterol"), 5, hint="mg/dL")
    section_divider(frame, 7)
    tk.Label(frame, text="Diagnosed Conditions", font=("Helvetica", 9, "bold"),
             bg=CARD, fg=MUTED).grid(row=8, column=0, columnspan=2,
                                     sticky="w", padx=24, pady=(8,0))
    yn_combo(frame, "Diabetes",      make_var("Diabetes",     "No"),  9)
    yn_combo(frame, "Hypertension",  make_var("Hypertension", "No"), 11)
    yn_combo(frame, "Heart Disease", make_var("Heart_Disease","No"), 13)
    yn_combo(frame, "Asthma",        make_var("Asthma",       "No"), 15)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    return frame

# ── Submit logic ──────────────────────────────────────────────────────────────
def do_submit():
    # ── Height → cm ──────────────────────────────────────────────────────────
    try:
        if vars_["_height_unit"].get() == "Imperial":
            feet   = float(vars_["_feet"].get())   if vars_["_feet"].get()   else 0
            inches = float(vars_["_inches"].get()) if vars_["_inches"].get() else 0
            height_cm = feet * 30.48 + inches * 2.54
        else:
            height_cm = float(vars_["_cm"].get()) if vars_["_cm"].get() else 0
    except ValueError:
        height_cm = 0

    # ── Weight → kg ──────────────────────────────────────────────────────────
    try:
        if vars_["_weight_unit"].get() == "Imperial":
            raw = vars_["_weight_imperial"].get()
            weight_kg = float(raw) * 0.453592 if raw else 0
        else:
            raw = vars_["_weight_metric"].get()
            weight_kg = float(raw) if raw else 0
    except ValueError:
        weight_kg = 0

    # ── BMI ───────────────────────────────────────────────────────────────────
    try:
        bmi = float(vars_["BMI"].get()) if vars_["BMI"].get() else (
            weight_kg / (height_cm / 100) ** 2
            if height_cm > 0 and weight_kg > 0 else 0)
    except ValueError:
        bmi = 0

    data = {
        "Gender":              vars_["Gender"].get(),
        "Height":              height_cm,
        "Weight":              weight_kg,
        "BMI":                 bmi,
        "Physical_Activity":   vars_["Physical_Activity"].get(),
        "Smoking_Status":      vars_["Smoking_Status"].get(),
        "Alcohol_Consumption": vars_["Alcohol_Consumption"].get(),
        "Diet":                vars_["Diet"].get(),
        "Blood_Pressure":      vars_["Blood_Pressure"].get(),
        "Cholesterol":         vars_["Cholesterol"].get(),
        "Diabetes":            1 if vars_["Diabetes"].get()     == "Yes" else 0,
        "Hypertension":        1 if vars_["Hypertension"].get() == "Yes" else 0,
        "Heart_Disease":       1 if vars_["Heart_Disease"].get()== "Yes" else 0,
        "Asthma":              1 if vars_["Asthma"].get()       == "Yes" else 0,
        "Age":                 vars_["Age"].get(),
    }

    try:
        import pandas as pd  # type: ignore
        from joblib import load  # type: ignore
        loaded_model = load("/Users/alanajoymorrison/Desktop/Capstone/lrmodel.joblib")
        preprocessor = load("/Users/alanajoymorrison/Desktop/Capstone/preprocessor.joblib")
        df = pd.DataFrame([data])
        X  = preprocessor.transform(df)
        prediction = loaded_model.predict(X)
        show_result(prediction[0])
    except Exception as e:
        messagebox.showerror("Error", f"Could not run prediction:\n{e}")
        print(data)

def show_result(years):
    win = tk.Toplevel(root)
    win.title("Your Result")
    win.geometry("340x220")
    win.configure(bg=CARD)
    win.resizable(False, False)
    cx = root.winfo_x() + (620 - 340) // 2
    cy = root.winfo_y() + (700 - 220) // 2
    win.geometry(f"340x220+{cx}+{cy}")
    tk.Label(win, text="Predicted Life Expectancy",
             font=("Georgia", 13, "bold"), bg=CARD, fg=TEXT).pack(pady=(28,4))
    tk.Label(win, text=f"{years:.1f} years",
             font=("Georgia", 38, "bold"), bg=CARD, fg=ACCENT).pack()
    tk.Label(win, text="Based on the information you provided",
             font=FONT_SMALL, bg=CARD, fg=MUTED).pack(pady=(4,16))
    tk.Button(win, text="Close", command=win.destroy,
              font=FONT_BTN, bg=ACCENT, fg="white",
              relief="flat", padx=20, pady=8,
              cursor="hand2").pack()

# ── Navigation ────────────────────────────────────────────────────────────────
def go_next():
    s = current_step.get()
    if s < len(STEPS) - 1:
        pages[s].pack_forget()
        current_step.set(s + 1)
        pages[s + 1].pack(fill="both", expand=True)
        update_stepper()
        update_nav()
    else:
        do_submit()

def go_back():
    s = current_step.get()
    if s > 0:
        pages[s].pack_forget()
        current_step.set(s - 1)
        pages[s - 1].pack(fill="both", expand=True)
        update_stepper()
        update_nav()

def update_nav():
    s = current_step.get()
    back_btn.config(state="normal" if s > 0 else "disabled",
                    bg=BG if s > 0 else BORDER,
                    fg=TEXT if s > 0 else MUTED)
    next_btn.config(text="Submit & Calculate" if s == len(STEPS)-1 else "Continue →")

# ── Layout ────────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=ACCENT, height=70)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header, text="LifeScore", font=("Georgia", 20, "bold"),
         bg=ACCENT, fg="white").pack(side="left", padx=24, pady=14)
tk.Label(header, text="Health Assessment Tool", font=("Helvetica", 10),
         bg=ACCENT, fg="#A8D5BA").pack(side="left", pady=20)

card = tk.Frame(root, bg=CARD, relief="flat",
                highlightthickness=1, highlightbackground=BORDER)
card.pack(fill="both", expand=True, padx=20, pady=16)

build_stepper(card)
tk.Frame(card, bg=BORDER, height=1).pack(fill="x")

page_container = tk.Frame(card, bg=CARD)
page_container.pack(fill="both", expand=True)

pages = [build_page_personal(page_container),
         build_page_lifestyle(page_container),
         build_page_medical(page_container)]
pages[0].pack(fill="both", expand=True)

tk.Frame(card, bg=BORDER, height=1).pack(fill="x", side="bottom")
nav = tk.Frame(card, bg=CARD, pady=16)
nav.pack(fill="x", side="bottom")

back_btn = tk.Button(nav, text="← Back", font=FONT_BTN, bg=BORDER, fg=MUTED,
                     relief="flat", padx=18, pady=9, cursor="hand2",
                     command=go_back, state="disabled")
back_btn.pack(side="left", padx=24)

next_btn = tk.Button(nav, text="Continue →", font=FONT_BTN, bg=ACCENT, fg="white",
                     relief="flat", padx=18, pady=9, cursor="hand2", command=go_next,
                     activebackground=STEP_DONE, activeforeground="white")
next_btn.pack(side="right", padx=24)

progress_lbl = tk.Label(nav, text="", font=FONT_SMALL, bg=CARD, fg=MUTED)
progress_lbl.pack(side="right", padx=8)

def refresh_progress(*_):
    progress_lbl.config(text=f"Step {current_step.get()+1} of {len(STEPS)}")

current_step.trace_add("write", refresh_progress)
refresh_progress()

root.mainloop()