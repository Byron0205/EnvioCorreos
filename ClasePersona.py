class Persona:
    def __init__(self,id,nombre, apellido, telefono, email):
        self.id = id
        self.nombre= nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email= email
    
    def getCorreo(self):
        return self.email