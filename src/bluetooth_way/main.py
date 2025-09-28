import bluetooth
from ble_advertising import advertising_payload
from temp_sensor import Temperature
import asyncio
from led_control import LEDControl

class BLEWiFiService:
    SERVICE_UUID = bluetooth.UUID("0094b196-ffb7-48bd-b5ea-18bf7e5a6dba")
    TEMP_CHARACTERISTIC_UUID = bluetooth.UUID("712f3291-7523-4cc2-879a-7babd68153d4")

    _IRQ_CENTRAL_CONNECT = const(1)
    _IRQ_CENTRAL_DISCONNECT = const(2)
    _IRQ_GATTS_WRITE = const(3)
    _IRQ_GATTS_READ_REQUEST = const(4)
  
    _FLAG_READ = const(0x0002)

    TEMP_CHARACTERISTIC = (
      TEMP_CHARACTERISTIC_UUID,
      _FLAG_READ,
    )

    SERVICE = (
      SERVICE_UUID,
      (TEMP_CHARACTERISTIC,)
    )

    def __init__(self):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self.irq_handler)
        self._temp = Temperature()
        self._led = LEDControl()

    def start_advertising(self):
        # Use the helper function to create the GAP advertising payload
        payload = advertising_payload(name="Pico", services=[self.SERVICE_UUID])
      
        # Register our custom GATTS service
        ((self._temp_char),) = self._ble.gatts_register_services((self.SERVICE,))
      
        print("Advertising")
        # Start advertising using the GAP payload, every 500000ms=0.5s
        self._ble.gap_advertise(500000, adv_data=payload)

        self._led.blink()
      
    def stop_advertising(self):
        print("Stopped Advertising")
        self._led.stop_blink()
        self._ble.gap_advertise(None)

    def irq_handler(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            print("Device connected")
            self.stop_advertising()
        elif event == _IRQ_CENTRAL_DISCONNECT:
            print("Device disconnected")
            # Start advertising again to allow a new connection.
            self.start_advertising()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, attr_handle = data
            self.receive_write_handler(attr_handle)
        elif event == _IRQ_GATTS_READ_REQUEST:
            conn_handle, attr_handle = data
            self.receive_read_handler(attr_handle)

    def receive_write_handler(self, attr_handle):
        pass

    def receive_read_handler(self, attr_handle):
        temp = self._temp.ReadTemperature()
        print("Reading Temp " + str(temp))
        self._ble.gatts_write(attr_handle, str(temp).encode())

        
ble_wifi_service = BLEWiFiService()
ble_wifi_service.start_advertising()
