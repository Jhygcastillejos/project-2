import socket
import json
import PySimpleGUI as sg
import subprocess

def gather_system_info():
    """vcgen commmands"""
   # Gathers system information
    core_voltage = subprocess.check_output(["vcgencmd", "measure_volts", "core"]).decode("utf-8").strip()
    memory_usage = subprocess.check_output(["vcgencmd", "get_mem", "arm"]).decode("utf-8").strip()
    clock_freq = subprocess.check_output(["vcgencmd", "measure_clock", "arm"]).decode("utf-8").strip()
    temperature = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    

    #returns gathered info
    return {
        "CPU Temperature": temperature.split('=')[1].split('\'')[0],
        "Core Voltage": core_voltage.split('=')[1].split('\'')[0],
        "Memory Usage": memory_usage.split('=')[1].split('\'')[0],
        "Clock Frequency": clock_freq.split('=')[1].split('\'')[0],
        }
        

def update_gui(window):
    """updtes gui with gathered info"""
    system_info = gather_system_info()
    for i, (label, value) in enumerate(system_info.items()):
        window[f'-INFO-{i}-'].update(f'{label}: {value}')

def main():
    """main function"""
    
    host = '10.102.13.154'  
    port = 8001  

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening for incoming connections.")

    client_socket, addr = server_socket.accept()
    print("Connected to client:", addr)
    
    #layuut command for gui
    layout = [
        [sg.Text('System Information')],
    ]

    for i in range(5):
        layout.append([sg.Text('', key=f'-INFO-{i}-')])

    window = sg.Window('Raspberry Pi System Info', layout)

    while True:
        event, values = window.read(timeout=2000)  # Update
        
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            json_data = json.loads(data)
            
        except ConnectionResetError:
            break

        update_gui(window)

    window.close()
    server_socket.close()
    

if __name__ == "__main__":
    main()
