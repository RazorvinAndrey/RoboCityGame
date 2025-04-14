import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from calculator import (
    line_parces,
    find_length,
)
from libs import robositygame as rcg


class ApertureScienceInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Rover Interface")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")

        self.scale = 1.0
        self.rotation_angle = 0
        self.original_image = Image.open("photo_2025-03-28_16-58-08.jpg")

        try:
            self.resample_method = Image.Resampling.LANCZOS
        except AttributeError:
            self.resample_method = Image.ANTIALIAS

        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=4, bg="#1e1e1e", sashrelief=tk.RAISED)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.left_panel = tk.Frame(self.paned, bg="#1e1e1e", width=500)  # Центр с лёгким смещением
        self.right_panel = tk.Frame(self.paned, bg="#1e1e1e")

        self.paned.add(self.left_panel)
        self.paned.add(self.right_panel)
        self.paned.sash_place(0, 500, 0)  # Устанавливаем положение полосы почти по центру


        self.create_scrollable_image()

        self.logo = Image.open("roboveinik.png").resize((60, 60), self.resample_method)
        self.logo_tk = ImageTk.PhotoImage(self.logo)

        self.create_right_panel()
        self.configure_styles()

    def create_scrollable_image(self):
        self.canvas = tk.Canvas(self.left_panel, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image_id = None
        self.display_image()

        self.canvas.bind("<MouseWheel>", self.zoom)

        zoom_frame = tk.Frame(self.left_panel, bg="#1e1e1e")
        zoom_frame.pack(fill=tk.X)

        ttk.Button(zoom_frame, text="+", width=3, command=self.zoom_in).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(zoom_frame, text="-", width=3, command=self.zoom_out).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(zoom_frame, text="⟳", width=3, command=self.rotate_image).pack(side=tk.LEFT, padx=5, pady=5)

    def display_image(self):
        width, height = self.original_image.size
        width, height = 0.6 * width, 0.6 * height
        rotated = self.original_image.rotate(self.rotation_angle, expand=True)
        resized = rotated.resize((int(width * self.scale), int(height * self.scale)), self.resample_method)
        self.tk_image = ImageTk.PhotoImage(resized)

        self.canvas.delete("all")
        self.image_id = self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.scale *= factor
        self.scale = max(0.1, min(self.scale, 5.0))
        self.display_image()

    def zoom_in(self):
        self.scale *= 1.1
        self.display_image()

    def zoom_out(self):
        self.scale /= 1.1
        self.display_image()

    def rotate_image(self):
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.display_image()

    def create_right_panel(self):
        logo_frame = tk.Frame(self.right_panel, bg="#1e1e1e")
        logo_frame.pack(pady=10)

        logo_label = tk.Label(logo_frame, image=self.logo_tk, bg="#1e1e1e")
        logo_label.pack(side=tk.LEFT)

        title_label = tk.Label(logo_frame, text="Робовейник", font=("Arial", 20, "bold"), fg="white", bg="#1e1e1e")
        title_label.pack(side=tk.LEFT, padx=10)

        self.toggle_btn = ttk.Button(self.right_panel, text="Скрыть изображение", command=self.toggle_image)
        self.toggle_btn.pack(pady=5)

        self.fields_frame = tk.Frame(self.right_panel, bg="#1e1e1e")
        self.fields_frame.pack(pady=10, padx=20, fill=tk.X)

        self.route_entry = self.create_labeled_entry("Маршрут:")
        self.start_pos_entry = self.create_labeled_entry("Стартовая позиция:", width=10)
        self.start_rot_entry = self.create_labeled_entry("Начальный поворот:", width=10)
        self.blocks_entry = self.create_labeled_entry("Блокировки:")
        self.flags_entry = self.create_labeled_entry("Флаги:")

        button_frame = tk.Frame(self.fields_frame, bg="#1e1e1e")
        button_frame.pack(pady=10)

        self.submit_button = ttk.Button(button_frame, text="Проверка выполнения", command=self.run_simulation)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Очистить поля", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.output_text = tk.Text(self.right_panel, height=10, bg="#222", fg="#fff", font=("Arial", 12))
        self.output_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def toggle_image(self):
        if self.left_panel.winfo_ismapped():
            self.paned.forget(self.left_panel)
            self.toggle_btn.config(text="Показать изображение")
        else:
            self.paned.add(self.left_panel, before=self.right_panel)
            self.paned.sash_place(0, 650, 0)
            self.toggle_btn.config(text="Скрыть изображение")

    def create_labeled_entry(self, label_text, width=40):
        container = tk.Frame(self.fields_frame, bg="#1e1e1e")
        container.pack(fill=tk.X, pady=5)

        label = tk.Label(container, text=label_text, fg="white", bg="#1e1e1e", anchor="w", width=18)
        label.pack(side=tk.LEFT)

        entry = ttk.Entry(container, width=width)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        return entry

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton", background="#e0e0e0", foreground="#000000", font=("Arial", 11, "bold"))
        style.map("TButton",
                  foreground=[('pressed', '#000'), ('active', '#111')],
                  background=[('pressed', '!disabled', '#ddd'), ('active', '#fff')])

        style.configure("TEntry", fieldbackground="#111111", foreground="white", padding=5)

    def run_simulation(self):
        self.output_text.delete(1.0, tk.END)

        try:
            gen_line = self.route_entry.get()
            start_pos = int(self.start_pos_entry.get())
            start_rot = int(self.start_rot_entry.get())
            blocks = list(map(int, self.blocks_entry.get().split(","))) if self.blocks_entry.get() else []
            flags = list(map(int, self.flags_entry.get().split(","))) if self.flags_entry.get() else []

            gen_graph, gen_rover, com_flag = rcg.init_game(start_pos, start_rot, blocks, flags)

            path = self.line_parse(gen_line)
            if path is None:
                self.output_text.insert(tk.END, "Некорректный маршрут.\n")
                return

            distance = self.find_length(path, gen_rover)
            if distance is None:
                self.output_text.insert(tk.END, "Ошибка при симуляции.\n")
                return

            score, message, opt_path = rcg.finalize_to_vizual_interface(gen_graph, gen_rover)
            self.output_text.insert(tk.END, f"ОЦЕНКА - {score}%\n")
            self.output_text.insert(tk.END, f"Оптимальный путь - {opt_path}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Ошибка: {e}\n")

    def line_parse(self, line):
        path = []
        path_str = line.split("-")
        for point in path_str:
            if not point.isdigit() or int(point) > 15 or int(point) < 1:
                return None
            path.append(int(point))
        return path

    def find_length(self, path, rover):
        for i in range(1, len(path)):
            if not rover.mov_to_point(path[i]):
                return None
        return rover.distance

    def clear_fields(self):
        self.route_entry.delete(0, tk.END)
        self.start_pos_entry.delete(0, tk.END)
        self.start_rot_entry.delete(0, tk.END)
        self.blocks_entry.delete(0, tk.END)
        self.flags_entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ApertureScienceInterface(root)
    root.mainloop()
