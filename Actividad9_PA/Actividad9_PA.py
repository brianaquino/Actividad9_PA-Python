import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

arduino_port = "COM5"
baud_rate = 9600
arduino = None

def conectar():
    global arduino
    try: 
        arduino = serial.Serial(arduino_port, baud_rate)
        time.sleep(2)
        lbConection.config(text = "Estado: Conectado", fg="green")
        messagebox.showinfo("Conexión", "Conexión establecida.")
        start_reading()
    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo conectar al arduino")

def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConection.config(text="Estado: desconectado", fg="red")
        messagebox.showinfo("Conexión", "Conexión terminada.")
    else:
        messagebox.showwarning("Advertencia", "No hay conexion activa.")

def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbLimTemp.get()
            if limite.isdigit():
                arduino.write(f"{limite}\n".encode())
                messagebox.showinfo("Enviado", f"limite de temperatura({limite}°C) enviado.")
            else:
                messagebox.showerror("Error", "Ingrese un valor numerico para el limite.")
        except Exception as e:
            messagebox.showwarning("Advertencia", "Conéctese al Arduino antes de enviar el limite.")

def read_from_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip()
            if "Temperatura" in data :
                temp_value = data.split(":")[1].strip().split(" ")[0]
                lbTemp.config(text=f"{temp_value} °C")
            time.sleep(1)
        except Exception as e:
            print(f"Error leyendo datos: {e}")
            break

def start_reading():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()


root = tk.Tk()
root.title("Interfaz de monitoreo de temperatura")
root.geometry("300x350")

lbTitleTemp = tk.Label(root, text= "Temperatura actual", font = ("Arial", 12))
lbTitleTemp.pack(pady=10)

lbTemp = tk.label(root, text= "-- °C", font =("Arial", 24))
lbTemp.pack()

lbConection = tk.Label(root, text = "Estado: Desconectado", fg="red", font= ("Arial", 10))
lbConection.pack(pady = 5)

lbLimitTemp = tk.Label(root, text="Limite de temperatura:")
lbLimitTemp.pack(pady = 5)
tbLimitTemp = tk.Entry(root, width=10)
tbLimitTemp.pack(pady=5)

btnEnviar = tk.Button(root, text= "Enviar limite", command=enviar_limite, font=("Arial", 10))
btnEnviar.pack(pady=5)

btnConectar = tk.Button(root, text="Conectar", command=conectar, font=("Arial", 10))
btnConectar.pack(pady=5)

btnDesconectar = tk.Button(root, text= "Desconectar", command=desconectar, font=("Arial", 10))
btnDesconectar.pack(pady=5)

root.mainloop()

