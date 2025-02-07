import os
import sys
import random
import time as t
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QStatusBar, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout, QSizePolicy
from threading import Thread
import winsound as ws
from datetime import datetime, date, time



class TruckTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Truck Tracker")
        self.setGeometry(100, 100, 400, 200)

        # Layouts
        layout = QVBoxLayout()
        hlayout1 = QHBoxLayout()
        hlayout2 = QHBoxLayout()
        layout.addLayout(hlayout1)
        layout.addLayout(hlayout2)

        # Input for Truck Type
        self.truck_type_input = QLineEdit(self)
        self.truck_type_input.setPlaceholderText("Please Enter Type of Truck")
        hlayout1.addWidget(self.truck_type_input)
        
        # Input for City
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Please Enter City")
        hlayout1.addWidget(self.city_input)

        # Input for Shipper ID
        self.shipper_id_input = QLineEdit(self)
        self.shipper_id_input.setPlaceholderText("Please Enter Shipper ID")
        hlayout2.addWidget(self.shipper_id_input)

        # Button to start tracking
        self.track_button = QPushButton("Start Tracking", self)
        self.track_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.track_button.setMinimumWidth(160)  # Set to minimum desired width, adjust as necessary
        
        # Set a fixed height (you can adjust this value)
        self.track_button.setFixedHeight(self.shipper_id_input.sizeHint().height())
        
        self.track_button.clicked.connect(self.start_tracking)
        hlayout2.addWidget(self.track_button)

        # Status display
        self.status_label = QLabel("Status: Waiting for input...", self)
        layout.addWidget(self.status_label)

        # Current location display
        self.location_label = QLabel("Status: Waiting for input...", self)
        layout.addWidget(self.location_label)
        
        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Central widget
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_tracking(self):
        truck_type = self.truck_type_input.text()
        shipper_id = self.shipper_id_input.text()
        city_check = self.city_input.text()

        if not truck_type or not shipper_id or not city_check:
            self.status_label.setText("Please enter Truck Type, Shipper ID, and City.")
            return

        self.status_label.setText("Tracking started...")
        self.location_label.setText('Finding Location...')
        self.tracking_thread = Thread(target=self.pickup_check, args=(truck_type, shipper_id, city_check))
        self.tracking_thread.start()

    def pickup_check(self, truck_type, shipper_id, city_check):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--headless')
        options.add_argument('--log-level=1')
        options.add_argument('--incognito')
        options.add_argument('--disable-gpu')
        
        beep_count = 0

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 60)
        track_link = f'https://www.jbhunt.com/track-shipments/?k=shipperId&v={shipper_id}'
        driver.get(track_link)
        
        try:
                   
            keep_running = True
            # def pickUpCheck(shipID): # Function to check if truck has been picked up and output if it has been or not. If it has outputs the expected time.
            while keep_running == True:
                count = 1
                try:
                    current_location = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div[2]/span')))
                    self.location_label.setText(f'Current Location: {current_location.text}')
                except TimeoutException:
                    self.location_label.setText('')
                city = wait.until(EC.visibility_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[{count}]/div[3]')))
                if 'Estimated delivery' in city.text:
                    city = wait.until(EC.visibility_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[{count}]/div[2]')))
                while f'{city_check}' not in city.text:
                    count +=1
                    # print(count)
                    city = wait.until(EC.visibility_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[{count}]/div[3]')))
                    if 'Estimated delivery' in city.text or 'Completed' in city.text:
                        # print(city.text,' prev')
                        city = wait.until(EC.visibility_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[{count}]/div[2]')))
                        # print(city.text, ' post')
                self.status_label.setText(f'Checking if picked up...')
                # print(city.text)
                try:
                    expecPic = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[1]/div[4]')))
                except TimeoutException:
                    expecPic = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[1]/div[3]')))
                if 'at' in expecPic.text:
                        expecPic = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[1]/div[4]')))
                while 'Estimated Pickup' in expecPic.text and keep_running:
                    now = datetime.now()
                    curr_time = now.strftime("%I:%M %p")
                    self.status_label.setText(f"{truck_type} truck not picked up as of {curr_time}. Checking again in 5 minutes.")
                    for i in range(300, 0, -1):
                        t.sleep(1)
                        self.status_bar.showMessage(f"Time until next check: {i} seconds")
                        if i == 1:
                            driver.refresh()
                    try:
                        expecPic = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[1]/div[4]')))
                    except TimeoutException:
                        expecPic = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[1]/div[3]')))
                    if 'at' in expecPic.text:
                        expecPic = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[1]/div[4]')))
                else: 
                    try:
                        expectedTime = wait.until(EC.visibility_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[{count}]/div[5]')))
                    except TimeoutException:
                        expectedTime = wait.until(EC.visibility_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[{count}]/div[4]')))
                    now = datetime.now()
                    curr_time = now.strftime("%I:%M %p")
                    expected_time_strip = datetime.strptime(expectedTime.text[3:], "%I:%M %p")
                    expected_time_strip_today = datetime.combine(date.today(), expected_time_strip.time())
                    if abs((expected_time_strip_today - datetime.now()).total_seconds()) <= 300:  # 300 seconds = 5 minutes
                        if(beep_count ==0):
                            freq=850
                            dur=1000
                            ws.Beep(freq,dur)
                            beep_count +=1
                            # break
                    # print(f'The {truck_type.upper()} truck is expected {expectedTime.text}')
                        # Include update of the self.status_label with truck expected time like:
                    if expected_time_strip_today < datetime.now() and f'{city_check}' in current_location.text :
                        self.status_label.setText(f'The {truck_type} truck has been delivered.')
                        self.location_label.setText('')
                        self.status_bar.showMessage("")
                        driver.quit()
                        keep_running = False
                        break
                    expected_time = expectedTime.text
                    self.status_label.setText(f'The {truck_type} truck is expected {expected_time}')
                    current_location = wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[1]/div[2]/div/div[2]/div[2]/span')))
                    self.location_label.setText(f'Current Location: {current_location.text}')
                    if keep_running == True:
                        for i in range(60, 0, -1):
                            t.sleep(1)
                            self.status_bar.showMessage(f"Time until next check: {i} seconds")
                            if i == 1:
                                driver.refresh()
                            try:
                                expectedTime = wait.until(EC.visibility_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[{count}]/div[5]')))
                            except TimeoutException:
                                expectedTime = wait.until(EC.visibility_of_element_located((By.XPATH,f'/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/ol/li[{count}]/div[4]')))
                    
                if not keep_running:
                    break    
        except TimeoutException:
            self.status_label.setText("Could not retrieve expected time. Please click Start Tracking again.")
            driver.quit()
        # driver.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = TruckTracker()
    tracker.show()
    sys.exit(app.exec_())