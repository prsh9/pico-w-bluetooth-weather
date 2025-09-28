import uasyncio as asyncio
import aioble
import bluetooth
from temp_sensor import Temperature
from led_control import LEDControl

# UUIDs
SERVICE_UUID = bluetooth.UUID("0094b196-ffb7-48bd-b5ea-18bf7e5a6dba")
TEMP_CHARACTERISTIC_UUID = bluetooth.UUID("712f3291-7523-4cc2-879a-7babd68153d4")

# Hardware interfaces
temp_sensor = Temperature()
led = LEDControl()

# Define BLE service and characteristic
service = aioble.Service(SERVICE_UUID)
temp_char = aioble.Characteristic(
    service,
    TEMP_CHARACTERISTIC_UUID,
    read=True
)

# Register services
aioble.register_services(service)

async def update_temperature_on_connect(connection):
    while connection.is_connected():
        temp = temp_sensor.ReadTemperature()
        print("Updating characteristic value:", temp)
        temp_char.write(str(temp).encode())
        await asyncio.sleep(5)  # Adjust as needed

async def advertise_and_wait():
    while True:
        print("Advertising...")
        led.blink()

        # Advertise and wait for connection
        async with await aioble.advertise(
            interval_us=500_000,
            name="Pico",
            services=[SERVICE_UUID],
        ) as connection:

            print("Device connected")
            led.stop_blink()

            # Start updating the temperature value periodically
            await update_temperature_on_connect(connection)

        print("Device disconnected")

async def main():
    await advertise_and_wait()

# Start the asyncio loop
asyncio.run(main())
