import PySimpleGUI as sg
import subprocess

sg.theme('DarkGreen5')

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Show'), sg.Button('Exit'), sg.Button(key="updateButton", button_text="Обновить")]
          ]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])
    if event == 'updateButton':
        window['-OUTPUT-'].update("Обновление...")
        subprocess.call(["c:\\Leonov\\pisar\\pisar\\install\\update.bat"])
        window['-OUTPUT-'].update("Обновление выполнено")

window.close()