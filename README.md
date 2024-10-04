# Auto-Clicker
A Auto Clicker that automates mouse clicking using a captured image.

## Features

- Button Image Capture: Hover over a button to capture its image for later use.
  
- Automated Clicking: The bot locates the captured button on the screen and clicks it at regular intervals.
  
- Adjustable Click Delay: Customize the delay between clicks using the built-in GUI.
  
- Start/Stop/Pause Controls: The bot can be started, paused, and stopped at any time.
  
- Status Indicator: The GUI provides real-time status updates, such as "Clicker paused", "Clicker resumed", and "Button image captured successfully".
  
## Tech Stack

- Python: Core language for the bot.
  
- PyAutoGUI: Handles mouse automation and GUI interaction.
  
- OpenCV: Used to match the button image on the screen.
  
- PIL: Captures images from the screen.
  
- Tkinter: Provides the graphical interface for user interaction.

# Installation and Setup
Download or clone the repository:
```
git clone https://github.com/WZhengJie99/Auto-Clicker.git
```
  
## How to Use

1. Install the required libraries:

```
pip install pyautogui opencv-python numpy pillow
```

2. Run the bot using the index.bat file or run with the command (index.bat file has to be in the same folder as index.py):

```
python index.py
```

3. Steps:

- Open the GUI.
- Click "Capture" to capture the button image.
  
- Set the click delay (default is 15 seconds).
  
- Click "Start" to begin the bot, and it will repeatedly click the captured button.
  
- Use the "Pause" button to temporarily stop clicking, or the "Stop" button to end the session entirely.
  
