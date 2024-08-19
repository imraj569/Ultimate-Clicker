from keyboard import press_and_release, add_hotkey
from time import sleep
import pyautogui
import tkinter as tk

# Define a flag to check if the script is running
is_running = False

def manual_clicks():
    global is_running
    if not is_running:
        return  # Prevent execution if the script is not running
    
    # Commented-out script actions
    """
    sleep(5)
    pyautogui.click(x=830, y=1040)
    sleep(2)
    press_and_release('h')
    sleep(3)
    press_and_release('e')
    sleep(2)
    press_and_release('l')
    sleep(4)
    press_and_release('l')
    sleep(1)
    press_and_release('o')
    sleep(1)
    press_and_release('enter')
    """
    print("Script actions would be executed here...")

def update_status(label, status):
    label.config(text=f"Status: {status}")
    label.update_idletasks()

def play_script(status_label):
    global is_running
    is_running = True
    update_status(status_label, "Running")
    manual_clicks()
    update_status(status_label, "Finished")

def reset_script(status_label):
    global is_running
    is_running = False
    update_status(status_label, "Reset")
    print("Script has been reset.")

def show_banner():
    root = tk.Tk()
    root.geometry("400x150")
    root.title("Script Controller")
    root.attributes('-topmost', True)

    status_label = tk.Label(root, text="Status: Ready", font=("Helvetica", 12))
    status_label.pack(pady=10)

    # Frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    play_button = tk.Button(button_frame, text="Play", command=lambda: play_script(status_label), font=("Helvetica", 12))
    play_button.pack(side=tk.LEFT, padx=5)

    reset_button = tk.Button(button_frame, text="Reset", command=lambda: reset_script(status_label), font=("Helvetica", 12))
    reset_button.pack(side=tk.LEFT, padx=5)

    instructions_label = tk.Label(root, text="Press Alt+M to start the script\nPress Alt+R to reset the script", font=("Helvetica", 10))
    instructions_label.pack(pady=20)

    root.mainloop()

def start_script():
    show_banner()
    # Set the hotkeys to start and reset the script
    add_hotkey('alt+m', lambda: play_script(None))
    add_hotkey('alt+r', lambda: reset_script(None))

if __name__ == "__main__":
    start_script()
