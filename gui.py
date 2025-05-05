import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from matrix import Matrix
import csv


class MatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Calculator")

        self.label = tk.Label(root, text="Matrix Calculator", font=("Arial", 16))
        self.label.pack(pady=10)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        tk.Button(self.button_frame, text="Add Matrices", command=self.add_matrices_gui).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.button_frame, text="Multiply by Constant", command=self.multiply_constant_gui).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.button_frame, text="Matrix Multiplication", command=self.multiply_matrices_gui).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.button_frame, text="Transpose", command=self.transpose_gui).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.button_frame, text="Determinant", command=self.determinant_gui).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(self.button_frame, text="Inverse", command=self.inverse_gui).grid(row=2, column=1, padx=10, pady=10)

        self.history_label = tk.Label(root, text="History", font=("Arial", 12))
        self.history_label.pack(pady=10)

        self.history_text = tk.Listbox(root, height=15, width=60)
        self.history_text.pack(pady=5)

        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        tk.Button(self.control_frame, text="Clear History", command=self.clear_history).grid(row=0, column=0, padx=5)
        tk.Button(self.control_frame, text="Export to TXT", command=self.export_txt).grid(row=0, column=1, padx=5)
        tk.Button(self.control_frame, text="Export to CSV", command=self.export_csv).grid(row=0, column=2, padx=5)

        self.dark_mode = tk.BooleanVar(value=False)
        self.theme_toggle_btn = tk.Button(self.control_frame, text="Switch to Dark Mode", command=self.switch_theme)
        self.theme_toggle_btn.grid(row=0, column=3, padx=5)

        self.history = []

    def get_matrix_input(self, rows, cols):
        input_data = []
        for i in range(rows):
            row_data = simpledialog.askstring("Matrix Input", f"Enter row {i + 1} (space separated values for {cols} columns):")
            input_data.append(row_data)
        return input_data

    def add_matrices_gui(self):
        try:
            rows, cols = map(int, simpledialog.askstring("Matrix Size", "Enter rows and columns (space separated):").split())
            matrix_a = Matrix(rows, cols)
            matrix_b = Matrix(rows, cols)

            data_a = self.get_matrix_input(rows, cols)
            data_b = self.get_matrix_input(rows, cols)

            matrix_a.create_from_input(data_a)
            matrix_b.create_from_input(data_b)

            result = matrix_a.add(matrix_b)

            result_str = "Addition of Matrices:\nMatrix A:\n" + "\n".join(" ".join(map(str, row)) for row in matrix_a.matrix)
            result_str += "\nMatrix B:\n" + "\n".join(" ".join(map(str, row)) for row in matrix_b.matrix)
            result_str += "\nResult:\n" + "\n".join(" ".join(map(str, row)) for row in result.matrix)

            self.update_history(result_str)
            self.display_result("Addition Result", result.matrix)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def multiply_constant_gui(self):
        try:
            rows, cols = map(int, simpledialog.askstring("Matrix Size", "Enter rows and columns (space separated):").split())
            matrix_a = Matrix(rows, cols)
            data_a = self.get_matrix_input(rows, cols)
            matrix_a.create_from_input(data_a)

            constant = float(simpledialog.askstring("Constant", "Enter the constant to multiply:"))
            result = matrix_a.multiply_by_constant(constant)

            result_str = f"Multiplication by Constant ({constant}):\nMatrix A:\n"
            result_str += "\n".join(" ".join(map(str, row)) for row in matrix_a.matrix)
            result_str += "\nResult:\n" + "\n".join(" ".join(map(str, row)) for row in result.matrix)

            self.update_history(result_str)
            self.display_result("Multiplication by Constant Result", result.matrix)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def multiply_matrices_gui(self):
        try:
            rows_a, cols_a = map(int, simpledialog.askstring("Matrix Size", "Enter rows and columns for the first matrix (space separated):").split())
            matrix_a = Matrix(rows_a, cols_a)

            rows_b, cols_b = map(int, simpledialog.askstring("Matrix Size", "Enter rows and columns for the second matrix (space separated):").split())
            matrix_b = Matrix(rows_b, cols_b)

            data_a = self.get_matrix_input(rows_a, cols_a)
            data_b = self.get_matrix_input(rows_b, cols_b)

            matrix_a.create_from_input(data_a)
            matrix_b.create_from_input(data_b)

            result = matrix_a.multiply_by_matrix(matrix_b)

            result_str = "Matrix Multiplication:\nMatrix A:\n" + "\n".join(" ".join(map(str, row)) for row in matrix_a.matrix)
            result_str += "\nMatrix B:\n" + "\n".join(" ".join(map(str, row)) for row in matrix_b.matrix)
            result_str += "\nResult:\n" + "\n".join(" ".join(map(str, row)) for row in result.matrix)

            self.update_history(result_str)
            self.display_result("Matrix Multiplication Result", result.matrix)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def transpose_gui(self):
        try:
            rows, cols = map(int, simpledialog.askstring("Matrix Size", "Enter rows and columns (space separated):").split())
            matrix_a = Matrix(rows, cols)
            data_a = self.get_matrix_input(rows, cols)
            matrix_a.create_from_input(data_a)

            result = matrix_a.transpose()

            result_str = "Transpose:\nOriginal Matrix:\n" + "\n".join(" ".join(map(str, row)) for row in matrix_a.matrix)
            result_str += "\nTransposed Matrix:\n" + "\n".join(" ".join(map(str, row)) for row in result.matrix)

            self.update_history(result_str)
            self.display_result("Transpose Result", result.matrix)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def determinant_gui(self):
        try:
            rows, cols = map(int, simpledialog.askstring("Matrix Size", "Enter rows and columns (space separated):").split())
            matrix_a = Matrix(rows, cols)
            data_a = self.get_matrix_input(rows, cols)
            matrix_a.create_from_input(data_a)

            det = matrix_a.determinant()

            result_str = "Determinant:\nMatrix:\n" + "\n".join(" ".join(map(str, row)) for row in matrix_a.matrix)
            result_str += f"\nDeterminant: {det}"

            self.update_history(result_str)

            result_window = tk.Toplevel(self.root)
            result_window.title("Determinant Result")
            tk.Label(result_window, text=f"Determinant: {det}", font=("Arial", 12)).pack()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def inverse_gui(self):
        try:
            rows, cols = map(int, simpledialog.askstring("Matrix Size", "Enter rows and columns (space separated):").split())
            matrix_a = Matrix(rows, cols)
            data_a = self.get_matrix_input(rows, cols)
            matrix_a.create_from_input(data_a)

            result = matrix_a.inverse()

            result_str = "Inverse:\nOriginal Matrix:\n" + "\n".join(" ".join(map(str, row)) for row in matrix_a.matrix)
            result_str += "\nInverse Matrix:\n" + "\n".join(" ".join(map(str, row)) for row in result.matrix)

            self.update_history(result_str)
            self.display_result("Inverse Result", result.matrix)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_history(self, result_str):
        formatted = result_str.strip()
        self.history.append(formatted)
        for line in formatted.split('\n'):
            self.history_text.insert(tk.END, line)
        self.history_text.insert(tk.END, "-" * 30)

    def display_result(self, title, matrix):
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        tk.Label(result_window, text=title, font=("Arial", 12)).pack()
        for row in matrix:
            tk.Label(result_window, text=" ".join(map(str, row))).pack()

    def clear_history(self):
        self.history = []
        self.history_text.delete(0, tk.END)

    def export_txt(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                for entry in self.history:
                    f.write(entry + '\n' + "-" * 30 + '\n')
            messagebox.showinfo("Export", "History exported to TXT successfully.")

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                for entry in self.history:
                    writer.writerow([entry])
            messagebox.showinfo("Export", "History exported to CSV successfully.")

    def switch_theme(self):
        self.dark_mode.set(not self.dark_mode.get())
        self.apply_theme()

    def apply_theme(self):
        dark = self.dark_mode.get()
        bg_color = "#2e2e2e" if dark else "SystemButtonFace"
        fg_color = "white" if dark else "black"
        entry_bg = "#1e1e1e" if dark else "white"

        self.root.configure(bg=bg_color)
        self.label.configure(bg=bg_color, fg=fg_color)
        self.button_frame.configure(bg=bg_color)
        self.history_label.configure(bg=bg_color, fg=fg_color)
        self.control_frame.configure(bg=bg_color)
        self.history_text.configure(bg=entry_bg, fg=fg_color, selectbackground="gray", insertbackground=fg_color)

        all_buttons = self.button_frame.winfo_children() + self.control_frame.winfo_children()
        for btn in all_buttons:
            try:
                btn.configure(bg="gray20" if dark else "lightgray", fg=fg_color)
            except:
                pass

        self.theme_toggle_btn.configure(
            text="Switch to Light Mode" if dark else "Switch to Dark Mode"
        )

def splash_screen(root):
    splash = tk.Toplevel(root)
    splash.title("Welcome")
    splash.geometry("400x300")
    label = tk.Label(splash, text="Welcome to Matrix Calculator", font=("Arial", 20))
    label.pack(expand=True)

    root.after(1200, lambda: splash.destroy())  # Close splash screen after 3 seconds
    root.after(1200, lambda: MatrixApp(root))  # Start the main app after splash


if __name__ == "__main__":
    root = tk.Tk()
    splash_screen(root)
    root.mainloop()
