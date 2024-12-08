from flask import Flask, request, jsonify, render_template, send_from_directory
import pickle
import numpy as np
import joblib
import matplotlib.pyplot as plt
import os
import pandas as pd

app = Flask(__name__)

@app.route('/')
def Inicio():
    # Retorna la página de inicio
    return render_template('home.html')

@app.route('/about')
def about():
    # Retorna la página 'about.html'
    return render_template('about.html')

@app.route("/predict", methods=['POST'])

def predict():
    
    # Obtener las características del formulario
    int_features = [
        int(request.form["edad"]),
        int(request.form["eduPadre"]),
        int(request.form["eduMadre"]),
        int(request.form["tiempoEstudio"]),
        int(request.form["relacionesFamiliares"]),
        int(request.form["tiempoLibre"]),
        int(request.form["salirConAmigos"]),
        int(request.form["consumoAlcohol"]),
        int(request.form["salud"]),
        float(request.form["ausencias"]),
        int(request.form["promedioCiclo1"]),
        int(request.form["promedioCiclo2"]),
        int(request.form["promedioCiclo3"]),
        int(request.form["promedioCiclo4"])
    ]

    # Extraer las variables del formulario
    age, fedu, medu, studytime, famrel, freetime, goout, walc, health, absences, val1, val2, val3, val4 = int_features
    promedio_reales = [val1, val2, val3, val4]
    
    predicciones = [[0] * 6 for _ in range(3)]
   
    for i in range(len(promedio_reales) - 1):
        g1 = promedio_reales[i]
        g2 = promedio_reales[i + 1]

        # Definir datos del alumno
        datos_alumno = {
            'age': age, 'Medu': medu, 'Fedu': fedu, 'traveltime': 3, 
            'studytime': studytime, 'famrel': famrel, 'freetime': freetime, 
            'goout': goout, 'Walc': walc, 'health': health, 
            'absences': absences, 'G1': g1, 'G2': g2
        }

        for j in range(6):
            # Convertir datos del alumno a DataFrame
            df_alumno = pd.DataFrame([datos_alumno])

            # Cargar el modelo entrenado
            ##RFR = joblib.load('E:\mi_proyecto_flask\modelo_random_fores_entrenado.pkl')

            try:
                RFR = joblib.load('D:\\Proyecto POO\\PLATAFORMA\\env\\mi_proyecto_flask1\\mi_proyecto_flask1\\modelo_random_forest_entrenado.pkl')
                print("Modelo cargado correctamente.")
            except Exception as e:
                print(f"Error al cargar el modelo: {e}")
                #Aquí puedes devolver un mensaje de error a la página web, por ejemplo:
                return render_template('error.html', message=f"Hubo un problema al cargar el modelo: {e}")


            # Predecir la calificación final G3
            prediccion_G3 = RFR.predict(df_alumno)[0]
            predicciones[i][j] = prediccion_G3

            # Actualizar G1 y G2 para la siguiente iteración
            datos_alumno['G1'] = datos_alumno['G2']  # G1 toma el valor de G2 actual
            datos_alumno['G2'] = prediccion_G3       # G2 toma el valor predicho de G3

    # Guardar la gráfica y pasar el nombre de archivo para mostrarla en la página
    return graficar_datos(predicciones, promedio_reales)

def graficar_datos(predicciones, promedio_reales):
    # Crear la lista de ciclos para el eje X
    ciclos = [f'Ciclo {i+1}' for i in range(10)]

    # Crear la figura
    fig, ax = plt.subplots(figsize=(10, 5))

    # Graficar valores reales para ciclo 1 y ciclo 2
    ax.plot(ciclos[:4], promedio_reales, marker='o', color='red', label="Valores Reales")

    # Colores para las diferentes predicciones
    colores_prediccion = ['blue', 'green', 'purple']

    # Graficar las predicciones para cada par de valores
    for i in range(3):  # Para cada conjunto de predicciones
        # Determinar el punto de inicio en el eje x basado en el último valor usado
        inicio_x = i + 2  # Ciclo 3, 4, 5 respectivamente
        x_range = ciclos[inicio_x:inicio_x+6]
        ax.plot(x_range, predicciones[i], marker='o', color=colores_prediccion[i], label=f"Predicciones {i+1} (val{i+1}-val{i+2})")

    # Añadir títulos y etiquetas
    ax.set_title("Predicción de Promedios Proximos ciclos con RF")
    ax.set_xlabel("Ciclos")
    ax.set_ylabel("Promedio Predicho")
    ax.legend()
    ax.grid(True)

    # Guardar la gráfica como archivo PNG en la carpeta 'static'
    image_path = os.path.join('static', 'grafica.png')

    try:
        fig.savefig(image_path)
        print(f"Gráfica guardada en {image_path}")
    
    except Exception as e:
        print(f"Error al guardar la gráfica: {e}")
        return render_template('error.html', message=f"Hubo un problema al guardar la gráfica: {e}")


    # Cerrar la figura para liberar memoria
    plt.close(fig)

    # Pasar la ruta de la imagen a la página web para renderizarla
    return render_template('resultados.html', image_url=image_path)

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Asegúrese de que la carpeta 'static' existe
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
