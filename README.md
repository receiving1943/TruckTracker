# Truck Tracker

## Overview
The **Truck Tracker** application is a desktop GUI tool designed to monitor the pickup and delivery status of trucks in real-time. Built with **PyQt5** for the user interface and **Selenium** for web scraping, it allows users to input key information such as **Truck Type**, **Shipper ID**, and **City**, then start tracking the truck's status. The application continuously retrieves tracking data from the JB Hunt tracking website, including current location and estimated times, updating the interface accordingly.

The tracker performs periodic checks every 5 minutes to see if the truck has been picked up or delivered, providing real-time updates and alerts when the truck is nearing its expected arrival time.

---

## Features
- Input fields for **Truck Type**, **City**, and **Shipper ID**.
- A **Start Tracking** button to initiate the monitoring process.
- Real-time display of the truck's current location and last update time.
- Periodic status checks every 5 minutes during active tracking.
- Visual alerts (beep sound) when the truck is close to its expected arrival time.
- Clear status messages indicating if the truck has been delivered or is still en route.

---

## Requirements
Ensure you have the following dependencies installed:

- **Python 3.x**
- **Selenium** - For web scraping and retrieving tracking information.
- **PyQt5** - For the GUI interface.
- **Chrome WebDriver** - Download from [here](https://sites.google.com/chromium.org/driver/) compatible with your Chrome version.
- **winsound** (Windows only) - For notification sounds.

## Installation
1. Clone or download this repository.
2. Install the required Python packages:

```bash
pip install selenium pyqt5
```
Download the appropriate ChromeDriver for your Chrome version from here.
Place chromedriver.exe in the same directory as your script or ensure it's accessible via your system PATH.
Ensure the truck.ico icon file is in the same directory, or update the icon path in the script.
Usage
Run the script with Python:

CopyRun
python your_script_name.py
This will open the GUI window. Enter the Truck Type, City, and Shipper ID, then click Start Tracking. The application will begin monitoring the truck's status, updating the display and alerting you as the truck approaches its expected time.

Notes
The script uses headless Chrome; ensure ChromeDriver matches your Chrome browser version.
The beeping notification uses winsound and works on Windows. For other OS, modify the beep functionality accordingly.
The tracking loop performs checks every 5 minutes, with more frequent updates (every minute) during active monitoring.
Make sure to have the truck.ico icon file in the script directory or update the icon path.
License
This project is provided as-is. Feel free to customize, improve, or adapt it to your needs.