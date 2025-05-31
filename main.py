import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Блокнот")
        self.root.geometry("800x600")

        self.text_area = tk.Text(self.root, undo=True, wrap='word')
        self.text_area.pack(fill=tk.BOTH, expand=1)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        # Файл
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Відкрити", command=self.open_file)
        file_menu.add_command(label="Зберегти", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.quit)
        self.menu.add_cascade(label="Файл", menu=file_menu)

        # Редагування
        edit_menu = tk.Menu(self.menu, tearoff=0)
        edit_menu.add_command(label="Вирізати", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Копіювати", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Вставити", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Відмінити", command=lambda: self.text_area.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Повернути", command=lambda: self.text_area.event_generate("<<Redo>>"))
        self.menu.add_cascade(label="Редагування", menu=edit_menu)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()