---

# Ultimate-Clicker 🚀

Welcome to **Ultimate-Clicker**! This project features Python scripts designed for automating mouse and keyboard actions, recording user interactions, and managing automated tasks. The suite includes tools for manual clicking, automatic execution of recorded clicks, and recording mouse and keyboard events.

## Overview

The project consists of three main scripts:

1. **`manual_clicker.py`**: Provides a basic script controller with play and reset functionalities using `tkinter` and `keyboard` hotkeys. 🎛️
2. **`auto_clicker.py`**: Executes mouse clicks and keyboard actions based on commands read from a file. Includes a GUI to manage execution. 🖱️
3. **`record_clicks.py`**: A comprehensive tool to record mouse clicks and keyboard events, save them, and configure sleep times between actions. 📝

## Installation

To get started, ensure you have the required packages installed. Use `pip` to install them:

```bash
pip install pyautogui keyboard tkinter
```

## Usage

### `manual_clicker.py`

This script offers a simple GUI to control script execution. 

**Features:**
- **Play Button**: Starts the script execution. ▶️
- **Reset Button**: Resets the script to its initial state. 🔄

**Hotkeys:**
- `Alt+M`: Start the script.
- `Alt+R`: Reset the script.

### `auto_clicker.py`

Run this script to execute mouse clicks and keyboard actions based on a file's commands. 

**Features:**
- **Play/Pause Button**: Starts or stops the execution of recorded commands. ⏯️
- **Repetition Button**: Set the number of repetitions for executing the script. 🔁
- **Reset Button**: Resets the execution and sets the status to paused. 🔄

**Commands Format:**
- `sleep(X)`: Sleeps for X seconds.
- `click(x=Y, y=Z)`: Clicks at the coordinates (Y, Z).
- `press_and_release('KEY')`: Presses and releases the specified key.

### `record_clicks.py`

This script helps you record mouse clicks and keyboard events, save them, and adjust sleep times.

**Features:**
- **Record Keyboard**: Toggle recording of keyboard events. ⌨️
- **Save Recorded Data**: Save recorded mouse and keyboard actions to a file. 💾
- **Set Sleep Time**: Configure the range of sleep times between clicks. ⏲️
- **Help Button**: Get instructions for using the application. ❓

**Hotkeys:**
- `Alt+S`: Save the current mouse position.
- `Esc`: Exit and save recorded data.

## Examples

1. **Start Recording:**

   Run `record_clicks.py` and use the "Record Keyboard" button to start recording. Click "Save Recorded Data" to save your actions to `recorded_data.txt`.

2. **Execute Recorded Commands:**

   Use `auto_clicker.py` with the `recorded_data.txt` file to execute the recorded actions. Adjust repetitions as needed.

## Contributing

We welcome contributions! Feel free to open issues or submit pull requests to improve the project. 💡

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 📜

## Contact

For any questions or suggestions, reach out via [GitHub Profile](https://github.com/imraj569/). 📫

---