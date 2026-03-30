import threading
import time

import customtkinter as ctk
import keyboard
import pyautogui

import pygetwindow as gw
import pystray
from PIL import Image, ImageDraw, ImageFilter, ImageTk
from pystray import MenuItem as item


class PrivacyShieldApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        # Встановлюємо темний режим інтерфейсу.
        ctk.set_default_color_theme("dark-blue")  # Встановлюємо кольорову тему.
        self.title("Privacy Shield")  # Заголовок головного вікна.
        self.geometry("500x300")

        # Початковий розмір вікна.

        self.blur = ctk.IntVar(value=20)

        # Змінна для сили розмиття (керується слайдером).
        self.hotkey = ctk.StringVar(value="ctrl+shift+x")  # Текст гарячої клавіші з поля вводу.
        self.status = ctk.StringVar(value="Inactive")  # CTaTyc cepBicy: Active/Inactive.
        self.overlay = None  # Посилання на вікно-оверлей (розмите накриття).
        self.overlay_img = None  # Посилання на PhotoImage, щоб зображення не зникало зі пам'яті.
        self.service_active = False  # Прапорець, чи запущений сервіс гарячої клавіші.
        self.stop_event = threading.Event()  # Сигнал для зупинки фонового потоку.
        self.listener_thread = None  # Посилання на потік, який слухає hotkey.
        self.hotkey_id = None  # Ідентифікатор зареєстрованої гарячої клавіші в бібліотеці keyboard.
        self.tray = None  # Посилання на іконку трею.

        self._build_ui()  # Створюємо всі елементи графічного інтерфейсу.

        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

    def _build_ui(self):

        box = ctk.CTkFrame(self, corner_radius=14)

        # Основний контейнер з заокругленням.
        box.pack(fill="both", expand=True, padx=14, pady=14)

        ctk.CTkLabel(box, text="Privacy Shield", font=ctk.CTkFont(size=26, weight="bold")).pack(anchor="w", padx=16, pady=(14, 6))

        self.status_lbl = ctk.CTkLabel(box, textvariable=self.status, text_color="#ff6b6b")

        self.status_lbl.pack(anchor="w", padx=16)

        ctk.CTkLabel(box, text="Blur intensity (1-50)").pack(anchor="w", padx=16, pady=(12, 0))

        ctk.CTkSlider(box, from_=1, to=50, number_of_steps=49, variable=self.blur).pack(fill="x", padx=16, pady=6)

        ctk.CTkLabel(box, text="Global hotkey").pack(anchor="w", padx=16, pady=(8, 0))
        ctk.CTkEntry(box, textvariable=self.hotkey).pack(fill="x", padx=16, pady=6)

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=14)

        self.start_btn = ctk.CTkButton(row, text="Start Service", command=self.toggle_service)
        self.start_btn.pack(side="left", padx=(0, 8))

        ctk.CTkButton(row, text="Hide to Tray", command=self.hide_to_tray).pack(side="left")

        ctk.CTkButton(row, text="Exit", fg_color="#963434", hover_color="#ab3b3b", command=self.exit_app).pack(side="right")

    def set_status(self, active):
        self.status.set("Active" if active else "Inactive")  # MiHAEMO TeKCT CTaTycy.
        self.status_lbl.configure(text_color="#66e28a" if active else "#ff6b6b")

        # Зелений для Active, червоний для Inactive.

        self.start_btn.configure(text="Stop Service" if active else "Start Service")

    def toggle_service(self):
        if self.service_active:  # Якщо сервіс уже працює, виконуємо зупинку.
            self.stop_event.set()  # Даємо сигнал потоку завершитись.
            if self.listener_thread and self.listener_thread.is_alive():  # живий.Якщо потік ще
                self.listener_thread.join(timeout=1)  # Чекаємо максимум 1 секунду на завершення.
            self.hide_overlay()  # При зупинці ховаємо можливий оверлей.
            self.service_active = False  # ФikcyєMo стаH "вимкнено".
            self.set_status(False)  # Оновлюємо UI-індикатори.
            return

        try:
            keyboard.parse_hotkey(self.hotkey.get().strip().lower())
            # Перевіряємо валідність формату hotkey.

        except Exception:  # Якщо формат невірний.
            self.status.set("Invalid Hotkey")

            # Показуємо повідомлення про помилку.
            self.status_lbl.configure(text_color="#ffd166")

            # Жовтий колір для попередження.
            return  # Не запускаємо сервіс з невалідною комбінацією.

        self.stop_event.clear()  # Скидаємо прапорець зупинки перед новим запуском.
        self.listener_thread = threading.Thread(target=self.listen_hotkey, daemon=True)
        # Створюємо фоновий

        self.listener_thread.start()  # Запускаємо прослуховування гарячої клавіші.
        self.service_active = True  # Позначаємо, що сервіс активний.
        self.set_status(True)  # Оновлюємо індикатор у GUI.

    def listen_hotkey(self):

        self.hotkey_id = keyboard.add_hotkey(self.hotkey.get().strip().lower(), lambda: self.after(0, self.toggle_overlay))

        while not self.stop_event.is_set():
            time.sleep(0.1)

        if self.hotkey_id is not None:  # Якщо гаряча клавіша була зареєстрована.
            keyboard.remove_hotkey(self.hotkey_id)  # Прибираємо реєстрацію hotkey.
            self.hotkey_id = None  # Очищаємо збережений

    def toggle_overlay(self):

        if self.overlay and self.overlay.winfo_exists():

            # Якщо оверлей уже є на екрані.
            self.hide_overlay()  # Повторний виклик ховає оверлей (toggle-поведінка).
            return

        win = gw.getActiveWindow()  # Отримуємо поточне активне вікно ОС.
        if not win or win.width <= 0 or win.height <= 0:

            return

        x, y, w, h = win.left, win.top, win.width, win.height

        img = pyautogui.screenshot(region=(x, y, w, h)).filter(ImageFilter.GaussianBlur(radius=int(self.blur.get())))

        self.overlay_img = ImageTk.PhotoImage(img)  # Перетворюємо PIL-Image у формат для tkinter.
        self.overlay = ctk.CTkToplevel(self)  # Створюємо окреме верхнє вікно-накладку.
        self.overlay.overrideredirect(True)  # Прибираємо рамку і системні кнопки вікна.
        self.overlay.attributes("-topmost", True)  # Тримаємо оверлей поверх інших вікон.
        self.overlay.geometry(f"{w}x{h}+{x}+{y}")  # Розміщуємо оверлей точно поверх активного вікна.

        lbl = ctk.CTkLabel(self.overlay, text="", image=self.overlay_img)
        # Віджет, що показує розмите зображення.
        lbl.pack(fill="both", expand=True)  # Розтягуємо зображення на весь оверлей.

        self.overlay.bind("<Button-1>", lambda _e: self.hide_overlay())

        # Клік по вікну закриває оверлей.
        lbl.bind("<Button-1>", lambda _e: self.hide_overlay())  # Клік по самому зображенню також закриває.

    def hide_overlay(self):
        if self.overlay and self.overlay.winfo_exists():  # Перевірка, що вікно реально створене.
            self.overlay.destroy()

            # Повністю видаляємо вікно оверлею.
            self.overlay = None  # Скидаємо посилання після закриття.

    def hide_to_tray(self):

        self.withdraw()

        # Ховаємо головне вікно з екрана.
        if self.tray:  # Якщо трей уже запущений вдруге не створюємо.
            return

        icon = Image.new("RGBA", (64, 64), (20, 22, 30, 255))  # Порожнє тло майбутньої іконки.
        d = ImageDraw.Draw(icon)  # Отримуємо "пензель" для малювання.
        d.rounded_rectangle((10, 10, 54, 54), radius=10, outline=(102, 226, 138), width=3)

        # Рамка-щит.
        d.polygon([(32, 16), (46, 24), (42, 40), (32, 48), (22, 40), (18, 24)], fill=(102, 226, 138))  # Силует щита.

        # Меню трею: показати вікно, перемкнути сервіс, вийти з програми.
        menu = (
            item("Show", lambda _i, _m: self.after(0, self.show_from_tray)),
            item("Toggle Service", lambda _i, _m: self.after(0, self.toggle_service)),
            item("Exit", lambda _i, _m: self.after(0, self.exit_app)),
        )

        self.tray = pystray.Icon("PrivacyShield", icon, "Privacy Shield", menu)  # CTBOPIEMO 06'EKT TpeIo.
        threading.Thread(target=self.tray.run, daemon=True).start()  # Запускаємо трей у фоні.

    def show_from_tray(self):

        self.deiconify()

        # Робимо вікно знову видимим.

        self.lift()

        # Піднімаємо вікно поверх інших.
        self.focus_force()

        # Передаємо фокус введення в це вікно.

    def exit_app(self):
        self.stop_event.set()  # Зупиняємо цикл прослуховування hotkey.
        self.hide_overlay()  # Прибираємо оверлей, якщо він був відкритий.

        if self.hotkey_id is not None:  # Якщо hotkey був зареєстрований.
            keyboard.remove_hotkey(self.hotkey_id)  # Видаляємо його перед виходом.

        if self.tray:  # Якщо трей-іконка створена.
            self.tray.stop()  # Зупиняємо цикл pystray.
            self.tray = None  # Очищаємо посилання.

        self.destroy()  # Закриваємо головне вікно і завершуємо mainloop.


if __name__ == "__main__":
    PrivacyShieldApp().mainloop()
