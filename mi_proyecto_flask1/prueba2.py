import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import joblib
import pandas as pd
import matplotlib.pyplot as plt

#Formulario del estudiante
class FormularioEstudiante:
    def __init__(self, root):
        self.root = root
        self.root.title("EstudIA")
        self.root.geometry("1920x1080")
        self.root.config(bg='#dbdbdb')

        # estructura general interfaz 2
        self.frame_izquierdo = tk.Frame(self.root, bg="#343645", width=300, height=1080)
        self.frame_izquierdo.pack(side="left", fill="y")

        self.frame_derecho = tk.Frame(self.root, bg="white", width=1620, height=1080)
        self.frame_derecho.pack(side="right", fill="both", expand=True)

        # Crear los botones en la sección izquierda
        self.botones_izquierda()

        self.entradas = []
        self.num_ciclos = 6

    def botones_izquierda(self):
        botones = [
            ("Comprobar Notas", self.crear_interfaz),
            ("Cuenta", None),
            ("Recursos", None),
            ("Ajustes", None),
        ]

        for texto, comando in botones:
            boton = tk.Button(
                self.frame_izquierdo,
                text=texto,
                font=("Helvetica", 12, "bold"),
                bg="#343645",
                fg="white",
                command=comando,
                height=2,
                width=20
            )
            boton.pack(pady=10)

    def crear_interfaz(self):

        etiquetas = [
            "Edad(rango: de 15 a 22):",
            "Educación del Padre(Escala: 0 - ninguna, 1 - educación primaria, 2 - educación secundaria, 4 - educación superior):",
            "Educación de la Madre(Escala: 0 - ninguna, 1 - educación primaria, 2 - educación secundaria, 4 - educación superior):",
            "Tiempo de Estudio(1 - <2 horas, 2 - 2 a 5 horas, 3 - 5 a 10 horas, 4 - >10 horas):",
            "Relaciones Familiares (1 - muy malas a 5 - excelentes):",
            "Tiempo Libre (1 - muy bajo a 5 - muy alto):",
            "Salir con Amigos (1 - muy bajo a 5 - muy alto):",
            "Consumo de Alcohol (1 - muy bajo a 5 - muy alto):",
            "Salud (1 - muy malo a 5 - muy bueno):",
            "Ausencias (0 a 93):",
            "Promedio Ponderado ciclo 1 (0 a 20):",
            "Promedio Ponderado ciclo 2 (0 a 20):",
            "Promedio ponderado ciclo 3 (0 a 20):",
            "Promedio ponderado ciclo 4 (0 a 20):",
        ]

        for i, etiqueta in enumerate(etiquetas):
            #etiqueta
            label = tk.Label(self.frame_derecho, text=etiqueta, font=("Helvetica", 12, "bold"), bg="white", anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=20, pady=5)

            #cuadro de entrada
            entry = tk.Entry(self.frame_derecho, width=25)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entradas.append(entry)

        boton_enviar = tk.Button(
            self.frame_derecho,
            text="Enviar",
            font=("Helvetica", 12, "bold"),
            command=self.enviar_datos,
            bg="#901919",
            fg="white",
        )
        boton_enviar.grid(row=len(etiquetas), column=0, columnspan=2, pady=20)    

    def enviar_datos(self):
        #Se crea arreglo datos y predicciones /datos guarda valor de las variables y predicciones el valor para cada par val1,val2
        datos = []
        predicciones = [[0] * self.num_ciclos for _ in range(3)]

        for i, entry in enumerate(self.entradas):
            valor = entry.get()  # Obtener el valor como cadena
            datos.append(int(valor))  # Convertir a entero para todos

        #datos ahora tiene valores enteros y se asocian a variables
        age, fedu, medu, studytime, famrel, freetime, goout, walc, health, absences, val1, val2, val3, val4 = datos
        self.promedio_reales = [val1, val2, val3, val4]

        for i in range(len(self.promedio_reales)-1):
            g1 = self.promedio_reales[i]
            g2 = self.promedio_reales[i+1]
            # Definir datos del alumno
            self.datos_alumno = {
                'age': age, 'Medu': medu, 'Fedu': fedu, 'traveltime': 3, 
                'studytime': studytime, 'famrel': famrel, 'freetime': freetime, 
                'goout': goout, 'Walc': walc, 'health': health, 
                'absences': absences, 'G1': g1, 'G2': g2
            }

            for j in range(self.num_ciclos):
                # Convertir datos del alumno a DataFrame
                df_alumno = pd.DataFrame([self.datos_alumno])

                # Cargar el modelo entrenado
                RFR = joblib.load('D:\Proyecto POO\Interfaz_IA\maq_1\modelo_random_fores_entrenado.pkl')

                # Predecir la calificación final G3
                prediccion_G3 = RFR.predict(df_alumno)[0]
                predicciones[i][j] = prediccion_G3

                # Actualizar G1 y G2 para la siguiente iteración
                self.datos_alumno['G1'] = self.datos_alumno['G2']  # G1 toma el valor de G2 actual
                self.datos_alumno['G2'] = prediccion_G3       # G2 toma el valor predicho de G3

        # Guardar las predicciones
        self.predicciones = predicciones
        self.graficar_datos()

    def graficar_datos(self):

        # Crear la lista de ciclos para el eje X
        ciclos = [f'Ciclo {i+1}' for i in range(10)]

        plt.figure(figsize=(10, 15))

        # Graficar valores reales para
        plt.plot(ciclos[:4], self.promedio_reales, marker='o', color='red', label="Valores Reales")

        # Colores para las diferentes predicciones
        colores_prediccion = ['blue', 'green', 'purple']

        # Graficar las predicciones para cada par de valores
        for i in range(3): 
            #determinar el punto de inicio en el eje x basado en el último valor usado
            inicio_x = i + 2  #ciclo 3, 4, 5
            
            #crear el rango de x para este conjunto de predicciones
            x_range = ciclos[inicio_x:inicio_x+6]
            
            #graficar las predicciones
            plt.plot(x_range, self.predicciones[i], 
                    marker='o', color=colores_prediccion[i], label=f"Predicciones {i+1} (val{i+1}-val{i+2})")

        # Añadir títulos y etiquetas
        plt.title("Predicción de Promedios Proximos ciclos con RF")
        plt.xlabel("Ciclos")
        plt.ylabel("Promedio Predicho")
        plt.legend()
        plt.grid(True)

        # Mostrar la gráfica
        plt.show()        
         
#Ventana de bienvenida
class VentanaBienvenida:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario del Estudiante")
        self.root.geometry("1920x1080")
        self.root.config(bg='lightblue')

        # Fuente personalizada
        self.fuente = tkFont.Font(family="Helvetica", size=20, weight="bold")

        # Configurar la distribución de las columnas para que se dividan en dos
        self.root.columnconfigure(0, weight=1)  # Columna izquierda
        self.root.columnconfigure(1, weight=1)  # Columna derecha

        #Crear un frame para el lado izquierd
        frame_izquierdo = tk.Frame(self.root, bg="#901919", width=560, height=1080)
        frame_izquierdo.grid(row=0, column=0, sticky="nsew")  # Ajustar el tamaño completo de la columna izquierda

        # Crear un frame para el lado derecho con fondo rojo claro
        frame_derecho = tk.Frame(self.root, bg="#dbdbdb", width=960, height=1080)
        frame_derecho.grid(row=0, column=1, sticky="nsew")  # Ajustar el tamaño completo de la columna derecha

        # Mensaje de bienvenida en el frame derecho
        bienvenida_label = tk.Label(frame_derecho, text="Bienvenido a EstudIA", font=self.fuente, bg="white")
        bienvenida_label.pack(pady=300)

        # Botón para ir al formulario en el frame derecho
        boton_entrar = tk.Button(frame_derecho, text="Ingresar", bg="#901919", fg="White", font=self.fuente, command=self.abrir_formulario)
        boton_entrar.pack(pady=0)      

    # Cerramos la ventana de bienvenida y abrimos la ventana del formulario
    def abrir_formulario(self):    
        self.root.destroy()
        root_formulario = tk.Tk()
        app_formulario = FormularioEstudiante(root_formulario)
        root_formulario.mainloop()

# Crear la ventana principal
if __name__ == "__main__":
    root_bienvenida = tk.Tk()
    app_bienvenida = VentanaBienvenida(root_bienvenida)
    root_bienvenida.mainloop()        
    