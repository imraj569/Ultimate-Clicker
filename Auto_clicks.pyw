import pyautogui
from time import sleep
import threading
import tkinter as tk
from tkinter import simpledialog
import keyboard

class ClickExecutor:
    def __init__(self, filename):
        self.filename = filename
        self.running = False
        self.paused = False
        self.thread = None
        self.repetitions = 1
        self.lock = threading.Lock()  # Add a lock to manage state changes safely

    def execute_clicks(self):
        while self.repetitions > 0 and self.is_running():
            try:
                with open(self.filename, 'r') as file:
                    lines = file.readlines()

                for line in lines:
                    line = line.strip()
                    if not self.is_running():
                        break

                    while self.is_paused():
                        sleep(0.1)

                    if line.startswith('sleep'):
                        try:
                            delay = float(line.split('(')[1].split(')')[0])
                            self.display_delay(delay)
                            sleep(delay)
                        except (IndexError, ValueError):
                            print(f"Invalid sleep command: {line}")
                    elif line.startswith('click'):
                        try:
                            coords = line.split('(')[1].split(')')[0]
                            x, y = [int(coord.split('=')[1]) for coord in coords.split(',')]
                            pyautogui.click(x=x, y=y)
                            print(f"Clicked at ({x}, {y})")
                        except (IndexError, ValueError):
                            print(f"Invalid click command: {line}")
                    elif line.startswith('press_and_release'):
                        try:
                            keys = line.split('(')[1].split(')')[0].strip("'")
                            sleep(0.1)  # Add a small delay before pressing keys
                            keyboard.press_and_release(keys)
                            print(f"Pressed and released keys: {keys}")
                        except (IndexError, ValueError):
                            print(f"Invalid press_and_release command: {line}")
                    else:
                        print(f"Unknown command: {line}")

                self.repetitions -= 1
                self.update_remaining_repetitions(self.repetitions)
                sleep(0.1)  # Small delay to ensure UI updates

            except FileNotFoundError:
                print(f"File {self.filename} not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

        self.finish_execution()

    def is_running(self):
        with self.lock:
            return self.running

    def is_paused(self):
        with self.lock:
            return self.paused

    def display_delay(self, delay):
        delay_ms = int(delay * 1000)
        app.update_status(f"Next delay: {delay_ms} ms")

    def start(self):
        with self.lock:
            if not self.running:
                self.running = True
                self.paused = False
                self.thread = threading.Thread(target=self.execute_clicks)
                self.thread.start()

    def pause(self):
        with self.lock:
            self.paused = True

    def resume(self):
        with self.lock:
            self.paused = False

    def stop(self):
        with self.lock:
            self.running = False
            self.paused = False

    def set_repetitions(self, repetitions):
        with self.lock:
            self.repetitions = repetitions
            self.update_remaining_repetitions(self.repetitions)

    def reset(self):
        self.stop()
        if self.thread:
            self.thread.join()  # Ensure the thread finishes before resetting
        self.repetitions = 1
        app.update_status("Paused - Next delay: 0 ms")
        self.update_remaining_repetitions(self.repetitions)
        app.toggle_button.config(text="Play")

    def update_remaining_repetitions(self, repetitions_left):
        app.remaining_repetitions_label.config(text=f"Repetitions left: {repetitions_left}")

    def finish_execution(self):
        with self.lock:
            self.running = False
            self.paused = False
        app.update_status("Finished")
        app.toggle_button.config(text="Play")

class ClickApp:
    def __init__(self, root, executor):
        self.executor = executor
        
        # Keep window on top
        root.attributes('-topmost', True)
        
        # Set window size
        root.geometry('400x150')

        # Create a frame to hold the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Play/Stop button
        self.toggle_button = tk.Button(button_frame, text="Play", command=self.toggle)
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        # Repetition button
        self.repetition_button = tk.Button(button_frame, text="Repetition", command=self.set_repetitions)
        self.repetition_button.pack(side=tk.LEFT, padx=5)

        # Reset button
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(root, text="Status: Paused - Next delay: 0 ms")
        self.status_label.pack(pady=5)

        # Remaining repetitions label
        self.remaining_repetitions_label = tk.Label(root, text="Repetitions left: 1")
        self.remaining_repetitions_label.pack(pady=5)

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

    def update_remaining_repetitions(self, repetitions_left):
        self.remaining_repetitions_label.config(text=f"Repetitions left: {repetitions_left}")

    def toggle(self):
        if self.executor.is_running():
            self.executor.stop()
            self.toggle_button.config(text="Play")
            self.update_status("Paused")
        else:
            self.executor.start()
            self.toggle_button.config(text="Pause")
            self.update_status("Playing")

    def set_repetitions(self):
        repetitions = simpledialog.askinteger("Input", "Enter the number of repetitions:", minvalue=1)
        if repetitions is not None:
            if self.executor.is_running():
                self.executor.stop()  # Stop current execution if running
                self.executor.thread.join()  # Ensure the thread finishes before starting again
            self.executor.set_repetitions(repetitions)
            self.executor.start()  # Start the script with new repetitions
            self.toggle_button.config(text="Pause")
            self.update_status("Playing")

    def reset(self):
        self.executor.reset()
        self.update_status("Paused - Next delay: 0 ms")

if __name__ == "__main__":
    filename = 'recorded_data.txt'
    root = tk.Tk()
    root.title("Click Executor")

    executor = ClickExecutor(filename)
    app = ClickApp(root, executor)

    root.mainloop()
