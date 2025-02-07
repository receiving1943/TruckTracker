# Truck Tracker

## Overview
The **Truck Tracker** application is designed to track the pickup and delivery status of a truck in real-time. This application allows users to enter key information such as the **Truck Type**, **Shipper ID**, and **City**, and start tracking the truck's status. The application uses a web scraping mechanism via Selenium to retrieve tracking information, including current location and expected delivery times, and updates the user interface accordingly.

The application is built using **PyQt5** for the graphical user interface (GUI), **Selenium** for web scraping, and **threading** to handle long-running processes.

## Features
- Input fields for **Truck Type**, **City**, and **Shipper ID**.
- Start button to initiate the tracking process.
- Real-time updates of the truck's current location and status.
- Periodic updates every 5 minutes to check if the truck has been picked up.
- Visual alert (beep) if the truck is expected to arrive soon.
- Displays status messages about whether the truck has been delivered or not.

## Requirements
Ensure you have the following dependencies installed:

- **Python 3.x**
- **Selenium** - Used for web scraping to get truck tracking information.
- **PyQt5** - Provides the GUI framework.
- **WebDriver for Chrome** - Ensure you have the Chrome WebDriver installed for Selenium.
- **Windows Sound** (for beeping notifications).

Install the dependencies using `pip`:
```bash
pip install selenium pyqt5
