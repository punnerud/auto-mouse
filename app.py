from pynput import mouse, keyboard
import time
import threading
import os
from AppKit import NSWorkspace

running = True
recording = False
sequence = []
last_click_time = 0
replay_speed = 4
initial_window = None
RECORDINGS_FILE = "recordings.txt"

def save_recording():
    with open(RECORDINGS_FILE, "w") as f:
        for x, y, delay, window_title in sequence:
            f.write(f"{x},{y},{delay},{window_title}\n")
    print(f"Recording saved to {RECORDINGS_FILE}")

def load_recording():
    if os.path.exists(RECORDINGS_FILE):
        with open(RECORDINGS_FILE, "r") as f:
            loaded_sequence = []
            for line in f:
                x, y, delay, window_title = line.strip().split(',', 3)
                loaded_sequence.append((float(x), float(y), float(delay), window_title))
            return loaded_sequence
    return None

def on_press(key):
    global running, recording, replay_speed
    if key == keyboard.Key.esc:
        print("Esc pressed. Exiting...")
        running = False
        return False
    elif hasattr(key, 'char') and key.char in '123456789':
        replay_speed = int(key.char)
        print(f"Replay speed changed to {replay_speed}x")

def get_active_window_title():
    active_app = NSWorkspace.sharedWorkspace().activeApplication()
    return active_app['NSApplicationName'] if active_app else "Unknown"

def on_click(x, y, button, pressed):
    global recording, sequence, last_click_time, initial_window
    if recording and pressed:
        current_time = time.time()
        window_title = get_active_window_title()
        if sequence:
            time_diff = current_time - last_click_time
            sequence.append((x, y, time_diff, window_title))
        else:
            sequence.append((x, y, 0, window_title))
            initial_window = window_title
        last_click_time = current_time
        print(f"Recorded click at ({x}, {y}) in window: {window_title}")

def perform_click(x, y):
    mouse_controller = mouse.Controller()
    mouse_controller.position = (x, y)
    mouse_controller.click(mouse.Button.left)

def replay_sequence():
    global sequence, running, replay_speed, initial_window
    if not sequence:
        print("No sequence recorded. Record a sequence first.")
        return
    
    print(f"Replaying sequence in loop at {replay_speed}x speed. Press Esc to stop. Use keys 1-9 to change speed.")
    while running:
        for i, (x, y, delay, window_title) in enumerate(sequence):
            if not running:
                break
            current_window = get_active_window_title()
            if current_window != window_title:
                print(f"Wrong window focus. Expected: {window_title}, Current: {current_window}")
                running = False
                break
            time.sleep(delay / replay_speed)
            perform_click(x, y)
            print(f"Click {i+1}/{len(sequence)} performed at ({x}, {y})")
        
        if not running:
            break
        print("Sequence completed. Restarting...")
    
    print("Replay stopped.")

def main():
    global running, recording, sequence, initial_window

    # Check for existing recording
    saved_sequence = load_recording()
    if saved_sequence:
        response = input("Found a saved recording. Do you want to use it? (y/n): ").lower()
        if response == 'y':
            sequence = saved_sequence
            print("Saved recording loaded.")

    print("Press 'r' to start/stop recording, 'p' to replay in loop, 1-9 to change speed, and 'Esc' to exit.")
    
    def on_press_local(key):
        global recording, sequence, running, initial_window, replay_speed
        if key == keyboard.Key.esc:
            print("Esc pressed. Exiting...")
            running = False
        elif hasattr(key, 'char'):
            if key.char == 'r':
                recording = not recording
                if recording:
                    sequence = []
                    initial_window = get_active_window_title()
                    print(f"Recording started in window: {initial_window}. Perform your click sequence.")
                else:
                    print("Recording stopped. Press 'p' to replay the sequence.")
                    save_recording()
            elif key.char == 'p':
                if not recording:
                    threading.Thread(target=replay_sequence).start()
            elif key.char in '123456789':
                replay_speed = int(key.char)
                print(f"\n\n\nReplay speed changed to {replay_speed}x\n\n\n")

    # Start listeners
    keyboard_listener = keyboard.Listener(on_press=on_press_local)
    mouse_listener = mouse.Listener(on_click=on_click)
    
    keyboard_listener.start()
    mouse_listener.start()

    while running:
        time.sleep(0.1)

    keyboard_listener.stop()
    mouse_listener.stop()

if __name__ == "__main__":
    main()
