import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil


class DanrexRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("Danrex Renamer")
        self.root.geometry("650x650")
        self.root.minsize(650, 650)
        self.root.configure(bg='#0a0a0a')

        self.colors = {
            'bg': '#0a0a0a',
            'bg_secondary': '#141414',
            'bg_tertiary': '#1a1a1a',
            'fg': '#ffffff',
            'fg_secondary': '#a0a0a0',
            'accent': '#00ff88',
            'accent_dark': '#00cc6a',
            'border': '#2a2a2a',
            'error': '#ff4444',
            'warning': '#ffaa00'
        }

        self.current_folder = ""
        self.files = []
        self.preview_data = []

        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        top_line = tk.Frame(main_frame, bg=self.colors['accent'], height=2)
        top_line.pack(fill=tk.X, pady=(0, 20))

        title_label = tk.Label(main_frame, text="✏️ Danrex Renamer",
                               font=('Segoe UI', 20, 'bold'),
                               bg=self.colors['bg'], fg=self.colors['accent'])
        title_label.pack(anchor=tk.W, pady=(0, 5))

        subtitle_label = tk.Label(main_frame, text="Массовое переименование файлов",
                                  font=('Segoe UI', 10),
                                  bg=self.colors['bg'], fg=self.colors['fg_secondary'])
        subtitle_label.pack(anchor=tk.W, pady=(0, 20))

        folder_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'],
                                relief=tk.FLAT, bd=1, highlightbackground=self.colors['border'],
                                highlightthickness=1)
        folder_frame.pack(fill=tk.X, pady=(0, 15))

        folder_inner = tk.Frame(folder_frame, bg=self.colors['bg_secondary'])
        folder_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        folder_label = tk.Label(folder_inner, text="📁 Выберите папку",
                                font=('Segoe UI', 10, 'bold'),
                                bg=self.colors['bg_secondary'], fg=self.colors['fg'])
        folder_label.pack(anchor=tk.W, pady=(0, 10))

        folder_controls = tk.Frame(folder_inner, bg=self.colors['bg_secondary'])
        folder_controls.pack(fill=tk.X)

        self.folder_path_var = tk.StringVar()
        self.folder_path_var.set("Папка не выбрана")
        self.folder_entry = tk.Entry(folder_controls, textvariable=self.folder_path_var,
                                     font=('Segoe UI', 10), bg=self.colors['bg_tertiary'],
                                     fg=self.colors['fg_secondary'], relief=tk.FLAT,
                                     state='readonly', readonlybackground=self.colors['bg_tertiary'])
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.browse_btn = tk.Button(folder_controls, text="Обзор", command=self.select_folder,
                                    cursor="hand2", bg=self.colors['accent'], fg='#0a0a0a',
                                    font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, padx=15, pady=5)
        self.browse_btn.pack(side=tk.RIGHT)

        mode_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'],
                              relief=tk.FLAT, bd=1, highlightbackground=self.colors['border'],
                              highlightthickness=1)
        mode_frame.pack(fill=tk.X, pady=(0, 15))

        mode_inner = tk.Frame(mode_frame, bg=self.colors['bg_secondary'])
        mode_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        mode_label = tk.Label(mode_inner, text="🎯 Режим переименования",
                              font=('Segoe UI', 10, 'bold'),
                              bg=self.colors['bg_secondary'], fg=self.colors['fg'])
        mode_label.pack(anchor=tk.W, pady=(0, 10))

        self.mode_var = tk.StringVar(value="Добавить префикс")
        self.mode_menu = ttk.Combobox(mode_inner, textvariable=self.mode_var,
                                      values=["Добавить префикс", "Добавить суффикс", "Заменить текст",
                                              "Нумерация", "Удалить символы"],
                                      state="readonly", font=('Segoe UI', 10))
        self.mode_menu.pack(fill=tk.X)
        self.mode_menu.bind('<<ComboboxSelected>>', self.on_mode_change)

        self.value_frame = tk.Frame(mode_inner, bg=self.colors['bg_secondary'])
        self.value_frame.pack(fill=tk.X, pady=(10, 0))

        self.create_value_inputs()

        preview_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'],
                                 relief=tk.FLAT, bd=1, highlightbackground=self.colors['border'],
                                 highlightthickness=1)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        preview_header = tk.Frame(preview_frame, bg=self.colors['bg_secondary'])
        preview_header.pack(fill=tk.X, padx=15, pady=(15, 5))

        preview_title = tk.Label(preview_header, text="📋 Предпросмотр",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg=self.colors['bg_secondary'], fg=self.colors['fg'])
        preview_title.pack(side=tk.LEFT)

        preview_count = tk.Label(preview_header, text="0 файлов",
                                 font=('Segoe UI', 9),
                                 bg=self.colors['bg_secondary'], fg=self.colors['accent'])
        preview_count.pack(side=tk.RIGHT)
        self.preview_count_label = preview_count

        preview_container = tk.Frame(preview_frame, bg=self.colors['bg'])
        preview_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        scrollbar = tk.Scrollbar(preview_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.preview_listbox = tk.Listbox(preview_container, bg=self.colors['bg_tertiary'],
                                          fg=self.colors['fg'], selectbackground=self.colors['accent'],
                                          font=('Consolas', 9), relief=tk.FLAT,
                                          yscrollcommand=scrollbar.set)
        self.preview_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.preview_listbox.yview)

        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(0, 10))

        self.preview_btn = tk.Button(button_frame, text="👁️ Предпросмотр", command=self.preview,
                                     cursor="hand2", bg=self.colors['bg_secondary'], fg=self.colors['accent'],
                                     font=('Segoe UI', 10, 'bold'), relief=tk.FLAT, bd=1,
                                     highlightbackground=self.colors['border'], highlightthickness=1,
                                     padx=20, pady=8)
        self.preview_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        self.rename_btn = tk.Button(button_frame, text="🔄 Переименовать", command=self.rename_files,
                                    cursor="hand2", bg=self.colors['accent'], fg='#0a0a0a',
                                    font=('Segoe UI', 10, 'bold'), relief=tk.FLAT,
                                    padx=20, pady=8, state=tk.DISABLED)
        self.rename_btn.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        status_bar = tk.Frame(main_frame, bg=self.colors['bg_secondary'], height=35)
        status_bar.pack(fill=tk.X)

        self.status_emoji = tk.Label(status_bar, text="✅", font=('Segoe UI', 11),
                                     bg=self.colors['bg_secondary'], fg=self.colors['accent'])
        self.status_emoji.pack(side=tk.LEFT, padx=(15, 10))

        self.status_label = tk.Label(status_bar, text="Готов к работе",
                                     font=('Segoe UI', 9),
                                     bg=self.colors['bg_secondary'], fg=self.colors['fg'])
        self.status_label.pack(side=tk.LEFT)

    def create_value_inputs(self):
        for widget in self.value_frame.winfo_children():
            widget.destroy()

        mode = self.mode_var.get()

        if mode == "Добавить префикс":
            tk.Label(self.value_frame, text="Префикс:", bg=self.colors['bg_secondary'],
                     fg=self.colors['fg'], font=('Segoe UI', 9)).pack(anchor=tk.W)
            self.value_entry = tk.Entry(self.value_frame, font=('Segoe UI', 10),
                                        bg=self.colors['bg_tertiary'], fg=self.colors['fg'],
                                        relief=tk.FLAT, insertbackground=self.colors['accent'])
            self.value_entry.pack(fill=tk.X, pady=(5, 0))

        elif mode == "Добавить суффикс":
            tk.Label(self.value_frame, text="Суффикс:", bg=self.colors['bg_secondary'],
                     fg=self.colors['fg'], font=('Segoe UI', 9)).pack(anchor=tk.W)
            self.value_entry = tk.Entry(self.value_frame, font=('Segoe UI', 10),
                                        bg=self.colors['bg_tertiary'], fg=self.colors['fg'],
                                        relief=tk.FLAT, insertbackground=self.colors['accent'])
            self.value_entry.pack(fill=tk.X, pady=(5, 0))

        elif mode == "Заменить текст":
            tk.Label(self.value_frame, text="Что заменить:", bg=self.colors['bg_secondary'],
                     fg=self.colors['fg'], font=('Segoe UI', 9)).pack(anchor=tk.W)
            self.find_entry = tk.Entry(self.value_frame, font=('Segoe UI', 10),
                                       bg=self.colors['bg_tertiary'], fg=self.colors['fg'],
                                       relief=tk.FLAT, insertbackground=self.colors['accent'])
            self.find_entry.pack(fill=tk.X, pady=(5, 5))

            tk.Label(self.value_frame, text="Заменить на:", bg=self.colors['bg_secondary'],
                     fg=self.colors['fg'], font=('Segoe UI', 9)).pack(anchor=tk.W)
            self.replace_entry = tk.Entry(self.value_frame, font=('Segoe UI', 10),
                                          bg=self.colors['bg_tertiary'], fg=self.colors['fg'],
                                          relief=tk.FLAT, insertbackground=self.colors['accent'])
            self.replace_entry.pack(fill=tk.X, pady=(5, 0))

        elif mode == "Нумерация":
            number_frame = tk.Frame(self.value_frame, bg=self.colors['bg_secondary'])
            number_frame.pack(fill=tk.X)

            tk.Label(number_frame, text="Начальный номер:", bg=self.colors['bg_secondary'],
                     fg=self.colors['fg'], font=('Segoe UI', 9)).pack(anchor=tk.W)
            self.start_number = tk.Entry(number_frame, font=('Segoe UI', 10),
                                         bg=self.colors['bg_tertiary'], fg=self.colors['fg'],
                                         relief=tk.FLAT, insertbackground=self.colors['accent'])
            self.start_number.pack(fill=tk.X, pady=(5, 5))
            self.start_number.insert(0, "1")

            tk.Label(number_frame, text="Формат (например: 001, file_01):", bg=self.colors['bg_secondary'],
                     fg=self.colors['fg'], font=('Segoe UI', 9)).pack(anchor=tk.W)
            self.number_format = tk.Entry(number_frame, font=('Segoe UI', 10),
                                          bg=self.colors['bg_tertiary'], fg=self.colors['fg'],
                                          relief=tk.FLAT, insertbackground=self.colors['accent'])
            self.number_format.pack(fill=tk.X, pady=(5, 0))
            self.number_format.insert(0, "001")

        elif mode == "Удалить символы":
            range_frame = tk.Frame(self.value_frame, bg=self.colors['bg_secondary'])
            range_frame.pack(fill=tk.X)

            tk.Label(range_frame, text="Начать с позиции (1 - первая буква):", bg=self.colors['bg_secondary'],
                     fg=self.colors['fg'], font=('Segoe UI', 9)).pack(anchor=tk.W)
            self.start_pos = tk.Entry(range_frame, font=('Segoe UI', 10),
                                      bg=self.colors['bg_tertiary'], fg=self.colors['fg'],
                                      relief=tk.FLAT, insertbackground=self.colors['accent'])
            self.start_pos.pack(fill=tk.X, pady=(5, 5))
            self.start_pos.insert(0, "1")

            tk.Label(range_frame, text="Закончить на позиции:", bg=self.colors['bg_secondary'],
                     fg=self.colors['fg'], font=('Segoe UI', 9)).pack(anchor=tk.W)
            self.end_pos = tk.Entry(range_frame, font=('Segoe UI', 10),
                                    bg=self.colors['bg_tertiary'], fg=self.colors['fg'],
                                    relief=tk.FLAT, insertbackground=self.colors['accent'])
            self.end_pos.pack(fill=tk.X, pady=(5, 0))

    def on_mode_change(self, event=None):
        self.create_value_inputs()
        if self.current_folder:
            self.preview()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.current_folder = folder
            self.folder_path_var.set(folder)
            self.scan_files()
            self.rename_btn.config(state=tk.NORMAL)
            self.preview()

    def scan_files(self):
        self.files = []
        if self.current_folder:
            for filename in os.listdir(self.current_folder):
                filepath = os.path.join(self.current_folder, filename)
                if os.path.isfile(filepath):
                    self.files.append(filename)
            self.files.sort()
        self.update_status(f"Найдено файлов: {len(self.files)}", is_success=True)

    def get_new_name(self, old_name, index=None):
        name, ext = os.path.splitext(old_name)
        mode = self.mode_var.get()

        if mode == "Добавить префикс":
            prefix = self.get_entry_value()
            return prefix + old_name

        elif mode == "Добавить суффикс":
            suffix = self.get_entry_value()
            return name + suffix + ext

        elif mode == "Заменить текст":
            find_text = self.find_entry.get().strip()
            replace_text = self.replace_entry.get().strip()
            if find_text:
                return old_name.replace(find_text, replace_text)
            return old_name

        elif mode == "Нумерация":
            try:
                start = int(self.start_number.get().strip() if self.start_number.get().strip() else "1")
                fmt = self.number_format.get().strip() if self.number_format.get().strip() else "001"
                num = start + (index if index is not None else 0)

                if fmt.isdigit():
                    num_str = str(num).zfill(len(fmt))
                else:
                    if '#' in fmt:
                        num_str = fmt.replace('#', str(num))
                    else:
                        num_str = f"{fmt}{num}"

                return f"{num_str}{ext}"
            except:
                return f"{index + 1}{ext}"

        elif mode == "Удалить символы":
            try:
                start = int(self.start_pos.get().strip()) - 1
                end = int(self.end_pos.get().strip())
                if start < 0:
                    start = 0
                if end > len(name):
                    end = len(name)
                new_name = name[:start] + name[end:]
                return new_name + ext if new_name else old_name
            except:
                return old_name

        return old_name

    def get_entry_value(self):
        try:
            return self.value_entry.get().strip()
        except:
            return ""

    def preview(self):
        if not self.current_folder:
            messagebox.showwarning("Предупреждение", "Сначала выберите папку!")
            return

        mode = self.mode_var.get()

        if mode in ["Добавить префикс", "Добавить суффикс"]:
            if not self.get_entry_value():
                messagebox.showwarning("Предупреждение", "Введите значение!")
                return

        if mode == "Заменить текст":
            if not self.find_entry.get().strip():
                messagebox.showwarning("Предупреждение", "Введите текст для замены!")
                return

        if mode == "Нумерация":
            if not self.start_number.get().strip():
                messagebox.showwarning("Предупреждение", "Введите начальный номер!")
                return

        self.preview_listbox.delete(0, tk.END)
        self.preview_data = []

        for idx, old_name in enumerate(self.files):
            new_name = self.get_new_name(old_name, idx)
            self.preview_data.append((old_name, new_name))
            self.preview_listbox.insert(tk.END, f"{old_name}  →  {new_name}")

        self.preview_count_label.config(text=f"{len(self.files)} файлов")
        self.update_status(f"Предпросмотр: {len(self.files)} файлов", is_success=True)

    def get_unique_filename(self, folder, filename, counter=1):
        name, ext = os.path.splitext(filename)
        new_filename = filename

        if counter > 1:
            new_filename = f"{name}_copy{counter - 1}{ext}"

        if os.path.exists(os.path.join(folder, new_filename)):
            return self.get_unique_filename(folder, filename, counter + 1)
        return new_filename

    def rename_files(self):
        if not self.preview_data:
            messagebox.showwarning("Предупреждение", "Сначала выполните предпросмотр!")
            return

        if not messagebox.askyesno("Подтверждение", f"Переименовать {len(self.files)} файлов?"):
            return

        renamed = 0
        errors = 0

        for old_name, new_name in self.preview_data:
            old_path = os.path.join(self.current_folder, old_name)
            new_path = os.path.join(self.current_folder, new_name)

            if old_name == new_name:
                continue

            if os.path.exists(new_path):
                new_name = self.get_unique_filename(self.current_folder, new_name)
                new_path = os.path.join(self.current_folder, new_name)

            try:
                os.rename(old_path, new_path)
                renamed += 1
            except Exception as e:
                errors += 1

        self.update_status(f"Переименовано: {renamed}, Ошибок: {errors}",
                           is_success=errors == 0)

        if renamed > 0:
            self.scan_files()
            self.preview()
        else:
            messagebox.showinfo("Результат", "Нет файлов для переименования")

    def update_status(self, message, is_error=False, is_success=False):
        self.status_label.config(text=message)
        if is_error:
            self.status_label.config(fg=self.colors['error'])
            self.status_emoji.config(text="❌", fg=self.colors['error'])
        elif is_success:
            self.status_label.config(fg=self.colors['accent'])
            self.status_emoji.config(text="✅", fg=self.colors['accent'])
        else:
            self.status_label.config(fg=self.colors['fg'])
            self.status_emoji.config(text="🔄", fg=self.colors['warning'])


def main():
    root = tk.Tk()
    app = DanrexRenamer(root)
    root.mainloop()


if __name__ == "__main__":
    main()