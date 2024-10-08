import pyautogui
import keyboard
import tkinter as tk
from tkinter import simpledialog, messagebox
from random import uniform  # Changed to `uniform` for float range
import subprocess,os

class MouseRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse & Keyboard Recorder")
        self.root.geometry("910x250")  # Adjusted to fit new button
        self.root.attributes('-topmost', True)  # Keep window on top

        # Mouse position and click count labels
        self.label_position = tk.Label(root, text="Mouse Position: ")
        self.label_position.pack(pady=5)

        self.label_clicks = tk.Label(root, text="Total Clicks: 0")
        self.label_clicks.pack(pady=5)

        # Status label
        self.label_status = tk.Label(root, text="Status: Idle")
        self.label_status.pack(pady=5)

        # Frame for buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # Help button
        self.button_help = tk.Button(self.button_frame, text="Help", command=self.show_instructions)
        self.button_help.grid(row=0, column=0, padx=5)

        # Set Sleep Time button
        self.button_set_sleep = tk.Button(self.button_frame, text="Set Mouse Sleep Time", command=self.set_sleep_time)
        self.button_set_sleep.grid(row=0, column=1, padx=5)

        # Set Keyboard Sleep Time button
        self.button_set_keyboard_sleep = tk.Button(self.button_frame, text="Set Keyboard Sleep Time", command=self.set_keyboard_sleep_time)
        self.button_set_keyboard_sleep.grid(row=0, column=2, padx=5)

        # Save button
        self.button_save = tk.Button(self.button_frame, text="Save Recorded Data", command=self.save_clicks)
        self.button_save.grid(row=0, column=3, padx=5)

        # Reset button
        self.button_reset = tk.Button(self.button_frame, text="Reset", command=self.reset)
        self.button_reset.grid(row=0, column=4, padx=5)

        # Record/Stop Keyboard button
        self.button_record_keyboard = tk.Button(self.button_frame, text="Record Keyboard", command=self.toggle_keyboard_recording)
        self.button_record_keyboard.grid(row=0, column=5, padx=5)

        # New buttons
        self.button_open_notepad = tk.Button(self.button_frame, text="Check Records", command=self.open_notepad)
        self.button_open_notepad.grid(row=1, column=1, padx=0, pady=5)  # Adjust padx for gap

        self.button_auto_clicker = tk.Button(self.button_frame, text="Start Auto Clicker", command=self.start_auto_clicker)
        self.button_auto_clicker.grid(row=1, column=2, padx=5, pady=5)  # Adjust padx for gap


        self.total_clicks = 0
        self.click_positions = []
        self.keyboard_records = []
        self.min_sleep = 1.0
        self.max_sleep = 5.0
        self.min_keyboard_sleep = 1.0  # Default keyboard sleep time
        self.max_keyboard_sleep = 5.0  # Default keyboard sleep time

        self.recording_keyboard = False
        self.current_modifiers = {key: False for key in ['ctrl', 'shift', 'alt']}  # Initialize modifier keys state
        self.update_mouse_position()
        self.bind_keys()

    def update_mouse_position(self):
        x, y = pyautogui.position()
        self.label_position.config(text=f"Mouse Position: {x}, {y}")
        self.root.after(100, self.update_mouse_position)

    def bind_keys(self):
        keyboard.add_hotkey('alt+s', self.save_click)
        keyboard.add_hotkey('esc', self.exit_program)
        if self.recording_keyboard:
            keyboard.hook(self.record_keyboard)

    def show_instructions(self):
        instructions = (
            "Instructions:\n"
            "1. Move the mouse to the desired position.\n"
            "2. Press 'Alt + S' to save the current mouse position.\n"
            "3. Press 'Esc' to exit and save the recorded data.\n"
            "4. Min 1 sec and Max 5 sec is the default wait time\n"
            "5. Click 'Set Mouse Sleep Time' to specify the range of sleep times between mouse clicks.\n"
            "6. Click 'Set Keyboard Sleep Time' to specify the range of sleep times between keyboard presses.\n"
            "7. Click 'Record Keyboard' to start or stop recording keyboard events."
        )
        messagebox.showinfo("Help", instructions)

    def set_sleep_time(self):
        try:
            min_sleep = simpledialog.askfloat("Set Mouse Sleep Time", "Enter minimum sleep time (seconds):", initialvalue=self.min_sleep)
            max_sleep = simpledialog.askfloat("Set Mouse Sleep Time", "Enter maximum sleep time (seconds):", initialvalue=self.max_sleep)

            if min_sleep is not None and max_sleep is not None:
                if min_sleep > max_sleep:
                    raise ValueError("Min sleep time should not be greater than max sleep time.")
                self.min_sleep = min_sleep
                self.max_sleep = max_sleep
                print(f"Mouse sleep time range set to {self.min_sleep} to {self.max_sleep} seconds.")
            else:
                print("Mouse sleep time setting was canceled.")

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Invalid input: {e}")

    def set_keyboard_sleep_time(self):
        try:
            min_sleep = simpledialog.askfloat("Set Keyboard Sleep Time", "Enter minimum keyboard sleep time (seconds):", initialvalue=self.min_keyboard_sleep)
            max_sleep = simpledialog.askfloat("Set Keyboard Sleep Time", "Enter maximum keyboard sleep time (seconds):", initialvalue=self.max_keyboard_sleep)

            if min_sleep is not None and max_sleep is not None:
                if min_sleep > max_sleep:
                    raise ValueError("Min sleep time should not be greater than max sleep time.")
                self.min_keyboard_sleep = min_sleep
                self.max_keyboard_sleep = max_sleep
                print(f"Keyboard sleep time range set to {self.min_keyboard_sleep} to {self.max_keyboard_sleep} seconds.")
            else:
                print("Keyboard sleep time setting was canceled.")

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Invalid input: {e}")

    def save_click(self):
        if not self.recording_keyboard:
            x, y = pyautogui.position()
            self.click_positions.append((x, y))
            self.total_clicks += 1
            self.label_clicks.config(text=f"Total Clicks: {self.total_clicks}")
            self.label_status.config(text="Status: Click Saved")
        else:
            self.label_status.config(text="Status: Cannot save click while recording keyboard.")

    def save_clicks(self):
        with open('recorded_data.txt', 'w') as file:
            for x, y in self.click_positions:
                sleep_time = uniform(self.min_sleep, self.max_sleep)
                file.write(f"sleep({sleep_time:.2f})\n")
                file.write(f"click(x={x}, y={y})\n")
            for record in self.keyboard_records:
                sleep_time = uniform(self.min_keyboard_sleep, self.max_keyboard_sleep)
                file.write(f"sleep({sleep_time:.2f})\n")
                file.write(f"{record}\n")
        print("Data recorded and saved to 'recorded_data.txt'.")
        self.label_status.config(text="Status: Data Saved")

    def reset(self):
        self.click_positions = []
        self.keyboard_records = []
        self.total_clicks = 0
        self.label_clicks.config(text="Total Clicks: 0")
        self.label_status.config(text="Status: Reset")

    def toggle_keyboard_recording(self):
        if self.recording_keyboard:
            self.recording_keyboard = False
            self.button_record_keyboard.config(text="Record Keyboard")
            keyboard.unhook_all()  # Stop recording keyboard events
            print("Stopped recording keyboard events.")
            self.bind_keys()  # Rebind mouse click hotkey
        else:
            self.recording_keyboard = True
            self.button_record_keyboard.config(text="Stop Keyboard")
            keyboard.hook(self.record_keyboard)  # Start recording keyboard events
            print("Started recording keyboard events.")

    def record_keyboard(self, event):
        if event.event_type == 'down':  # Only record keydown events
            if event.name in self.current_modifiers:  # Check for modifier keys
                # Store modifier key state
                self.current_modifiers[event.name] = True
            else:
                # Combine with any active modifier keys
                combined_keys = '+'.join([key for key, pressed in self.current_modifiers.items() if pressed] + [event.name])
                self.keyboard_records.append(f"press_and_release('{combined_keys}')")
                self.label_status.config(text=f"Status: Key '{combined_keys}' Recorded")
        elif event.event_type == 'up':
            if event.name in self.current_modifiers:
                # Reset the modifier key state on release
                self.current_modifiers[event.name] = False

    def open_notepad(self):
        try:
            file_path = 'recorded_data.txt'
            if os.path.exists(file_path):
                os.startfile(file_path)  # Open file in default application (Notepad)
            else:
                messagebox.showerror("Error", "Recorded data file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

    def start_auto_clicker(self):
        try:
            script_path = 'Auto_clicks.pyw'
            if os.path.exists(script_path):
                subprocess.Popen(['pythonw', script_path])  # Start the auto clicker script
            else:
                messagebox.showerror("Error", "Auto Clicker script not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start auto clicker: {e}")


    def exit_program(self):
        if self.recording_keyboard:
            self.toggle_keyboard_recording()  # Save and stop recording if necessary
        self.save_clicks()  # Save all recorded data
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseRecorder(root)
    root.mainloop()
