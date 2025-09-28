pico-w-bluetooth-weather

# Pico W Bluetooth Temp Plotter 

Welcome to Pico W tutorial

See it in action
![](./images/temp_example.mp4)


## Steps to Run:

### Pico W

There are 2 ways to run. Using low level library or using high level library. The steps for the deployment for both are similar.
One is available in `src\bluetooth_way` and the other is `src\aioble_way`

Steps
- Connect to pico w via Thonny
- Install Micropython
- Upload the files in the `src\<pico>` directory to the microcontroller (see above).
- (Optional) Start main.py
- Restart the device


### PC
- Enable Bluetooth
- Open `src\local\tempPlotter.html` in Chrome (or any other web-bluetooth supported browser)
- Follow the steps mentioned on the webpage
