import tkinter as tk
#from tkinter import *
from tkinter import ttk



root=tk.Tk()
root.geometry('400x200')
root.title('User Info Form')

gender_var=tk.StringVar()
feet_var=tk.StringVar()
inches_var=tk.StringVar()

 
def submit():
    try:
        feet = float(feet_var.get()) if feet_var.get() else 0
        inches = float(inches_var.get()) if inches_var.get() else 0
        height_cm = feet * 30.48 + inches * 2.54
    except ValueError:
        height_cm = ''
    # Collect all input values
    data = {
        'Gender': gender_var.get(),
        'Height': height_cm,
        'Weight': weight_var.get(),
        'BMI': bmi_var.get(),
        'Physical_Activity': pa_var.get(),
        'Smoking_Status': smoke_var.get(),
        'Alcohol_Consumption': alc_var.get(),
        'Diet': diet_var.get(),
        'Blood_Pressure': bp_var.get(),
        'Cholesterol': chol_var.get(),
        'Diabetes': 1 if diabetes_var.get() == 'Yes' else 0,
        'Hypertension': 1 if hyper_var.get() == 'Yes' else 0,
        'Heart_Disease': 1 if heart_var.get() == 'Yes' else 0,
        'Asthma': 1 if asthma_var.get() == 'Yes' else 0,
        'Age': age_var.get()
    }
    import pandas as pd
    from joblib import load
    # Load model and preprocessor
    loaded_model = load('/Users/alanajoymorrison/Desktop/Capstone/lrmodel.joblib')
    print("model loaded...")
    preprocessor = load('/Users/alanajoymorrison/Desktop/Capstone/preprocessor.joblib')
    print("preprocessor loaded...")
    # Create DataFrame for a single row
    df = pd.DataFrame([data])
    print("data loaded...")
    # Preprocess
    X = preprocessor.transform(df)
    print("data processing...")
    # Predict
    prediction = loaded_model.predict(X)
    # Show result in popup
    from tkinter import messagebox
    messagebox.showinfo('Prediction', f'Predicted Life Expectancy: {prediction[0]:.2f}')
    # Reset fields
    gender_var.set("")
    feet_var.set("")
    inches_var.set("")
    weight_var.set("")
    bmi_var.set("")
    pa_var.set('Select')
    smoke_var.set('Select')
    alc_var.set('Select')
    diet_var.set('Select')
    bp_var.set('Select')
    chol_var.set("")
    diabetes_var.set('Select')
    hyper_var.set('Select')
    heart_var.set('Select')
    asthma_var.set('Select')
    age_var.set("")

def show():
    lbl.config(text=cb.get())
    
# creating a label for gender
# name using widget Label
gender_label = tk.Label(root, text = 'Gender', font=('calibre',10, 'bold'))

# Dropdown options  
g = ["Female", "Male"]

# Combobox  
gender_entry = ttk.Combobox(root, values=g)
gender_entry.set("Select Gender") # set the default optio
#cb.pack()
 
# creating a label for height
height_label = tk.Label(root, text = 'Height', font = ('calibre',10,'bold'))
 
# creating a entry for height
feet_entry=tk.Entry(root, textvariable = feet_var, font = ('calibre',10,'normal'))
inch_entry=tk.Entry(root, textvariable = inches_var, font = ('calibre',10,'normal'))
 
# Weight
weight_var = tk.StringVar()
weight_label = tk.Label(root, text='Weight (kg)', font=('calibre',10,'bold'))
weight_entry = tk.Entry(root, textvariable=weight_var, font=('calibre',10,'normal'))

# BMI
bmi_var = tk.StringVar()
bmi_label = tk.Label(root, text='BMI', font=('calibre',10,'bold'))
bmi_entry = tk.Entry(root, textvariable=bmi_var, font=('calibre',10,'normal'))

# Physical Activity
pa_var = tk.StringVar()
pa_label = tk.Label(root, text='Physical Activity', font=('calibre',10,'bold'))
pa_options = ['Low', 'Medium', 'High']
pa_entry = ttk.Combobox(root, values=pa_options, textvariable=pa_var)
pa_entry.set('Select')

# Smoking Status
smoke_var = tk.StringVar()
smoke_label = tk.Label(root, text='Smoking Status', font=('calibre',10,'bold'))
smoke_options = ['Never', 'Former', 'Current']
smoke_entry = ttk.Combobox(root, values=smoke_options, textvariable=smoke_var)
smoke_entry.set('Select')

# Alcohol Consumption
alc_var = tk.StringVar()
alc_label = tk.Label(root, text='Alcohol Consumption', font=('calibre',10,'bold'))
alc_options = ['None', 'Moderate', 'High']
alc_entry = ttk.Combobox(root, values=alc_options, textvariable=alc_var)
alc_entry.set('Select')

# Diet
diet_var = tk.StringVar()
diet_label = tk.Label(root, text='Diet', font=('calibre',10,'bold'))
diet_options = ['Poor', 'Average', 'Healthy']
diet_entry = ttk.Combobox(root, values=diet_options, textvariable=diet_var)
diet_entry.set('Select')

# Blood Pressure
bp_var = tk.StringVar()
bp_label = tk.Label(root, text='Blood Pressure', font=('calibre',10,'bold'))
bp_options = ['Low', 'Normal', 'High']
bp_entry = ttk.Combobox(root, values=bp_options, textvariable=bp_var)
bp_entry.set('Select')

# Cholesterol
chol_var = tk.StringVar()
chol_label = tk.Label(root, text='Cholesterol', font=('calibre',10,'bold'))
chol_entry = tk.Entry(root, textvariable=chol_var, font=('calibre',10,'normal'))

# Diabetes
diabetes_var = tk.StringVar()
diabetes_label = tk.Label(root, text='Diabetes', font=('calibre',10,'bold'))
diabetes_entry = ttk.Combobox(root, values=['No', 'Yes'], textvariable=diabetes_var)
diabetes_entry.set('Select')

# Hypertension
hyper_var = tk.StringVar()
hyper_label = tk.Label(root, text='Hypertension', font=('calibre',10,'bold'))
hyper_entry = ttk.Combobox(root, values=['No', 'Yes'], textvariable=hyper_var)
hyper_entry.set('Select')

# Heart Disease
heart_var = tk.StringVar()
heart_label = tk.Label(root, text='Heart Disease', font=('calibre',10,'bold'))
heart_entry = ttk.Combobox(root, values=['No', 'Yes'], textvariable=heart_var)
heart_entry.set('Select')

# Asthma
asthma_var = tk.StringVar()
asthma_label = tk.Label(root, text='Asthma', font=('calibre',10,'bold'))
asthma_entry = ttk.Combobox(root, values=['No', 'Yes'], textvariable=asthma_var)
asthma_entry.set('Select')

# Age
age_var = tk.StringVar()
age_label = tk.Label(root, text='Age', font=('calibre',10,'bold'))
age_entry = tk.Entry(root, textvariable=age_var, font=('calibre',10,'normal'))

# creating a button using the widget 
# Button that will call the submit function 
sub_btn=tk.Button(root,text = 'Submit', command = submit)
 
# placing the label and entry in
# the required position using grid
# method
gender_label.grid(row=0,column=0)
gender_entry.grid(row=0,column=1)
height_label.grid(row=1,column=0)
feet_entry.grid(row=1,column=1)
inch_entry.grid(row=1,column=2)
weight_label.grid(row=2,column=0)
weight_entry.grid(row=2,column=1)
bmi_label.grid(row=3,column=0)
bmi_entry.grid(row=3,column=1)
pa_label.grid(row=4,column=0)
pa_entry.grid(row=4,column=1)
smoke_label.grid(row=5,column=0)
smoke_entry.grid(row=5,column=1)
alc_label.grid(row=6,column=0)
alc_entry.grid(row=6,column=1)
diet_label.grid(row=7,column=0)
diet_entry.grid(row=7,column=1)
bp_label.grid(row=8,column=0)
bp_entry.grid(row=8,column=1)
chol_label.grid(row=9,column=0)
chol_entry.grid(row=9,column=1)
diabetes_label.grid(row=10,column=0)
diabetes_entry.grid(row=10,column=1)
hyper_label.grid(row=11,column=0)
hyper_entry.grid(row=11,column=1)
heart_label.grid(row=12,column=0)
heart_entry.grid(row=12,column=1)
asthma_label.grid(row=13,column=0)
asthma_entry.grid(row=13,column=1)
age_label.grid(row=14,column=0)
age_entry.grid(row=14,column=1)
sub_btn.grid(row=15,column=1)
 
# performing an infinite loop 
# for the window to display
root.mainloop()


