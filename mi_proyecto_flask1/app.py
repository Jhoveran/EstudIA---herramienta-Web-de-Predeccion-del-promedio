import os
import numpy as np
import joblib
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, request, jsonify, render_template, send_from_directory

class StudentPredictor:
    def __init__(self, model_path=None):
        """
        Inicialice el predictor con una ruta de modelo.

        Args:
        model_path (str, opcional): Ruta al modelo entrenado.
        El valor predeterminado es una ruta predefinida si no se proporciona.
        """
        if model_path is None:
            model_path = 'D:\\Proyecto POO\\PLATAFORMA\\env\\mi_proyecto_flask1\\mi_proyecto_flask1\\modelo_random_forest_entrenado.pkl'
        
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        """
        Cargue el modelo de aprendizaje automático entrenado.

        Args:
        model_path (str): Ruta al archivo del modelo.

        Devuelve:
        Objeto del modelo listo para predicciones
        """
        try:
            return joblib.load(model_path)
        except Exception as e:
            raise ValueError(f"Error cargar model: {e}")

    def prepare_student_data(self, features):
        """
        Preparar los datos de los estudiantes para la predicción.

        Args:
        features (dict): Diccionario de características del estudiante

        Retornos:
        pandas.DataFrame: Datos preparados del estudiante
        """
        return pd.DataFrame([features])

    def predict_grades(self, features_list):
        """
        Predecir calificaciones para varios ciclos.

        Args:
        features_list (lista): Lista de diccionarios de características para cada ciclo

        Retornos:
        list: Calificaciones predichas para cada ciclo
        """
        predicciones = [[0] * 6 for _ in range(3)]

        for i in range(len(features_list) - 1):
            datos_alumno = features_list[i]

            for j in range(6):
                df_alumno = self.prepare_student_data(datos_alumno)
                prediccion_G3 = self.model.predict(df_alumno)[0]
                predicciones[i][j] = prediccion_G3

                # Update G1 and G2 for next iteration
                datos_alumno['G1'] = datos_alumno['G2']
                datos_alumno['G2'] = prediccion_G3

        return predicciones

class GraphPlotter:
    @staticmethod
    def plot_predictions(predicciones, promedio_reales, output_path='static/grafica.png'):
        """
        Crea un gráfico de calificaciones reales y predichas.

        Args:
        predicciones(lista): Calificaciones predichas
        promedio_reales(lista): Calificaciones reales
        output_path(str): Ruta para guardar el gráfico

        Retornos:
        str: Ruta al gráfico guardado
        """
        ciclos = [f'Ciclo {i+1}' for i in range(10)]
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(ciclos[:4], promedio_reales, marker='o', color='red', label="Valores Reales")

        colores_prediccion = ['blue', 'green', 'purple']

        for i in range(3):
            inicio_x = i + 2
            x_range = ciclos[inicio_x:inicio_x+6]
            ax.plot(x_range, predicciones[i], marker='o', color=colores_prediccion[i], 
                    label=f"Predicciones {i+1} (val{i+1}-val{i+2})")

        ax.set_title("Predicción de Promedios Proximos ciclos con RF")
        ax.set_xlabel("Ciclos")
        ax.set_ylabel("Promedio Predicho")
        ax.legend()
        ax.grid(True)

        try:
            fig.savefig(output_path)
            plt.close(fig)
            return output_path
        except Exception as e:
            raise ValueError(f"Error saving graph: {e}")

def create_app(predictor=None, plotter=None):
    """
    Crear y configurar la aplicación Flask.

    Args:
    predictor (StudentPredictor, opcional): instancia del predictor
    plotter (GraphPlotter, opcional): instancia del trazador de gráficos

    Devuelve:
    Flask: aplicación Flask configurada
    """
    app = Flask(__name__)
    predictor = predictor or StudentPredictor()
    plotter = plotter or GraphPlotter()

    @app.route('/')
    def inicio():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route("/predict", methods=['POST'])
    def predict():
        try:
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

            age, fedu, medu, studytime, famrel, freetime, goout, walc, health, absences, val1, val2, val3, val4 = int_features
            promedio_reales = [val1, val2, val3, val4]

            features_list = []
            for i in range(len(promedio_reales) - 1):
                features_list.append({
                    'age': age, 'Medu': medu, 'Fedu': fedu, 'traveltime': 3,
                    'studytime': studytime, 'famrel': famrel, 'freetime': freetime,
                    'goout': goout, 'Walc': walc, 'health': health,
                    'absences': absences, 'G1': promedio_reales[i], 
                    'G2': promedio_reales[i + 1]
                })

            predicciones = predictor.predict_grades(features_list)
            graph_path = plotter.plot_predictions(predicciones, promedio_reales)
            return render_template('resultados.html', image_url=graph_path)

        except Exception as e:
            return render_template('error.html', message=str(e))

    @app.route('/static/<filename>')
    def serve_static(filename):
        return send_from_directory('static', filename)

    return app

def main():
    app = create_app()
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)

if __name__ == '__main__':
    main()
