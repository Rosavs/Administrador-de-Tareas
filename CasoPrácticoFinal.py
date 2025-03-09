#Caso Práctico Final

#Visual Studio Code versión 3.11.2 64-bit

#La ejecución empieza en la línea 128 pidiendo 
#un nombre para el organizador de tareas y un número máximo que puede almacenar

#La clase Tarea se inicia pidiendo una primera tarea
#la añade a una lista de tareas y añade estado "pendiente" a una lista de estados
#después muestra las diferentes opciones llamando al método self.opciones 

class Tarea():
    def __init__(self,nombre,numerotareas):
        self.nombre = nombre
        self.numerotareas = numerotareas
        self.estado = []
        self.tareas = []
        self.tareas.append(input("Primera tarea: "))
        self.estado.append("pendiente")
        self.opciones()        

#muestra las diferentes opciones y pide una opción

    def opciones(self):
        print("\n--- Organizador de tareas: ",self.nombre,"---")
        print("Opciones: \n A para Agregar nueva tarea\
        \n C para Completar una tarea\
        \n L para Listar todas las tareas\
        \n E para Eliminar una tarea\
        \n S para Salir ")
        self.opcion = input("Elige una opción: ")

        #admite mayúscula o minúscula y llama a los posibles métodos

        if self.opcion in ["A","a"] :               
            self.añadir()
        elif self.opcion in ["E","e"]:
            self.eliminar()
        elif self.opcion in ["L","l"]:
            self.listar()
        elif self.opcion in ["C","c"]:
            self.completar()
        elif self.opcion in ["S","s"]:
            print("¡Hasta luego!")        #si se elige la S o s termina

        #si la opción elegida no exite, vuelve a mostrar las opciones
        #llamando al método self.opciones
            
        else:
            print("Opción no válida")
            self.opciones()

    #añade una tarea si el número máximo no ha sido alcanzado
    #añade "pendiente" a la lista de estados porque una tarea nueva siempre empezará como pendiente
    #y vuelve a mostrar las opciones

    def añadir(self):
        if len(self.tareas) < self.numerotareas:
            self.tareas.append(input("Tarea: "))
            self.estado.append("pendiente")
            self.opciones()

    #si la lista de tareas ha llegado al límite, muestra un mensaje
    #y vuelve a mostras las opciones
            
        else:
            print(f'Alcanzado límite máximo de {self.numerotareas}, no puedes añadir más')
            self.opciones()
    
    #elimina una tarea pidiendo el número de tarea y comprobando:
    #si el valor introducido es númerico y
    #si está en el rango de la lista de tareas

    def eliminar(self):
        self.entradaeliminar = input("Número de tarea a eliminar: ")
        if self.entradaeliminar.isnumeric():
            self.aeliminar = int(self.entradaeliminar)  
            if 0 < self.aeliminar  <= len(self.tareas):
                self.tareas.pop(self.aeliminar-1)         #elimina el elemento en su puesto real en la lista que empieza por 0 
                self.estado.pop(self.aeliminar-1)         #y elimina también su estado en la lista de estado 
                self.opciones()
            else:
                print("No vale, número erróneo")          #si el valor introducido no corresponde a ninguna tarea  
                self.opciones()
        else:
            print("No vale, valor erróneo")               #si el valor introducido no es numérico
            self.opciones()

    #muestra el listado de tareas con un índice y su estado

    def listar(self):
        print("\n-NÚMERO-  -TAREA (ESTADO)-")
        self.indice = list(range(0,len(self.tareas)))              #crea un índice
        for i,j,k in zip(self.indice,self.tareas,self.estado):     #une el índice, las tareas y los estados 
            print(f' {i+1}         {j} ({k}) ')
        self.opciones()

    #completa una tarea pidiendo el número de tarea y comprobando:
    #si el valor introducido es númerico,
    #si está en el rango de la lista de tareas y
    #si ya estaba completada

    def completar(self):
        self.entradacompletar = input("Número de tarea a completar: ")
        if self.entradacompletar.isnumeric():
            self.acompletar = int(self.entradacompletar)
                        
            if self.acompletar <= len(self.tareas) and self.acompletar > 0:
                if self.estado[self.acompletar-1] == "completo":
                    print("La tarea ya estaba completada")
                    self.opciones()
                else:
                    self.estado[self.acompletar-1] = "completo"
                    self.opciones()
            
            else:
                print("No vale, número erróneo")
                self.opciones()
        else:
            print("No vale, números sólo")                      #si el valor introducido no es numérico
            self.opciones()



#Aquí empieza a ejecutarse pidiendo un nombre y un número de tareas máximo para almacenar

print("¡Comenzamos!")

while True:
    
    a=input("Elige un nombre para el organizador: ")    
    b=input("Elige un número máximo de tareas (de 1 a 10): ") 
           
    try:
        nub=int(b)                             #si el valor introducido es un número 
                                               #comprueba que está entre 0 y 10
        if 10< nub or nub <= 0:
            print("Número fuera de rango")     #si no está en el rango avisa
        elif 0< nub <=  10:
            tar=Tarea(a,nub)                   #si todo está bien se ejecuta creando un objeto de la clase Tarea 
            break                              #con los parámetros introducidos 
    except: 
        if b.isnumeric() == False:             #si el valor introducido no es numérico 
            print("Sólo numeros")              #avisa  
   