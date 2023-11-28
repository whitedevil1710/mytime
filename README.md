# Time Tracking Utility

This utility comprises Python and Bash scripts designed to track work time, monitor breaks, and install necessary dependencies for the time-tracking functionality.

## Features

- **Python Script (`main.py`):**
  - Monitors work time considering screen lock periods and breaks.
  - Uses `Tkinter` for creating pop-up windows.
  - Utilizes a custom module `lock.py` to check the screen lock status.
  - Displays time-related information continuously in the terminal.
  
- **Bash Script (`setup.sh`):**
  - Install the required `gnome-screensaver` package if not present.
  - Install the necessary Python packages (`python3-tk`) for the Python script to execute.
  - Creates an executable file (`mytime`) that executes the `main.py` Python script.
  - Provides user instructions after successful installation.

## Requirements

- Python 3.x
- `gnome-screensaver` package
- `Tkinter` for Python GUI (installed via `python3-tk`)

## Installation

To install the time-tracking utility, follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/time-tracking.git
    ```
1. Navigate to the project directory:
    ```bash
    cd time-tracking
    ```
1. Run the setup script:
   ```bash
   bash setup.sh
   ```
This script will check for necessary dependencies and install missing ones. It will also create an executable (mytime) to start the time-tracking utility.

## Usage

Once the installation is complete, execute the following command to start the time-tracking utility:

```bash
mytime
```

This will initiate the time-tracking application, which will continuously display work time, break time, start time, and current time in the terminal.

## Disclaimer

Please be cautious while executing system-level scripts. Verify the contents of the scripts to ensure they align with your requirements and review potential system modifications before running them on your system.

## Contributing

If you find issues or have suggestions for improvements, feel free to open an issue or create a pull request. Contributions are welcome!