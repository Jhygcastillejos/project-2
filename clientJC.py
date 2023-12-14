import PySimpleGUI as sg
import socket
import json
import time

#unicode for blinking led
CIRCLE = '●'  
CIRCLE_OUTLINE = '○' 

def LED(color, key):
    """led color and key"""
    return sg.Text(CIRCLE_OUTLINE, text_color=color, key=key)

def collect_pi_data():
    """function for collecting Pi data"""
    return {"dummy_data": "placeholder"}

def establish_connection(host, port):
    """establishes connection"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        return client_socket
    except ConnectionRefusedError:
        return None
    
#gui layout for iteration and led
layout = [
    [sg.Text('led '), LED('white', '-LED-')],
    [sg.Text('Iterations: 0', key='-ITERATIONS-')], 
    [sg.Button('Exit')]
]

window = sg.Window('Connection Status', layout, font='Any 16')

host = '10.102.13.154'  
port = 8001  
client_connected = False
iterations = 0

#closes after 50 iterations
while iterations < 50:  
    event, values = window.read(timeout=2000)
    
    #closes when exit s pressed
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if not client_connected:
        client_socket = establish_connection(host, port)
        if client_socket:
            client_connected = True
            window['-LED-'].update(CIRCLE)

    else:
        data = collect_pi_data()
        data_json = json.dumps(data)
        try:
            client_socket.send(data_json.encode())
            iterations += 1
            window['-ITERATIONS-'].update(f'Iterations: {iterations}')
            
           #blinking correspods to itterations
            if iterations % 2 == 0:
                window['-LED-'].update(CIRCLE_OUTLINE)
            else:
                window['-LED-'].update(CIRCLE)
            
        except socket.error:
            window['-LED-'].update(CIRCLE_OUTLINE)
            client_connected = False

window.close()
