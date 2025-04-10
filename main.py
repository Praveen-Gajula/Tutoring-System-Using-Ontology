import tkinter as tk
from math import gcd
from functools import reduce

class RationalToolApp:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("Rational Number Tool")
        self.root_window.geometry("800x600")
        self.root_window.configure(bg="white")
        
        self.build_interface()

    def build_interface(self):
        # Main title
        title_lbl = tk.Label(self.root_window, text="Rational Number Tool", 
                             font=("Helvetica", 24, "bold"), bg="white", fg="darkred")
        title_lbl.pack(pady=20)

        # Container for selecting the number of fractions
        count_container = tk.Frame(self.root_window, bg="white")
        count_container.pack(pady=10)
        tk.Label(count_container, text="Number of Rational Numbers:", 
                 font=("Helvetica", 14), bg="white").grid(row=0, column=0, padx=10)
        self.fraction_count_var = tk.StringVar(value="2")
        count_menu = tk.OptionMenu(count_container, self.fraction_count_var, *[str(i) for i in range(2, 8)],
                                   command=self.refresh_inputs)
        count_menu.config(font=("Helvetica", 12))
        count_menu.grid(row=0, column=1, padx=10)

        # Container for selecting the arithmetic operation
        op_container = tk.Frame(self.root_window, bg="white")
        op_container.pack(pady=10)
        tk.Label(op_container, text="Select Operation:", 
                 font=("Helvetica", 14), bg="white").grid(row=0, column=0, padx=10)
        self.operation_var = tk.StringVar(value="Add")
        op_menu = tk.OptionMenu(op_container, self.operation_var, "Add", "Subtract", "Multiply", "Divide")
        op_menu.config(font=("Helvetica", 12))
        op_menu.grid(row=0, column=1, padx=10)

        # Container for rational number input rows
        self.input_container = tk.Frame(self.root_window, bg="white")
        self.input_container.pack(pady=20)
        self.refresh_inputs()

        # Label to display the built equation
        self.equation_lbl = tk.Label(self.root_window, text="Equation:", 
                                     font=("Helvetica", 14), bg="white", fg="green", wraplength=700)
        self.equation_lbl.pack(pady=10)

        # Label to show the computed outcome
        self.outcome_lbl = tk.Label(self.root_window, text="Outcome:", 
                                    font=("Helvetica", 14), bg="white", fg="black", wraplength=700)
        self.outcome_lbl.pack(pady=10)

        # Button to initiate the computation
        compute_btn = tk.Button(self.root_window, text="Compute Result", 
                                font=("Helvetica", 14, "bold"), bg="darkred", fg="white",
                                command=self.compute_result)
        compute_btn.pack(pady=10)

        # Footer label
        footer_lbl = tk.Label(self.root_window, text="Crafted with precision", 
                              font=("Helvetica", 10), bg="white", fg="gray")
        footer_lbl.pack(side="bottom", pady=20)

    def refresh_inputs(self, *args):
        # Remove existing input rows
        for widget in self.input_container.winfo_children():
            widget.destroy()

        self.input_rows = []
        num_rows = int(self.fraction_count_var.get())
        for idx in range(num_rows):
            row_frame = tk.Frame(self.input_container, bg="white")
            row_frame.pack(pady=5)
            prompt_lbl = tk.Label(row_frame, text=f"Rational #{idx+1}:", 
                                  font=("Helvetica", 12), bg="white", width=15, anchor="e")
            prompt_lbl.pack(side="left", padx=10)
            numer_entry = tk.Entry(row_frame, font=("Helvetica", 12), width=7)
            numer_entry.pack(side="left")
            slash_lbl = tk.Label(row_frame, text="/", font=("Helvetica", 12), bg="white")
            slash_lbl.pack(side="left")
            denom_entry = tk.Entry(row_frame, font=("Helvetica", 12), width=7)
            denom_entry.pack(side="left")
            self.input_rows.append((numer_entry, denom_entry))

    def compute_result(self):
        try:
            fractions_list = []
            # Read input rational numbers
            for num_entry, denom_entry in self.input_rows:
                num_val = int(num_entry.get())
                denom_val = int(denom_entry.get())
                if denom_val == 0:
                    raise ValueError("Denominator cannot be zero.")
                fractions_list.append((num_val, denom_val))
            
            # Build equation string based on chosen operation
            op_choice = self.operation_var.get()
            eq_str = self.build_equation(fractions_list, op_choice)
            self.equation_lbl.config(text=f"Equation: {eq_str}")
            
            # Process the arithmetic and update outcome label
            result = self.process_arithmetic(fractions_list, op_choice)
            self.outcome_lbl.config(text=f"Outcome: {result[0]}/{result[1]}")
        except Exception as error:
            self.outcome_lbl.config(text=f"Error: {error}")

    def build_equation(self, fraction_data, op_text):
        # Map operation to symbol
        op_symbols = {
            "Add": "+",
            "Subtract": "-",
            "Multiply": "×",
            "Divide": "÷"
        }
        symbol = op_symbols.get(op_text, "?")
        parts = [f"({n}/{d})" for n, d in fraction_data]
        return f" {symbol} ".join(parts)

    def process_arithmetic(self, fraction_data, op_text):
        if op_text == "Add":
            return self.add_rationals(fraction_data)
        elif op_text == "Subtract":
            return self.subtract_rationals(fraction_data)
        elif op_text == "Multiply":
            return self.multiply_rationals(fraction_data)
        elif op_text == "Divide":
            return self.divide_rationals(fraction_data)
        else:
            raise ValueError("Invalid operation selected.")

    def add_rationals(self, fraction_data):
        common_denom = 1
        for _, d in fraction_data:
            common_denom = self.compute_lcm(common_denom, d)
        sum_numer = sum(n * (common_denom // d) for n, d in fraction_data)
        return self.simplify_rational(sum_numer, common_denom)

    def subtract_rationals(self, fraction_data):
        common_denom = 1
        for _, d in fraction_data:
            common_denom = self.compute_lcm(common_denom, d)
        initial = fraction_data[0]
        diff_numer = initial[0] * (common_denom // initial[1])
        for n, d in fraction_data[1:]:
            diff_numer -= n * (common_denom // d)
        return self.simplify_rational(diff_numer, common_denom)

    def multiply_rationals(self, fraction_data):
        prod_numer = 1
        prod_denom = 1
        for n, d in fraction_data:
            prod_numer *= n
            prod_denom *= d
        return self.simplify_rational(prod_numer, prod_denom)

    def divide_rationals(self, fraction_data):
        quot_numer, quot_denom = fraction_data[0]
        for n, d in fraction_data[1:]:
            if n == 0:
                raise ValueError("Cannot divide by a rational with zero numerator.")
            quot_numer *= d
            quot_denom *= n
        return self.simplify_rational(quot_numer, quot_denom)

    def compute_lcm(self, a, b):
        return abs(a * b) // gcd(a, b) if a and b else 0

    def simplify_rational(self, numerator, denominator):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        if numerator == 0:
            return (0, 1)
        common_factor = gcd(numerator, denominator)
        return (numerator // common_factor, denominator // common_factor)

if __name__ == "__main__":
    main_window = tk.Tk()
    app = RationalToolApp(main_window)
    main_window.mainloop()
