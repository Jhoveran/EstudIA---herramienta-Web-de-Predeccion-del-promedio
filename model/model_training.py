import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
from scipy import stats
from math import sqrt
%matplotlib inline

df = pd.read_csv("D:\Proyecto POO\student+performance\student\student-por.csv", sep = ';')
df.head(5)

#DATA CLEANING
# revision de valores faltantes
df.isnull().sum()

# revision de duplicados
df.duplicated().value_counts()

#ONE-HOT ENCODING
# Listado de columnas a codificar
Columns = ["school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob", 
           "reason", "guardian", "schoolsup", "famsup", "paid", 
           "activities", "nursery", "higher", "internet", "romantic"]

# Aplica One-Hot Encoding a las columnas seleccionadas y actualizar el dataframe original
df = pd.get_dummies(df, columns=Columns)

# Visualiza el resultado para comprobar las nuevas columnas

# Guarda las columnas del DataFrame de entrenamiento
columnas_entrenamiento = df.columns
joblib.dump(columnas_entrenamiento, 'columnas_entrenamiento.pkl')
print(columnas_entrenamiento)

# Calcula la matriz de correlación
corr = df.corr()

# Crea una figura con un tamaño grande
plt.figure(figsize=(50,50))

# Dibuja el mapa de calor usando seaborn, con anotaciones y un mapa de colores azul
sns.heatmap(corr, annot=True, cmap="Blues")

# Establece el título de la gráfica
plt.title('Mapa de Calor de Correlación', fontsize=20)

#ELIMINAR VALORES ATIPICOS
# revision de valores atipicos en feature 'G1'
plt.figure(figsize = (60,30))
sns.boxplot(x='G1', data=df)
sns.stripplot(x='G1', data=df, color="#804630")

# revision de valores atipicos en feature 'G2'
plt.figure(figsize = (60,30))
sns.boxplot(x='G2', data=df)
sns.stripplot(x='G2', data=df, color="#804630")

# Seleccionar solo las columnas numéricas
numeric_df = df.select_dtypes(include=[np.number])

# Calcular el Z-score solo para las columnas numéricas
z_scores = np.abs(stats.zscore(numeric_df))

# Filtrar el DataFrame original basado en el Z-score de las variables numéricas
df = df[(z_scores < 3).all(axis=1)]

# revision de valores atipicos en feature 'G1'
plt.figure(figsize = (60,30))
sns.boxplot(x='G1', data=df)
sns.stripplot(x='G1', data=df, color="#804630")

# revision de valores atipicos en feature 'G2'
plt.figure(figsize = (60,30))
sns.boxplot(x='G2', data=df)
sns.stripplot(x='G2', data=df, color="#804630")

#FEATURE SELECTION
#Separar las características (features) y la variable objetivo (target)
x = df.drop('G3', axis=1) #creacion de un nuevo DataFrame
y = df['G3']

#all_features es una lista con los nombres de todos los feature
all_features = x.columns
all_features

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

# Tomar un objeto de la biblioteca para utilizar el modelo.
# Utilizar el criterio de Gini para definir la importancia de las características.
# creacion de una instancia de  clasificador de random forest
rfc = RandomForestClassifier(random_state=0) 

# entrenar el modelo de random forest utilizando x y etiquetas y
rfc.fit(x, y)

# seleccion de caracteristicas importantes 
selector = SelectFromModel(estimator=rfc, threshold="mean")

# entrenamiento del selector de caracteristicas
selector.fit(x, y)

# obtener las caracteristicas seleccionadas
selected_features = all_features[selector.get_support(indices=True)]
selected_features

#MODEL AND OPTIMIZATION
# modelo de regresion de random forest
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# features independientes y target variable
features = df[selected_features]  # Features
target = df['G3']  # Target variable

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Inicializar la regresión de random forest con parámetros específicos
RFR = RandomForestRegressor(random_state=100, criterion='squared_error', max_depth=30, min_samples_leaf=5, n_jobs=1)

# Entrenar la regresión
RFR.fit(X_train, y_train)

# Predecir sobre los datos de prueba
y_pred = RFR.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

rmse = sqrt(mse)

r2 = r2_score(y_test, y_pred)

print("RFR Mean Squared Error MSE:", mse)
print("RFR Root Mean Squared Error RMSE:", rmse)
print("RFR R^2 Score:", r2)

#GUARDAR MODELO
from sklearn.ensemble import RandomForestRegressor
import joblib

# Guardar el modelo entrenado en un archivo
joblib.dump(RFR, 'modelo_random_fores_entrenado.pkl')

print("Modelo guardado exitosamente.")
