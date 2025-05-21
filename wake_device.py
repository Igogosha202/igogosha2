import json
import sys
from wakeonlan import send_magic_packet

# Загрузка базы устройств
with open('devices.json', 'r', encoding='utf-8') as f:
    devices = json.load(f)

def wake_device(device_name):
    device = devices.get(device_name)
    if not device:
        print(f"Устройство '{device_name}' не найдено.")
        sys.exit(1)
    mac_address = device['mac']
    send_magic_packet(mac_address)
    print(f"Отправлен пакет Wake-on-LAN для {device_name} ({mac_address})")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python wake_device.py <имя_устройства>")
        sys.exit(1)
    device_name = sys.argv[1]
    wake_device(device_name)