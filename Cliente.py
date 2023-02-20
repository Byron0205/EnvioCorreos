import threading

rutas=[]

def CargarClientesXML(ruta):
    pass

hilo1= threading.Thread(target=CargarClientesXML, args=(rutas[0]))
hilo2= threading.Thread(target=CargarClientesXML, args=(rutas[1]))
hilo3= threading.Thread(target=CargarClientesXML, args=(rutas[2]))

