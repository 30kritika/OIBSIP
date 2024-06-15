import tkinter as tk

class BMICalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("BMI Calculator")

        self.height_label = tk.Label(text="Enter your height in meters:")
        self.height_entry = tk.Entry()
        self.weight_label = tk.Label(text="Enter your weight in kilograms:")
        self.weight_entry = tk.Entry()

        self.calculate_button = tk.Button(text="Calculate BMI", command=self.calculate_bmi)

        self.bmi_label = tk.Label(text="")

        self.height_label.grid(row=0, column=0)
        self.height_entry.grid(row=0, column=1)
        self.weight_label.grid(row=1, column=0)
        self.weight_entry.grid(row=1, column=1)
        self.calculate_button.grid(row=2, column=0, columnspan=2)  
        self.bmi_label.grid(row=3, column=0, columnspan=2) 
    def calculate_bmi(self):
        try:
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())

            if height <= 0 or weight <= 0:
                self.bmi_label.config(text="Height and weight must be positive values.")
                return

            bmi = weight / (height ** 2)

            self.bmi_label.config(text=f"Your BMI is {bmi:.2f}")
        except ValueError:
            
            self.bmi_label.config(text="Please enter valid numbers for height and weight.")

bmi_calculator = BMICalculator()
bmi_calculator.window.mainloop()
