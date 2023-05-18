import asyncio
from bleak import BleakScanner, BleakClient

MODEL_NBR_UUID = "19b10001-e8f2-537e-4f6c-d104768a1214"


async def main():
    devices = await BleakScanner.find_device_by_name("Button Device")
    print(devices)
    async with BleakClient(devices.address) as client:
        value = bytes(await client.read_gatt_descriptor(MODEL_NBR_UUID))
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(str, model_number))))

asyncio.run(main())