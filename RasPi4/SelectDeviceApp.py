#11:01 24 jun 2024
import tkinter as tk
from tkinter import messagebox
from bluepy.btle import Scanner, DefaultDelegate
import json
import os

ble_devices_path = r'ble_devices.json'

current_dir = os.path.dirname(os.path.abspath(__file__))
ble_devices_path = os.path.join(current_dir , 'data' , ble_devices_path)
scanned_devices = []
saved_devices = []

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

def scan_ble_devices():
    global scanned_devices
    scanned_devices = []

    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(0.3)

    scanned_devices = [(dev.addr, dev.getValueText(9)) for dev in devices]

    display_scanned_devices()

def display_scanned_devices():
    listbox_scanned.delete(0, tk.END)
    for addr, name in scanned_devices:
        listbox_scanned.insert(tk.END, f"{name} | {addr}")

def save_selected_device():
    selected_index = listbox_scanned.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Please select a device from the scanned devices list.")
        return

    selected_device = scanned_devices[selected_index[0]]
    if selected_device not in saved_devices:
        saved_devices.append(selected_device)
        display_saved_devices()
        messagebox.showinfo("Info", f"Device {selected_device[0]} saved.")
    else:
        messagebox.showwarning("Warning", f"Device {selected_device[0]} is already saved.")

def delete_saved_device():
    selected_index = listbox_saved.curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "Please select a device from the saved devices list.")
        return

    deleted_device = saved_devices[selected_index[0]]
    saved_devices.pop(selected_index[0])
    display_saved_devices()
    messagebox.showinfo("Info", f"Device {deleted_device[0]} deleted.")

def display_saved_devices():
    listbox_saved.delete(0, tk.END)
    with open(ble_devices_path, 'w') as f:
        json.dump(saved_devices, f, indent=4)
        
    for addr, name in saved_devices:
        listbox_saved.insert(tk.END, f" {name} | {addr}")

try:
    with open(ble_devices_path, 'r') as f:
        saved_devices = json.load(f)
    
    root = tk.Tk()
    root.title("BLE Device Manager")

    frame_scanned = tk.Frame(root)
    frame_scanned.pack(side=tk.LEFT, padx=10, pady=10)

    label_scanned = tk.Label(frame_scanned, text="Scanned BLE Devices")
    label_scanned.pack(pady=10)

    listbox_scanned = tk.Listbox(frame_scanned, width=30, height=10)
    listbox_scanned.pack(pady=10)

    button_scan = tk.Button(frame_scanned, text="Scan Devices", command=scan_ble_devices)
    button_scan.pack(pady=5)

    button_save = tk.Button(frame_scanned, text="Save Selected Device", command=save_selected_device)
    button_save.pack(pady=5)

    frame_saved = tk.Frame(root)
    frame_saved.pack(side=tk.RIGHT, padx=10, pady=10)

    label_saved = tk.Label(frame_saved, text="Saved BLE Devices")
    label_saved.pack(pady=10)
    
    listbox_saved = tk.Listbox(frame_saved, width=30, height=10)
    listbox_saved.pack(pady=10)

    button_delete = tk.Button(frame_saved, text="Delete Selected Device", command=delete_saved_device)
    button_delete.pack(pady=5)
    display_saved_devices()
    root.mainloop()
except FileNotFoundError:
    print(f"Error to read file: {ble_devices_path}")



