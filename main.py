import tkinter as tk
from tkinter import filedialog, messagebox, font
from PIL import Image, ImageTk  # Додайте цей імпорт

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Блокнот")
        self.root.geometry("800x600")

        # ОДИН фрейм для всіх елементів керування (шрифт + кнопки вирівнювання)
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=5, pady=2)

        # Список шрифтів
        self.font_families = list(font.families())
        self.font_var = tk.StringVar(value="Arial")
        font_menu = tk.OptionMenu(control_frame, self.font_var, *self.font_families)
        font_menu.pack(side=tk.LEFT, padx=5)

        # Список розмірів
        self.font_size_var = tk.IntVar(value=12)
        font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 32, 36, 48, 72]
        size_menu = tk.OptionMenu(control_frame, self.font_size_var, *font_sizes)
        size_menu.pack(side=tk.LEFT, padx=5)

        # Кнопка застосування стилю до виділеного тексту
        apply_btn = tk.Button(control_frame, text="Застосувати", command=self.apply_font)
        apply_btn.pack(side=tk.LEFT, padx=5)

        # Завантаження іконок для кнопок вирівнювання
        align_left_img = Image.open("align-left.png").resize((24, 24), Image.LANCZOS)
        self.align_left_icon = ImageTk.PhotoImage(align_left_img)
        align_center_img = Image.open("align-center.png").resize((24, 24), Image.LANCZOS)
        self.align_center_icon = ImageTk.PhotoImage(align_center_img)
        align_right_img = Image.open("align-right.png").resize((24, 24), Image.LANCZOS)
        self.align_right_icon = ImageTk.PhotoImage(align_right_img)

        # Кнопки вирівнювання в тому ж control_frame
        align_left_btn = tk.Button(
            control_frame,
            image=self.align_left_icon,
            command=self.align_left
        )
        align_left_btn.pack(side=tk.LEFT, padx=2, pady=2)

        align_center_btn = tk.Button(
            control_frame,
            image=self.align_center_icon,
            command=self.align_center
        )
        align_center_btn.pack(side=tk.LEFT, padx=2, pady=2)

        align_right_btn = tk.Button(
            control_frame,
            image=self.align_right_icon,
            command=self.align_right
        )
        align_right_btn.pack(side=tk.LEFT, padx=2, pady=2)

        # Додаємо текстове поле з вертикальним скролбаром
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=1)

        self.text_area = tk.Text(text_frame, undo=True, wrap='word')
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = tk.Scrollbar(text_frame, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)

        # Додаємо контекстне меню
        self.context_menu = tk.Menu(self.text_area, tearoff=0)
        self.context_menu.add_command(label="Вирізати", command=lambda: self.text_area.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Копіювати", command=lambda: self.text_area.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Вставити", command=lambda: self.text_area.event_generate("<<Paste>>"))

        self.text_area.bind("<Button-3>", self.show_context_menu)  # ПКМ для Windows
        self.text_area.bind("<Button-2>", self.show_context_menu)  # ПКМ для Mac

        # Додаємо гарячі клавіші для копіювання та вставки
        self.text_area.bind('<Control-v>', lambda event: self.paste_clipboard())
        self.text_area.bind('<Control-V>', lambda event: self.paste_clipboard())
        self.text_area.bind('<Control-c>', lambda event: self.copy_clipboard())
        self.text_area.bind('<Control-C>', lambda event: self.copy_clipboard())

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

    def apply_font(self):
        try:
            selected_font = self.font_var.get()
            selected_size = self.font_size_var.get()
            current_tags = self.text_area.tag_names("sel.first")
            tag_name = f"{selected_font}_{selected_size}"

            if tag_name not in self.text_area.tag_names():
                self.text_area.tag_configure(tag_name, font=(selected_font, selected_size))
            self.text_area.tag_add(tag_name, "sel.first", "sel.last")
        except tk.TclError:
            messagebox.showwarning("Увага", "Виділіть текст для зміни шрифту!")

    def align_left(self):
        # Встановлюємо вирівнювання по лівому краю для всього тексту
        self.text_area.tag_configure('left', justify='left')
        self.text_area.tag_add('left', '1.0', tk.END)
        self.text_area.tag_remove('center', '1.0', tk.END)
        self.text_area.tag_remove('right', '1.0', tk.END)

    def align_center(self):
        # Встановлюємо вирівнювання по центру для всього тексту
        self.text_area.tag_configure('center', justify='center')
        self.text_area.tag_add('center', '1.0', tk.END)
        self.text_area.tag_remove('left', '1.0', tk.END)
        self.text_area.tag_remove('right', '1.0', tk.END)

    def align_right(self):
        # Встановлюємо вирівнювання по правому краю для всього тексту
        self.text_area.tag_configure('right', justify='right')
        self.text_area.tag_add('right', '1.0', tk.END)
        self.text_area.tag_remove('left', '1.0', tk.END)
        self.text_area.tag_remove('center', '1.0', tk.END)

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

    def paste_clipboard(self):
        try:
            self.text_area.event_generate("<<Paste>>")
            return "break"
        except Exception:
            pass

    def copy_clipboard(self):
        try:
            self.text_area.event_generate("<<Copy>>")
            return "break"
        except Exception:
            pass

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()