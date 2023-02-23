import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as alert
from ClasePersona import Persona
import xml.etree.ElementTree as ET
import socket

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Correo nuevo")
        self.geometry('550x320')
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.correo = ''
        self.password = ''
        self.completados = tk.IntVar(value=0)
        self.total = tk.IntVar()
        self.rutas =[None,None,None]
        self.clientes = []
        self.hilo1= threading.Thread(target=self.GuardarClientes, args=(self.rutas[0],))
        self.hilo2= threading.Thread(target=self.GuardarClientes, args=(self.rutas[1],))
        self.hilo3= threading.Thread(target=self.GuardarClientes, args=(self.rutas[2],))
        self.ruta = tk.StringVar()
        self.CorreoPara= tk.StringVar()
        self.boton_CargarClientes = ''
        self.correoPara_Entry=''
        self.componentes()
        #self.boton_Consultar = ''

        


    def componentes(self):

        correo_label = tk.Label(self, text="Correo:")
        correo_entry = tk.Entry(self, width=50)
        
        contrasena_label = tk.Label(self, text="Contraseña:", anchor="center")
        contrasena_entry = tk.Entry(self, width=50, show="*", justify="center")
        

        #iniciar_sesion_button = tk.Button(self, text="Iniciar sesión",command=lambda:self.guardarCredenciales(correo_entry.get(),contrasena_entry.get()))
        

        correoPara = tk.Label(self, text="Para:")
        self.correoPara_Entry = tk.Entry(self, width=50, textvariable=self.CorreoPara)
        cargarDestinatarios= tk.Button(self, text= 'Cargar', width=6,command=self.ventanaCargarClientes)
        asunto_label = tk.Label(self, text="Asunto:")
        asunto_entry = tk.Entry(self, width=50)
        mensaje_label = tk.Label(self, text="Mensaje:")
        mensaje_text = tk.Text(self, width=50, height=10)
        enviar_button = tk.Button(self, text="Enviar", command=lambda:self.enviarCorreo(mensaje=mensaje_text.get(1.0,tk.END),asunto= asunto_entry.get(),correo= correo_entry.get(),password= contrasena_entry.get()))
        
        correo_label.grid(row=0,column=0)
        correo_entry.grid(row=0,column=1)
        contrasena_label.grid(row=1,column=0)
        contrasena_entry.grid(row=1,column=1)
        #iniciar_sesion_button.grid(row=2,column=1,sticky=tk.E)
        correoPara.grid(row=3, column=0, sticky=tk.E)
        self.correoPara_Entry.grid(row=3, column=1)
        cargarDestinatarios.grid(row=3,column=2)
        asunto_label.grid(row=4, column=0, sticky=tk.E)
        asunto_entry.grid(row=4, column=1)
        mensaje_label.grid(row=5, column=0, sticky=tk.NE)
        mensaje_text.grid(row=5, column=1, rowspan=3)
        enviar_button.grid(row=9, column=1, sticky=tk.E)

    def VentanaProgreso(self):
        self.total.set(len(self.clientes))
        ventana = tk.Toplevel(self)
        ventana.grab_set()
        lblCompletados = tk.Label(ventana, textvariable=self.completados)
        lblCompletados.grid(row=1, column=1)
        lblUnion= tk.Label(ventana, text=' de ')
        lblUnion.grid(row=1, column=2)
        lblRestante = tk.Label(ventana, textvariable=self.total)
        lblRestante.grid(row=1, column=3)
        while self.completados.get() < self.total.get(): #Esto recibe lo que envia el server, no se como mostrarlo o si deberia estar aqui xd
            data = self.clientSocket.recv(4096)
            dt = data.decode()
            self.completados.set(int(dt))
        else:
            alert.showinfo(title='transaccion exitosa', message='Completado el envio!!')
            #ventana.destroy()
        ventana.mainloop()

    def enviarCorreo(self, mensaje, asunto, correo, password):
        self.clientSocket.connect(('localhost', 5000))
        if self.CorreoPara.get() != 'cargado desde xml':
            datos = f'4,{mensaje},{asunto},{correo},{password},{self.CorreoPara.get()}'
        else:
            datos = f'2,{mensaje},{asunto},{correo},{password},'
            enviado = datos.encode()
            self.clientSocket.send(enviado)
            self.clientSocket.send(b'1,')

            for c in self.clientes:
                datos = f'{c.email},'
                enviado = datos.encode()
                self.clientSocket.send(enviado)
        self.clientSocket.send(b'3')
        self.VentanaProgreso()

    def CargarClientesXML(self):
        if len(self.rutas)>=3:
            self.hilo1.start()
            self.hilo2.start()
            self.hilo3.start()
            self.hilo1.join()
            self.hilo2.join()
            self.hilo3.join()
        elif len(self.rutas)>=2:
            self.hilo1.start()
            self.hilo2.start()
            self.hilo1.join()
            self.hilo2.join()

    def GuardarClientes(self,ruta):
        tree = ET.parse(ruta)
        root = tree.getroot()
        for c in root.iter('personne'):
            persone_id = c.attrib['id']
            datos=[]
            datos.append(persone_id)
            for child in c:
                datos.append(child.text)
            cliente = Persona(id=datos[0],email=datos[4])
            self.clientes.append(cliente)

    def cerrarVentana(self,ventana):
        ventana.grab_release()
        ventana.destroy()

    def ventanaCargarClientes(self):
        carga = tk.Toplevel(self)
        carga.title("Cargar Clientes")
        carga.geometry('500x250')
        carga.grab_set()
        label_instruccion = tk.Label(carga, text="Debe seleccionar minimo 2 archivos(3 max)", font='10')
        label_instruccion.grid(row=1,column=0,columnspan=2)

        boton_buscar = tk.Button(carga, text="Buscar archivos", command=self.buscar_archivos)
        boton_buscar.grid(row=2,column=0)

        label_archivos = tk.Label(carga, textvariable=self.ruta)
        label_archivos.grid(row=3,column=0,columnspan=2)

        #self.boton_Consultar =tk.Button(carga, text='Ver Clientes', command=self.ConsultarClientes)
        #self.boton_Consultar.grid(row=4,column=1)
        
        self.boton_CargarClientes = tk.Button(carga,text='GuardarClientes', command=self.CargarClientesXML)
        self.boton_CargarClientes.grid(row=4,column=0)
        boton_Aceptar = tk.Button(carga, text='Aceptar', command=lambda:self.cerrarVentana(carga))
        boton_Aceptar.grid(row=5,column=1)
        if self.ruta.get() == "":
            self.boton_CargarClientes.config(state='disabled')

    def buscar_archivos(self):
        self.rutas.clear()
        self.rutas= list(filedialog.askopenfilenames(filetypes=[("Archivo XML", "*.xml")]))
        self.ruta.set(value="")
        
        if len(self.rutas) >= 2 and len(self.rutas) <= 3:
            if len(self.rutas)>=3:
                self.ruta.set(value=f'{self.rutas[0]}\n{self.rutas[1]}\n{self.rutas[2]}')
                self.hilo1 =threading.Thread(target=self.GuardarClientes, args=(self.rutas[0],))
                self.hilo2 =threading.Thread(target=self.GuardarClientes, args=(self.rutas[1],))
                self.hilo3 =threading.Thread(target=self.GuardarClientes, args=(self.rutas[2],))

            else:
                self.ruta.set(value=f'{self.rutas[0]}\n{self.rutas[1]}')
                self.hilo1 =threading.Thread(target=self.GuardarClientes, args=(self.rutas[0],))
                self.hilo2 =threading.Thread(target=self.GuardarClientes, args=(self.rutas[1],))
                

            self.boton_CargarClientes.config(state='normal')
            self.CorreoPara.set('cargado desde xml')
            self.correoPara_Entry.config( state='disabled')
            alert.showinfo(title='Transaccion exitosa', message='Clientes cargados correctamente')
        else:
            alert.showwarning(title='Error en la carga de archivos',text="Debe seleccionar entre 2 y 3 archivos")
    
    def guardarCredenciales(self, user, password):
        self.correo = user
        self.password = password

    def IniciarSesion(self):
        ventana = tk.Toplevel(self)
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

        iniciar_sesion_button = tk.Button(ventana, text="Iniciar sesión",command=lambda:self.guardarCredenciales(correo_entry.get(),contrasena_entry.get(),ventana))
        iniciar_sesion_button.pack(pady=20)
        # centrar la ventana en la pantalla
        #ventana.update_idletasks()
        #width = ventana.winfo_width()
        #height = ventana.winfo_height()
        #x = (ventana.winfo_screenwidth() // 2) - (width // 2)
        #y = (ventana.winfo_screenheight() // 2) - (height // 2)
        #ventana.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        ventana.mainloop()

    #Funcion para revisar que existan y se creen los clientes
    #def ConsultarClientes(self):
    #   formConsultar = tk.Toplevel(self)
    #    formConsultar.title("Búsqueda")

    #    lblBuscar = tk.Label(formConsultar, text='Digite el nombre o apellido',justify='center')
    #    lblBuscar.grid(column=1,row=0)


        #lista de pacientes
    #    pacientes = tk.Listbox(formConsultar,justify='center')
    #    pacientes.grid(row=2,column=1)

    #    for p in self.clientes:
    #        pacientes.insert('end',  p.id+" "+p.nombre +" "+p.apellido)
            

    #    formConsultar.mainloop()



root = GUI()

root.mainloop()