import os
import unittest
import tempfile
from unittest.mock import Mock, patch
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from app import StudentPredictor, GraphPlotter, create_app

class TestStudentPredictor(unittest.TestCase):
    def setUp(self):
        # Crear un modelo simulado para realizar pruebas
        self.mock_model = Mock()
        self.mock_model.predict.return_value = np.array([80])

    def test_load_model_success(self):
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as tmp_file:
            joblib.dump(self.mock_model, tmp_file.name)
        
        predictor = StudentPredictor(model_path=tmp_file.name)
        self.assertIsNotNone(predictor.model)
        os.unlink(tmp_file.name)

    def test_load_model_failure(self):
        with self.assertRaises(ValueError):
            StudentPredictor(model_path='non_existent_path.pkl')

    def test_prepare_student_data(self):
        predictor = StudentPredictor()
        features = {
            'age': 18, 'Medu': 2, 'Fedu': 3, 'traveltime': 3,
            'studytime': 2, 'famrel': 4, 'freetime': 3,
            'goout': 2, 'Walc': 1, 'health': 3,
            'absences': 5, 'G1': 15, 'G2': 16  # Grades within 0-20 range
        }
        df = predictor.prepare_student_data(features)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['age'], 18)

    def test_predict_grades(self):
        with patch.object(StudentPredictor, 'load_model', return_value=self.mock_model):
            predictor = StudentPredictor()
            features_list = [
                {
                    'age': 18, 'Medu': 2, 'Fedu': 3, 'traveltime': 3,
                    'studytime': 2, 'famrel': 4, 'freetime': 3,
                    'goout': 2, 'Walc': 1, 'health': 3,
                    'absences': 5, 'G1': 15, 'G2': 16  # Grades within 0-20 range
                }
            ]
            predicciones = predictor.predict_grades(features_list)
            
            self.assertEqual(len(predicciones), 3)
            self.assertEqual(len(predicciones[0]), 6)

class TestGraphPlotter(unittest.TestCase):
    def test_plot_predictions(self):
        predicciones = [
            [15, 16, 17, 18, 19, 20], 
            [10, 11, 12, 13, 14, 15],
            [5, 6, 7, 8, 9, 10]
        ]
        promedio_reales = [12, 13, 14, 15]
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, 'test_grafica.png')
            graph_path = GraphPlotter.plot_predictions(predicciones, promedio_reales, output_path)
            
            self.assertTrue(os.path.exists(graph_path))
            self.assertTrue(os.path.getsize(graph_path) > 0)

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        # Simular las dependencias
        self.mock_predictor = Mock(spec=StudentPredictor)
        self.mock_plotter = Mock(spec=GraphPlotter)
        
        # Crear un cliente de prueba
        self.app = create_app(self.mock_predictor, self.mock_plotter)
        self.client = self.app.test_client()

    def test_inicio_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_route(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_predict_route_success(self):
        # Preparar valores de retorno simulados
        self.mock_predictor.predict_grades.return_value = [
            [15, 16, 17, 18, 19, 20],
            [10, 11, 12, 13, 14, 15],
            [5, 6, 7, 8, 9, 10]
        ]
        self.mock_plotter.plot_predictions.return_value = 'static/grafica.png'

        # Simular el envio de formulario
        form_data = {
            'edad': '18', 'eduPadre': '2', 'eduMadre': '3', 
            'tiempoEstudio': '2', 'relacionesFamiliares': '4', 
            'tiempoLibre': '3', 'salirConAmigos': '2', 
            'consumoAlcohol': '1', 'salud': '3', 
            'ausencias': '5', 'promedioCiclo1': '12', 
            'promedioCiclo2': '13', 'promedioCiclo3': '14', 
            'promedioCiclo4': '15'
        }
        
        response = self.client.post('/predict', data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_predict_route_failure(self):
        # Simular un escenario donde la prediccion falla 
        self.mock_predictor.predict_grades.side_effect = ValueError("Prediction error")
        
        form_data = {
            'edad': '18', 'eduPadre': '2', 'eduMadre': '3', 
            'tiempoEstudio': '2', 'relacionesFamiliares': '4', 
            'tiempoLibre': '3', 'salirConAmigos': '2', 
            'consumoAlcohol': '1', 'salud': '3', 
            'ausencias': '5', 'promedioCiclo1': '12', 
            'promedioCiclo2': '13', 'promedioCiclo3': '14', 
            'promedioCiclo4': '15'
        }
        
        response = self.client.post('/predict', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
