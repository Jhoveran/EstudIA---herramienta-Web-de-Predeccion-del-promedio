import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont


class FormularioEstudiante:
    def __init__(self, root):
        self.root = root
        self.root.title("EstudIA")
        self.root.geometry("1920x1080")
        self.root.config(bg='#dbdbdb')

        # Crear la estructura general
        self.frame_izquierdo = tk.Frame(self.root, bg="#901919", width=300, height=1080)
        self.frame_izquierdo.pack(side="left", fill="y")

        self.frame_derecho = tk.Frame(self.root, bg="white", width=1620, height=1080)
        self.frame_derecho.pack(side="right", fill="both", expand=True)

        # Crear los botones en la sección izquierda
        self.crear_botones()

    def crear_botones(self):
        botones = [
            ("Comprobar Notas", self.mostrar_formulario),
            ("Cuenta", None),
            ("Recursos", None),
            ("Ajustes", None),
        ]

        for texto, comando in botones:
            boton = tk.Button(
                self.frame_izquierdo,
                text=texto,
                font=("Helvetica", 12, "bold"),
                bg="white",
                fg="#901919",
                command=comando,
                height=2,
                width=20
            )
            boton.pack(pady=10)

    def mostrar_formulario(self):
        # Limpiar el contenido del frame derecho antes de mostrar el formulario
        for widget in self.frame_derecho.winfo_children():
            widget.destroy()

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
            label = tk.Label(self.frame_derecho, text=etiqueta, font=("Helvetica", 12), bg="white", anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=20, pady=5)

            entry = tk.Entry(self.frame_derecho, width=25)
            entry.grid(row=i, column=1, padx=10, pady=5)

        boton_enviar = tk.Button(
            self.frame_derecho,
            text="Enviar",
            font=("Helvetica", 12, "bold"),
            bg="#901919",
            fg="white",
            command=lambda: messagebox.showinfo("Info", "Datos enviados correctamente")
        )
        boton_enviar.grid(row=len(etiquetas), column=0, columnspan=2, pady=20)


class VentanaBienvenida:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienvenida")
        self.root.geometry("1920x1080")
        self.root.config(bg="lightblue")

        # Fuente personalizada
        self.fuente = tkFont.Font(family="Helvetica", size=20, weight="bold")

        # Mensaje de bienvenida
        bienvenida_label = tk.Label(self.root, text="Bienvenido a EstudIA", font=self.fuente, bg="lightblue")
        bienvenida_label.pack(pady=300)

        # Botón para ir al formulario
        boton_entrar = tk.Button(
            self.root,
            text="Ingresar",
            bg="#901919",
            fg="white",
            font=self.fuente,
            command=self.abrir_formulario
        )
        boton_entrar.pack(pady=20)

    def abrir_formulario(self):
        self.root.destroy()
        root_formulario = tk.Tk()
        app_formulario = FormularioEstudiante(root_formulario)
        root_formulario.mainloop()


if __name__ == "__main__":
    root_bienvenida = tk.Tk()
    app_bienvenida = VentanaBienvenida(root_bienvenida)
    root_bienvenida.mainloop()
