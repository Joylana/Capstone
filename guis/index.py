import tkinter as tk
from tkinter import ttk, messagebox
import math

# ── Palette ──────────────────────────────────────────────────────────────────
BG          = "#F5F4F0"        # warm off-white canvas
CARD        = "#FFFFFF"        # card surface
ACCENT      = "#2D6A4F"        # deep forest green
ACCENT_LITE = "#D8F3DC"        # pale mint
TEXT        = "#1A1A2E"        # near-black
MUTED       = "#8D99AE"        # cool grey
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

# Center window
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
    e.grid(row=row, column=1, sticky="w", padx=(0,24),
           pady=(10,0), rowspan=1 if not hint else 1)
    if hint:
        e.grid(row=row, column=1, rowspan=2, sticky="w", padx=(0,24))
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
    c.grid(row=row, column=1, sticky="w", padx=(0,24), pady=(10,0))
    if hint:
        c.grid(row=row, column=1, rowspan=2, sticky="w", padx=(0,24))
    return c

def section_divider(parent, row):
    sep = tk.Frame(parent, bg=BORDER, height=1)
    sep.grid(row=row, column=0, columnspan=2, sticky="ew",
             padx=24, pady=(14,2))

def yn_combo(parent, label, var, row):
    return labeled_combo(parent, label, var, ["No", "Yes"], row)

# ── Step management ──────────────────────────────────────────────────────────
STEPS = ["Personal", "Lifestyle", "Medical"]
current_step = tk.IntVar(value=0)

step_labels = []
step_dots   = []
connector_lines = []

def build_stepper(parent):
    frame = tk.Frame(parent, bg=CARD)
    frame.pack(fill="x", padx=0, pady=0)

    inner = tk.Frame(frame, bg=CARD)
    inner.pack(pady=(18, 6))

    for i, name in enumerate(STEPS):
        col = tk.Frame(inner, bg=CARD)
        col.grid(row=0, column=i*2, padx=0)

        dot = tk.Label(col, text=str(i+1), font=FONT_STEP,
                       bg=MUTED, fg="white",
                       width=3, relief="flat")
        dot.config(pady=4)
        dot.pack()

        lbl = tk.Label(col, text=name, font=FONT_SMALL,
                       bg=CARD, fg=MUTED)
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
            lbl.config(fg=STEP_DONE)
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

def build_page_personal(notebook):
    frame = tk.Frame(notebook, bg=CARD)

    tk.Label(frame, text="About You", font=FONT_HEAD,
             bg=CARD, fg=TEXT).grid(row=0, column=0, columnspan=2,
                                     sticky="w", padx=24, pady=(20,4))
    tk.Label(frame, text="Basic demographic and physical information",
             font=FONT_SMALL, bg=CARD, fg=MUTED).grid(
             row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0,8))

    section_divider(frame, 2)

    gender_var = make_var("Gender")
    labeled_combo(frame, "Gender", gender_var, ["Female", "Male"], 3)

    age_var = make_var("Age")
    labeled_entry(frame, "Age", age_var, 5, hint="years")

    # Height — feet + inches side by side
    feet_var   = make_var("_feet")
    inches_var = make_var("_inches")
    tk.Label(frame, text="Height", font=FONT_LABEL_B,
             bg=CARD, fg=TEXT).grid(row=7, column=0, sticky="w",
                                    padx=(24,8), pady=(10,0))
    hf = tk.Frame(frame, bg=CARD)
    hf.grid(row=7, column=1, sticky="w", padx=(0,24), pady=(10,0))
    tk.Entry(hf, textvariable=feet_var, font=FONT_ENTRY,
             bg=BG, fg=TEXT, relief="flat",
             highlightthickness=1, highlightbackground=BORDER,
             highlightcolor=ACCENT, width=5, bd=4).pack(side="left")
    tk.Label(hf, text=" ft  ", font=FONT_SMALL,
             bg=CARD, fg=MUTED).pack(side="left")
    tk.Entry(hf, textvariable=inches_var, font=FONT_ENTRY,
             bg=BG, fg=TEXT, relief="flat",
             highlightthickness=1, highlightbackground=BORDER,
             highlightcolor=ACCENT, width=5, bd=4).pack(side="left")
    tk.Label(hf, text=" in", font=FONT_SMALL,
             bg=CARD, fg=MUTED).pack(side="left")

    weight_var = make_var("Weight")
    labeled_entry(frame, "Weight", weight_var, 9, hint="pounds")

    bmi_var = make_var("BMI")
    labeled_entry(frame, "BMI", bmi_var, 11, hint="optional — leave blank to auto-calculate")

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    return frame

def build_page_lifestyle(notebook):
    frame = tk.Frame(notebook, bg=CARD)

    tk.Label(frame, text="Lifestyle Habits", font=FONT_HEAD,
             bg=CARD, fg=TEXT).grid(row=0, column=0, columnspan=2,
                                     sticky="w", padx=24, pady=(20,4))
    tk.Label(frame, text="Your daily habits and activity patterns",
             font=FONT_SMALL, bg=CARD, fg=MUTED).grid(
             row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0,8))

    section_divider(frame, 2)

    pa_var    = make_var("Physical_Activity", "Low")
    smoke_var = make_var("Smoking_Status",    "Never")
    alc_var   = make_var("Alcohol_Consumption","None")
    diet_var  = make_var("Diet",              "Average")

    labeled_combo(frame, "Physical Activity", pa_var,
                  ["Low", "Medium", "High"], 3,
                  hint="Your typical weekly exercise level")
    labeled_combo(frame, "Smoking Status", smoke_var,
                  ["Never", "Former", "Current"], 5)
    labeled_combo(frame, "Alcohol Consumption", alc_var,
                  ["None", "Moderate", "High"], 7)
    labeled_combo(frame, "Diet Quality", diet_var,
                  ["Poor", "Average", "Healthy"], 9)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    return frame

def build_page_medical(notebook):
    frame = tk.Frame(notebook, bg=CARD)

    tk.Label(frame, text="Medical History", font=FONT_HEAD,
             bg=CARD, fg=TEXT).grid(row=0, column=0, columnspan=2,
                                     sticky="w", padx=24, pady=(20,4))
    tk.Label(frame, text="Current health conditions and measurements",
             font=FONT_SMALL, bg=CARD, fg=MUTED).grid(
             row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0,8))

    section_divider(frame, 2)

    bp_var       = make_var("Blood_Pressure", "Normal")
    chol_var     = make_var("Cholesterol")
    diabetes_var = make_var("Diabetes",    "No")
    hyper_var    = make_var("Hypertension","No")
    heart_var    = make_var("Heart_Disease","No")
    asthma_var   = make_var("Asthma",      "No")

    labeled_combo(frame, "Blood Pressure", bp_var,
                  ["Low", "Normal", "High"], 3)
    labeled_entry(frame, "Cholesterol", chol_var, 5, hint="mg/dL")

    section_divider(frame, 7)

    tk.Label(frame, text="Diagnosed Conditions",
             font=("Helvetica", 9, "bold"), bg=CARD, fg=MUTED).grid(
             row=8, column=0, columnspan=2, sticky="w", padx=24, pady=(8,0))

    yn_combo(frame, "Diabetes",     diabetes_var, 9)
    yn_combo(frame, "Hypertension", hyper_var,   11)
    yn_combo(frame, "Heart Disease",heart_var,   13)
    yn_combo(frame, "Asthma",       asthma_var,  15)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    return frame

# ── Submit logic ──────────────────────────────────────────────────────────────
def do_submit():
    try:
        feet   = float(vars_["_feet"].get())   if vars_["_feet"].get()   else 0
        inches = float(vars_["_inches"].get()) if vars_["_inches"].get() else 0
        height_cm = feet * 30.48 + inches * 2.54
    except ValueError:
        height_cm = 0

    try:
        weight_kg = float(vars_["Weight"].get()) * 0.453592 if vars_["Weight"].get() else 0
    except ValueError:
        weight_kg = 0

    try:      
        bmi = float(vars_["BMI"].get()) if vars_["BMI"].get() else height_cm > 0 and weight_kg > 0 and weight_kg / (height_cm/100)**2
    except ValueError:
        bmi = 0

    data = {
        "Gender":               vars_["Gender"].get(),
        "Height":               height_cm,
        "Weight":               weight_kg,
        "BMI":                  bmi,
        "Physical_Activity":    vars_["Physical_Activity"].get(),
        "Smoking_Status":       vars_["Smoking_Status"].get(),
        "Alcohol_Consumption":  vars_["Alcohol_Consumption"].get(),
        "Diet":                 vars_["Diet"].get(),
        "Blood_Pressure":       vars_["Blood_Pressure"].get(),
        "Cholesterol":          vars_["Cholesterol"].get(),
        "Diabetes":             1 if vars_["Diabetes"].get()     == "Yes" else 0,
        "Hypertension":         1 if vars_["Hypertension"].get() == "Yes" else 0,
        "Heart_Disease":        1 if vars_["Heart_Disease"].get()== "Yes" else 0,
        "Asthma":               1 if vars_["Asthma"].get()       == "Yes" else 0,
        "Age":                  vars_["Age"].get(),
    }

    try:
        import pandas as pd # type: ignore
        from joblib import load # type: ignore

        loaded_model  = load("/Users/alanajoymorrison/Desktop/Capstone/lrmodel.joblib")
        preprocessor  = load("/Users/alanajoymorrison/Desktop/Capstone/preprocessor.joblib")
        df = pd.DataFrame([data])
        X  = preprocessor.transform(df)
        prediction = loaded_model.predict(X)

        result_val = prediction[0]
        show_result(result_val)
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

# ── Header ──
header = tk.Frame(root, bg=ACCENT, height=70)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="LifeScore", font=("Georgia", 20, "bold"),
         bg=ACCENT, fg="white").pack(side="left", padx=24, pady=14)
tk.Label(header, text="Health Assessment Tool",
         font=("Helvetica", 10), bg=ACCENT,
         fg="#A8D5BA").pack(side="left", pady=20)

# ── Card ──
card = tk.Frame(root, bg=CARD, relief="flat",
                highlightthickness=1, highlightbackground=BORDER)
card.pack(fill="both", expand=True, padx=20, pady=16)

build_stepper(card)

sep = tk.Frame(card, bg=BORDER, height=1)
sep.pack(fill="x")

# ── Page container ──
page_container = tk.Frame(card, bg=CARD)
page_container.pack(fill="both", expand=True)

p1 = build_page_personal(page_container)
p2 = build_page_lifestyle(page_container)
p3 = build_page_medical(page_container)
pages = [p1, p2, p3]
pages[0].pack(fill="both", expand=True)

# ── Nav bar ──
nav = tk.Frame(card, bg=CARD, pady=16)
nav.pack(fill="x", side="bottom")

tk.Frame(card, bg=BORDER, height=1).pack(fill="x", side="bottom")

back_btn = tk.Button(nav, text="← Back", font=FONT_BTN,
                     bg=BORDER, fg=MUTED,
                     relief="flat", padx=18, pady=9,
                     cursor="hand2", command=go_back,
                     state="disabled")
back_btn.pack(side="left", padx=24)

next_btn = tk.Button(nav, text="Continue →", font=FONT_BTN,
                     bg=ACCENT, fg="white",
                     relief="flat", padx=18, pady=9,
                     cursor="hand2", command=go_next,
                     activebackground=STEP_DONE, activeforeground="white")
next_btn.pack(side="right", padx=24)

progress_lbl = tk.Label(nav,
    text="", font=FONT_SMALL, bg=CARD, fg=MUTED)
progress_lbl.pack(side="right", padx=8)

def refresh_progress(*_):
    s = current_step.get()
    progress_lbl.config(text=f"Step {s+1} of {len(STEPS)}")

current_step.trace_add("write", refresh_progress)
refresh_progress()

root.mainloop()