# Auto Clicker with Recording and Replay

This Python script allows you to record and replay mouse click sequences on macOS. It's useful for automating repetitive tasks that involve clicking at specific locations on your screen.

## Features

- Record mouse click sequences with timing
- Replay recorded sequences in a loop
- Adjust replay speed on the fly (1x to 9x)
- Save and load recordings automatically
- Window-specific click sequences for accuracy

## Requirements

- Python 3.x
- macOS (uses AppKit for window detection)
- pynput library

## Installation

1. Clone this repository or download the `app.py` file.
2. Install the required library:
   ```
   pip install pynput
   ```

## Usage
```
   python app.py
   ```

Run the script using Python:

## How to Use

1. **Start the script**: Open a terminal, navigate to the directory containing `app.py`, and run the command above.


2. **Recording a sequence**:
   - Press `r` to start recording.
   - Perform your desired click sequence. Each click will be recorded with its position and timing.
   - Press `r` again to stop recording and save the sequence.

3. **Replaying a sequence**:
   - After recording or loading a sequence, press `p` to start replaying.
   - The sequence will loop continuously until stopped.
   - Ensure you're in the correct window when starting the replay.

4. **Adjusting replay speed**:
   - While replaying, press number keys 1-9 to change the replay speed (1x to 9x).
   - The new speed will be displayed in the console.

5. **Stopping the script**:
   - Press `Esc` at any time to stop the replay and exit the program.

### Commands Summary

- `r`: Start/stop recording
- `p`: Play the recorded sequence in a loop
- `1-9`: Change replay speed (1x to 9x)
- `Esc`: Exit the program