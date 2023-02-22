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
sock.listen(3)
Limite = 0
inicio = False

# PruebaLola1234

def EscribirEmail(email, mensaje, asunto):
    remitente = "jbarquero201420@gmail.com"
    mensaje = mensaje
    destinatario = email
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = email
    email["Subject"] = asunto
    email.set_content(mensaje)
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, 'kghjhmsvsthnxems') #Falta clave
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()

def RecibirDatos(con,direc):
    errores = ''
    contadorprocesados = 0
    asunto = ''
    mensaje = ''
    while True:
        try:
            data = con.recv(4096)
            dt = data.decode()
            datosEnviados=dt.split(',')
            while True:
                if datosEnviados[0] == '1':
                    datosEnviados.remove('1')
                    for p in datosEnviados:
                        if p == '3':
                            break
                        hilo1= threading.Thread(target=EscribirEmail, args=(p,mensaje,asunto,))
                        hilo1.start()
                        contadorprocesados += 1
                        data = str(contadorprocesados).encode()
                        con.send(data)
                    hilo1.join()
                elif datosEnviados[0] == '2':
                    mensaje = datosEnviados[1]
                    asunto = datosEnviados[2]
                    datosEnviados.remove('2')
                    datosEnviados.remove(mensaje)
                    datosEnviados.remove(asunto)
                elif datosEnviados[-1] == '3':
                    break
            break
        except:
            errores = format_exc()+"\n"
    EscribirXML(str(len(datosEnviados)-1),str(contadorprocesados), errores)
    con.close()
    sock.close()

def EscribirXML(Registros,Registrosprocesados,Errores):
    root = ET.Element("Estadísticas")

    g1 = ET.SubElement(root,"General")
    r1 = ET.SubElement(g1, "TotalDeRegistros")
    r1.text = Registros
    p1 = ET.SubElement(g1, "TotalDeRegistrosProcesados")
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
RecibirDatos(con,client_addr)
#Forma con varias conexiones
#while True: 
    # creamos los hilos
    #hilo1 = threading.Thread(target=RecibirDatos, name='Hilo 1', args=con)
    # ejecutamos los hilos
    #hilo1.start()
    #Limite += 1
    #if Limite == 3:
    #    break


            