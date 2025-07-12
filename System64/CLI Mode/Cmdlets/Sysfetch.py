import psutil
import platform
import socket
import os
import cpuinfo
from datetime import datetime

def get_cpu_info():
    cpu_info = {}
    cpu_info['Processor Name'] = cpuinfo.get_cpu_info()['brand_raw']
    cpu_info['Physical Cores'] = psutil.cpu_count(logical=False)
    cpu_info['Total Cores'] = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    if cpu_freq:
        cpu_info['Max Frequency (MHz)'] = cpu_freq.max
        cpu_info['Min Frequency (MHz)'] = cpu_freq.min
        cpu_info['Current Frequency (MHz)'] = cpu_freq.current
    return cpu_info

def get_memory_info():
    svmem = psutil.virtual_memory()
    memory_info = {
        'Total RAM (GB)': svmem.total / (1024 ** 3),
        'Available RAM (GB)': svmem.available / (1024 ** 3),
        'Used RAM (GB)': svmem.used / (1024 ** 3),
        'RAM Usage (%)': svmem.percent,
    }
    return memory_info

def get_storage_info():
    partitions = psutil.disk_partitions()
    storage_info = []
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            storage_info.append({
                'Device': partition.device,
                'Mount Point': partition.mountpoint,
                'File System Type': partition.fstype,
                'Total Size (GB)': usage.total / (1024 ** 3),
                'Used Size (GB)': usage.used / (1024 ** 3),
                'Free Size (GB)': usage.free / (1024 ** 3),
                'Usage (%)': usage.percent,
            })
        except PermissionError:
            print(f"Skipping {partition.device} as it is not ready.")
    return storage_info

def get_network_info():
    network_info = {}
    addrs = psutil.net_if_addrs()
    net_io = psutil.net_io_counters()

    for interface, addr_list in addrs.items():
        if interface == 'Ethernet':
            network_info['Connection Type'] = 'Ethernet'
        else:
            network_info['Connection Type'] = 'Wi-Fi'

        for addr in addr_list:
            if addr.family == socket.AF_INET:
                network_info['IPv4 Address'] = addr.address
            elif addr.family == socket.AF_INET6:
                network_info['IPv6 Address'] = addr.address

    network_info['Bytes Sent'] = net_io.bytes_sent / (1024 ** 2)  # in MB
    network_info['Bytes Received'] = net_io.bytes_recv / (1024 ** 2)  # in MB

    return network_info

def get_system_info():
    system_info = {
        'OS': platform.system(),
        'OS Version': platform.version(),
        'OS Build': platform.release(),
        'Device Name': platform.node(),
        'System Uptime': str(datetime.now() - datetime.fromtimestamp(psutil.boot_time()))
    }
    return system_info

def main():
    print("===== CPU Information =====")
    for key, value in get_cpu_info().items():
        print(f"{key}: {value}")
    
    print("\n===== Memory Information =====")
    for key, value in get_memory_info().items():
        print(f"{key}: {value:.2f} GB")
    
    print("\n===== Storage Information =====")
    for partition in get_storage_info():
        print(f"\nDevice: {partition['Device']}")
        for key, value in partition.items():
            if key != 'Device':
                print(f"  {key}: {value:.2f} GB" if 'GB' in key else f"  {key}: {value}")
    
    print("\n===== Network Information =====")
    for key, value in get_network_info().items():
        print(f"{key}: {value}")

    print("\n===== System Information =====")
    for key, value in get_system_info().items():
        print(f"{key}: {value}")

    # Wait for user input before closing
    try:
        input("\nPress Enter to exit...")
    except:
        pass

if __name__ == "__main__":
    main()
