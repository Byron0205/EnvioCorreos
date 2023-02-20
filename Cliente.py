import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as alert
from ClasePersona import Persona
import xml.etree.ElementTree as ET

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Selección de archivos")
        self.geometry('500x500')
        self.rutas =[None,None,None]
        self.clientes = []
        self.hilo1= threading.Thread(target=self.GuardarClientes, args=(self.rutas[0],))
        self.hilo2= threading.Thread(target=self.GuardarClientes, args=(self.rutas[1],))
        self.hilo3= threading.Thread(target=self.GuardarClientes, args=(self.rutas[2],))
        self.ruta = tk.StringVar(value="Debe seleccionar entre 2 y 3 archivos")
        self.boton_CargarClientes = tk.Button(self,text='GuardarClientes', command=self.CargarClientesXML)

        self.componentes()


    def componentes(self):
        label_instruccion = tk.Label(self, text="Seleccionar 2 o 3 archivos:")
        label_instruccion.pack()

        boton_buscar = tk.Button(self, text="Buscar archivos", command=self.buscar_archivos)
        boton_buscar.pack()

        label_archivos = tk.Label(self, textvariable=self.ruta)
        label_archivos.pack()
        boton_Consultar = tk.Button(self, text='Ver Clientes', command=self.ConsultarClientes)
        boton_Consultar.pack()
        self.boton_CargarClientes = tk.Button(self,text='GuardarClientes', command=self.CargarClientesXML)
        self.boton_CargarClientes.pack()
        if self.ruta.get() == "Debe seleccionar entre 2 y 3 archivos":
            self.boton_CargarClientes.config(state='disabled')

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
            cliente = Persona(id=datos[0],nombre=datos[1],apellido=datos[2],telefono=datos[3],email=datos[4])
            self.clientes.append(cliente)


    def buscar_archivos(self):
        self.rutas.clear()
        self.rutas= list(filedialog.askopenfilenames(filetypes=[("Archivo XML", "*.xml")]))
        self.ruta.set(value="Debe seleccionar entre 2 y 3 archivos")
        
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
        else:
            alert.showwarning(title='Error en la carga de archivos',text="Debe seleccionar entre 2 y 3 archivos")
    
    #Funcion para revisar que existan y se creen los clientes
    def ConsultarClientes(self):
        formConsultar = tk.Toplevel(self)
        formConsultar.title("Búsqueda")

        lblBuscar = tk.Label(formConsultar, text='Digite el nombre o apellido',justify='center')
        lblBuscar.grid(column=1,row=0)


        #lista de pacientes
        pacientes = tk.Listbox(formConsultar,justify='center')
        pacientes.grid(row=2,column=1)

        for p in self.clientes:
            pacientes.insert('end',  p.id+" "+p.nombre +" "+p.apellido)
            

        formConsultar.mainloop()



root = GUI()

root.mainloop()