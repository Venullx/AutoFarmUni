# AutoFarmUni - User Guide

## Description

**AutoFarmUni** is an automated tool for completing missions with friends automatically in `Unison League` using the `Bluestacks` Emulator.

## Requirements

- Python 3.7 or higher
- Python Libraries:
  - `Pillow` for image manipulation
  - `numpy` for array operations
  - `tkinter` for graphical interface
  - `subprocess` for executing external scripts
- `adb` (Android Debug Bridge) installed and configured
- Android device connected via USB with USB debugging enabled

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Venullx/AutoFarmUni

2. **Install dependencies:**
     ```bash
     pip install -r requirements.txt

## Project Structure
`src/`
* `actions.py`: For comparing images and performing actions based on comparisons.
* `click.py`: For cropping captured images.
* `cut.py`:  For listing connected Android devices.
* `finddevice.py` For capturing screenshots from the device.
* `matchimage.py` For comparing two images to determine if they are identical.
* `printscreen.py`: For capturing screenshots from the device.

`images/`
* `base/`: Directory containing base images for comparison.
* `screenshots/`: Directory where screenshots will be stored.
* `screenshots/cropped`: Directory for storing cropped screenshots after image processing.

## Usage
1. **Configure the Bluestacks Emulator**

   Launch the emulator, click on `Settings > Advanced`, and enable `Android Debug Bridge (ADB)`.

   Still in the settings, go to `Display`, under video resolution, select `Custom` and set the resolution to `480x840`.


2. **Start the application**
Run the `main.py` script:
    ```bash
    python main.py

Start the application:

Click the `Start` button to initialize the application.
Click the `Find devices` button to list connected Android devices.

### Select a device:

From the list of devices, double-click on the desired device to select it.

### Start screenshot capture:

After selecting a device, click the `Start` button to begin.

### Exit the application:

Click the `Exit` button to close the application and cancel any ongoing operations.
