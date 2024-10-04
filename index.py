
# Information
"""
autoClicker project by Wong Zheng Jie
Github: https://github.com/WZhengJie99
Email: wzhengjie99@gmail.com
Original intention for Discord, Isekaid #1927, https://isekaid.in/
Last Updated: Oct 2024
"""

# Pre-requisites and maintenance info
"""
requirements:
pip install -r requirements.txt

or pip install via command:
python -m pip install pyautogui opencv-python pillow

Run the script via index.bat

Packaged locally with PyInstaller:
python -m pip install pyinstaller

run code to build/rebuild exe:
pyinstaller --onefile --windowed --clean  index.py

codes for cleanup pre build exe:
rmdir /s /q build
rmdir /s /q dist
del index.spec

"""

import pyautogui
import cv2
import numpy as np
from time import sleep
from PIL import ImageGrab
import threading
import tkinter as tk

paused = False
running = False  # Track whether the bot is running
button_image = None
click_delay = 15  # Default click delay in seconds

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pause_button.config(text="Resume")
        status_label.config(text="Clicker paused.", fg="orange")  # Update status label
        print("Bot paused.")
    else:
        pause_button.config(text="Pause")
        status_label.config(text="Clicker resumed.", fg="green")  # Update status label
        print("Bot resumed.")

def start_bot():
    global running
    if not running:
        running = True
        status_label.config(text="Clicker started.", fg="green")  # Update status label
        print("Starting the bot...")
        bot_thread = threading.Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()

def stop_bot():
    global running
    running = False
    status_label.config(text="Clicker stopped.", fg="red")  # Update status label
    print("Stopping the bot...")

def capture_button():
    global button_image
    print("Hover over the button you want to capture and press 'Enter'.")
    sleep(1)
    
    def on_enter(event):
        global button_image
        mouse_x, mouse_y = pyautogui.position()
        
        region_size = 100
        left = mouse_x - region_size // 2
        top = mouse_y - region_size // 2
        right = mouse_x + region_size // 2
        bottom = mouse_y + region_size // 2
        
        button_image = np.array(ImageGrab.grab(bbox=(left, top, right, bottom)))

        # Display the captured image to confirm it was captured correctly
        # cv2.imshow("Captured Button", button_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        status_label.config(text="Button image captured successfully!", fg="green")  # Update status label
        print("Button image captured!")

    root.bind('<Return>', on_enter)

def locate_button():
    global button_image
    if button_image is None:
        print("No button image captured. Please capture the button first.")
        return None
    
    screen = np.array(ImageGrab.grab())  # Capture the screen
    result = cv2.matchTemplate(screen, button_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"Max Value (Confidence): {max_val}")  # confidence level for debug
    threshold = 0.7
    if max_val >= threshold:
        return max_loc
    return None

def click_button(location):
    global button_image
    if button_image is None:
        print("No button image captured. Cannot click.")
        return
    
    button_width, button_height = button_image.shape[1], button_image.shape[0]
    center_x = location[0] + button_width // 2
    center_y = location[1] + button_height // 2
    
    print(f"Clicking at: ({center_x}, {center_y})")  # Debug print to check where the click will happen
    pyautogui.moveTo(center_x, center_y, duration=1)
    pyautogui.click()

def run_bot():
    global running, click_delay
    while running:
        if not paused:
            location = locate_button()
            if location:
                print("Button found! Clicking...")
                click_button(location)
                sleep(click_delay)
            else:
                print("Button not found, waiting...")
            sleep(0.5)
        else:
            sleep(0.1)

def create_gui():
    global pause_button, delay_entry, status_label
    
    global root
    root = tk.Tk()
    root.title("Auto Clicker")
    root.geometry("650x1100")

    tk.Label(root, text="Auto Clicker", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Status label to display capture status
    tk.Label(root, text="Status:").pack(pady=10)
    status_label = tk.Label(root, text="")
    status_label.pack(pady=10)

    tk.Label(root, text="Hover over selected area and click 'enter' to capture").pack(pady=10)
    tk.Label(root, text="area while this window is on top of other windows").pack(pady=10)
    capture_button_widget = tk.Button(root, text="Capture", command=capture_button)
    capture_button_widget.pack(pady=20)
    
    start_button = tk.Button(root, text="Start", command=start_bot)
    start_button.pack(pady=20)
    
    stop_button = tk.Button(root, text="Stop", command=stop_bot)
    stop_button.pack(pady=20)
    
    pause_button = tk.Button(root, text="Pause", command=toggle_pause)
    pause_button.pack(pady=20)
    
    # Delay input field
    tk.Label(root, text="Set Click Delay (seconds):").pack(pady=10)
    delay_entry = tk.Entry(root)
    delay_entry.insert(0, "15")
    delay_entry.pack(pady=5)
    
    def update_delay():
        global click_delay
        try:
            click_delay = float(delay_entry.get())
            print(f"Click delay set to: {click_delay} seconds")
        except ValueError:
            print("Invalid input for delay. Please enter a number.")

    delay_button = tk.Button(root, text="Update Delay", command=update_delay)
    delay_button.pack(pady=5)

    tk.Label(root, text="").pack(pady=5)
    tk.Label(root, text="Auto Clicker by Wong Zheng Jie").pack(pady=10)
    tk.Label(root, text="Github: https://github.com/WZhengJie99").pack(pady=10)
    tk.Label(root, text="Email: wzhengjie99@gmail.com").pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()

if __name__ == "__main__":
    create_gui()
