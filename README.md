# 🛡️ Privacy Shield

A lightweight desktop utility that lets you instantly **blur the currently active window** using a global hotkey. Useful for privacy during screen sharing, streaming, or working in public spaces.

---

<img width="489" height="320" alt="Screenshot 2026-04-25 183459" src="https://github.com/user-attachments/assets/2d358365-7a28-4cab-9e56-66158ed44401" />
## ✨ Features

* 🔒 Blur any active window instantly
* 🎚️ Adjustable blur intensity (1–50)
* ⌨️ Custom global hotkey
* 🧵 Background hotkey listener (non-blocking)
* 🖥️ System tray integration
* 👆 Click overlay to remove blur

---

## 📦 Requirements

Install the required Python packages:

```bash
pip install customtkinter keyboard pyautogui pygetwindow pystray pillow
```

---

## 🚀 How to Run

```bash
python your_script_name.py
```

---

## 🧠 How It Works

1. The app runs a GUI using **CustomTkinter**
2. A background thread listens for a global hotkey
3. When triggered:

   * Captures a screenshot of the active window
   * Applies Gaussian blur
   * Displays it as an overlay on top of the window
4. Clicking the overlay removes it

---

## 🖥️ UI Overview

| Element           | Description                                    |
| ----------------- | ---------------------------------------------- |
| **Blur Slider**   | Adjust blur strength                           |
| **Hotkey Input**  | Set your global shortcut (e.g. `ctrl+shift+x`) |
| **Start Service** | Enable/disable hotkey listener                 |
| **Hide to Tray**  | Minimize app to system tray                    |
| **Exit**          | Close the app                                  |

---

## ⌨️ Hotkey Format

Use combinations like:

```
ctrl+shift+x
alt+z
ctrl+alt+b
```

If invalid, the app will display **"Invalid Hotkey"**.

---

## 🔄 Usage Flow

1. Launch the app
2. Set:

   * Blur intensity
   * Hotkey
3. Click **Start Service**
4. Press your hotkey:

   * Overlay appears (blurred window)
5. Click overlay or press hotkey again to remove it

---

## 📌 System Tray Controls

When minimized to tray, you can:

* **Show** → Restore window
* **Toggle Service** → Start/Stop hotkey listener
* **Exit** → Quit application

---

## 🧵 Threading

* A daemon thread runs the hotkey listener
* Uses `threading.Event` to safely stop execution
* Prevents UI freezing

---

## ⚠️ Notes

* Works only on **active window**
* Requires permissions for:

  * Keyboard input detection
  * Screen capture
* Some antivirus tools may flag global keyboard hooks

---

## 🛠️ Project Structure

```
privacy-shield/
│
├── main.py        # Main application file
└── README.md      # Documentation
```

---

## 🧩 Key Libraries Used

* `customtkinter` – Modern UI
* `keyboard` – Global hotkeys
* `pyautogui` – Screenshot capture
* `pygetwindow` – Active window detection
* `pystray` – System tray integration
* `Pillow` – Image processing (blur)

---

## 🛑 Stopping the App

* Click **Exit**, or
* Use tray → **Exit**

---

## 💡 Future Improvements (Optional Ideas)

* Multi-monitor support
* Blur specific regions instead of full window
* Auto-blur on app switch
* Save user settings
* Add animation for overlay
