import socket
from email.message import EmailMessage
import smtplib
from xml.dom import minidom
import xml.etree.ElementTree as ET
from traceback import format_exc
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5000 # Puerto de comunicacion
sock.bind(('localhost',port)) # IP y Puerto de conexion en una Tupla
sock.listen(4)
ListaPersonas = []
contador = 0
Limite = 0
inicio = False

def EscribirEmail(Lista,Datos):
    remitente = Datos[0]
    destinatario = Lista[4]
    mensaje = "Esto es un mensaje desde python"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Correo de prueba python"
    email.set_content(mensaje)
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, Datos[1]) #Falta clave
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()

def RecibirDatos(con):
    contadorprocesados = 0
    while True:
        try:
            data = con.recv(4096)
            dt = data.decode()
            if not inicio:
                DatosInicio = dt.split(",") #El primer envio de datos es el usuario, clave y cantidad de personas
                inicio = True
            else:
                ListaPersonas.append(dt)
                contador += 1
                if contador == 5: #Cada cinco datos es una persona
                    EnviarEmail = threading.Thread(target=EscribirEmail, name='Enviar Email', args=(ListaPersonas,DatosInicio))
                    EnviarEmail.start()
                    #EscribirEmail(ListaPersonas,DatosInicio)
                    contadorprocesados += 1
                    contador = 0
                    ListaPersonas = [] # Falta forma de saber cuando terminar el while
                if DatosInicio[3] == contadorprocesados:
                    break
        except:
            errores = format_exc()+"\n"
    EscribirXML(DatosInicio[3],contadorprocesados,errores)
    con.close()
    sock.close()

def EscribirXML(Registros,Registrosprocesados,Errores):
    root = ET.Element("Estadísticas")

    g1 = ET.SubElement(root,"General")
    r1 = ET.SubElement(g1, "Total de registros")
    r1.text = Registros
    p1 = ET.SubElement(g1, "Total de registros procesados")
    p1.text = Registrosprocesados
    e1 = ET.SubElement(g1, "Errores")
    e1.text = Errores

        
    tree = ET.ElementTree(root)
    #tree.write('pacientesPrueba.xml', encoding="UTF-8", xml_declaration=True, method="xml")
    xml = minidom.parseString(ET.tostring(root, encoding='unicode'))

    with open('Estadísticas.xml', 'w', encoding="UTF-8") as f:
        f.write(xml.toprettyxml(indent="    "))


#Forma con una sola conexion
con, client_addr =  sock.accept()
RecibirDatos(con)
#Forma con varias conexiones
#while True: 
    # creamos los hilos
    #hilo1 = threading.Thread(target=RecibirDatos, name='Hilo 1', args=con)
    # ejecutamos los hilos
    #hilo1.start()
    #Limite += 1
    #if Limite == 3:
    #    break


            