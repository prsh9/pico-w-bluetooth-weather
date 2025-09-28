from machine import Timer, Pin

class LEDControl:
    def __init__(self):
        self.led = Pin("WL_GPIO0", Pin.OUT)
        self.blinktimer = None

    def on(self):
        self.led.on()
        
    def off(self):
        self.led.off()
        
    def led_toggle(self, t):
        self.led.toggle()

    def blink(self, period=500):
        if self.blinktimer is not None:
            return
        
        self.blinktimer = Timer()
        self.blinktimer.init(mode=Timer.PERIODIC, period=period, callback=self.led_toggle)

    def stop_blink(self):
        if self.blinktimer is None:
            return
        self.blinktimer.deinit()
        self.off()
        self.blinktimer = None