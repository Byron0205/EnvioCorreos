import tkinter as tk

def VentanaCorreoUnico():
    ventana = tk.Tk()
    ventana.title("Correo nuevo")

    ventana.geometry("520x250")
    correoPara = tk.Label(ventana, text="Para:")
    correoPara_Entry = tk.Entry(ventana, width=50)
    cargarDestinatarios= tk.Button(ventana, text= 'Cargar', width=6)
    asunto_label = tk.Label(ventana, text="Asunto:")
    asunto_entry = tk.Entry(ventana, width=50)
    mensaje_label = tk.Label(ventana, text="Mensaje:")
    mensaje_text = tk.Text(ventana, width=50, height=10)
    enviar_button = tk.Button(ventana, text="Enviar")

    correoPara.grid(row=0, column=0, sticky=tk.E)
    correoPara_Entry.grid(row=0, column=1)
    cargarDestinatarios.grid(row=0,column=2)
    asunto_label.grid(row=1, column=0, sticky=tk.E)
    asunto_entry.grid(row=1, column=1)
    mensaje_label.grid(row=2, column=0, sticky=tk.NE)
    mensaje_text.grid(row=2, column=1, rowspan=3)
    enviar_button.grid(row=5, column=1, sticky=tk.E)

    ventana.mainloop()

VentanaCorreoUnico()

def IniciarSesion():
    ventana = tk.Tk()
    ventana.title("Inicio de sesión")
    ventana.geometry("500x250")

    titulo_label = tk.Label(ventana, text="Inicio de sesión", font=("Arial", 18), pady=20)
    titulo_label.pack()

    correo_label = tk.Label(ventana, text="Correo electrónico:", anchor="center")
    correo_label.pack()
    correo_entry = tk.Entry(ventana, width=50, justify="center")
    correo_entry.pack()

    contrasena_label = tk.Label(ventana, text="Contraseña generada:", anchor="center")
    contrasena_label.pack()
    contrasena_entry = tk.Entry(ventana, width=50, show="*", justify="center")
    contrasena_entry.pack()

    iniciar_sesion_button = tk.Button(ventana, text="Iniciar sesión")
    iniciar_sesion_button.pack(pady=20)

    # centrar la ventana en la pantalla
    ventana.eval('tk::PlaceWindow %s center' % ventana.winfo_toplevel())

    ventana.mainloop()
