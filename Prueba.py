import tkinter as tk

def VentanaCorreoUnico():
    ventana = tk.Tk()
    ventana.title("Correo nuevo")

    ventana.geometry("500x250")
    correoPara = tk.Label(ventana, text="Para:")
    correoPara_Entry = tk.Entry(ventana, width=50)
    asunto_label = tk.Label(ventana, text="Asunto:")
    asunto_entry = tk.Entry(ventana, width=50)
    mensaje_label = tk.Label(ventana, text="Mensaje:")
    mensaje_text = tk.Text(ventana, width=50, height=10)
    enviar_button = tk.Button(ventana, text="Enviar")

    correoPara.grid(row=0, column=0, sticky=tk.E)
    correoPara_Entry.grid(row=0, column=1)
    asunto_label.grid(row=1, column=0, sticky=tk.E)
    asunto_entry.grid(row=1, column=1)
    mensaje_label.grid(row=2, column=0, sticky=tk.NE)
    mensaje_text.grid(row=2, column=1, rowspan=3)
    enviar_button.grid(row=5, column=1, sticky=tk.E)

    ventana.mainloop()

VentanaCorreoUnico()