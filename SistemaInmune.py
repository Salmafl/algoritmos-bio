import numpy as np

# Función para generar datos aleatorios
def generar_datos_normales(mu, sigma, n):
    return np.random.normal(mu, sigma, n)

# Función para calcular la afinidad entre una célula y los datos
def calcular_afinidad(celula, datos):
    return np.sum((celula - datos)**2)

# Función para seleccionar las células más aptas
def seleccionar_mejores_celulas(celulas, datos, num_mejores):
    afinidades = np.array([calcular_afinidad(c, datos) for c in celulas])
    mejores_indices = np.argsort(afinidades)[:num_mejores]
    return [celulas[i] for i in mejores_indices]

# Función para mutar las células seleccionadas
def mutar_celulas(celulas_seleccionadas, tasa_mutacion):
    nuevas_celulas = []
    for celula in celulas_seleccionadas:
        nueva_celula = celula + np.random.normal(0, tasa_mutacion, len(celula))
        nuevas_celulas.append(nueva_celula)
    return nuevas_celulas

# Función para detectar anomalías en los datos
def detectar_anomalias(datos, num_celulas=100, tasa_mutacion=0.1, iteraciones=10):
    # Inicializar el conjunto de células aleatorias
    celulas = [np.random.rand(len(datos)) for _ in range(num_celulas)]
    
    for _ in range(iteraciones):
        # Seleccionar las mejores células
        mejores_celulas = seleccionar_mejores_celulas(celulas, datos, int(num_celulas / 10))
        
        # Mutar las células seleccionadas
        celulas_mutadas = mutar_celulas(mejores_celulas, tasa_mutacion)
        
        # Reemplazar las células menos aptas con las mutadas
        celulas.extend(celulas_mutadas)
        celulas.sort(key=lambda x: calcular_afinidad(x, datos))
        celulas = celulas[:num_celulas]
    
    # Calcular la afinidad de cada célula con los datos
    afinidades = [calcular_afinidad(c, datos) for c in celulas]
    
    # Calcular el umbral como la media más una desviación estándar
    umbral = np.mean(afinidades) + np.std(afinidades)
    
    # Identificar anomalías
    anomalias = [i for i, a in enumerate(afinidades) if a > umbral]
    
    return anomalias, celulas

# Ejemplo de uso
if __name__ == "__main__":
    # Generar datos normales y datos con anomalías
    datos_normales = generar_datos_normales(0, 1, 1000)
    datos_anomalias = np.concatenate((generar_datos_normales(5, 1, 50), generar_datos_normales(-5, 1, 50)))
    todos_los_datos = np.concatenate((datos_normales, datos_anomalias))
    
    # Detectar anomalías
    anomalias_detectadas, celulas_finales = detectar_anomalias(todos_los_datos)
    
    # Imprimir resultados
    print("Índices de anomalías detectadas:", anomalias_detectadas)
    print("Número de anomalías detectadas:", len(anomalias_detectadas))