import random
import math

# Función para calcular la distancia euclidiana entre dos puntos (ciudades)
def distancia(ciudad1, ciudad2):
    return math.sqrt((ciudad1[0] - ciudad2[0])**2 + (ciudad1[1] - ciudad2[1])**2)

# Función para calcular la distancia total de una ruta
def distancia_total(ruta, ciudades):
    distancia_total = 0
    for i in range(len(ruta) - 1):
        distancia_total += distancia(ciudades[ruta[i]], ciudades[ruta[i+1]])
    distancia_total += distancia(ciudades[ruta[-1]], ciudades[ruta[0]]) # Distancia de regreso al punto de partida
    return distancia_total

# Función para generar una solución inicial aleatoria
def solucion_inicial(ciudades):
    ruta = list(range(len(ciudades)))
    random.shuffle(ruta)
    return ruta

# Función para realizar el algoritmo de recorrido simulado
def recorrido_simulado(ciudades, temperatura_inicial=10000, factor_enfriamiento=0.95, iteraciones_por_temperatura=1000):
    mejor_ruta = solucion_inicial(ciudades)
    mejor_distancia = distancia_total(mejor_ruta, ciudades)
    temperatura = temperatura_inicial
    
    while temperatura > 1:
        for _ in range(iteraciones_por_temperatura):
            # Generar una nueva solución vecina intercambiando dos ciudades aleatorias
            nueva_ruta = mejor_ruta[:]
            indice1, indice2 = random.sample(range(len(ciudades)), 2)
            nueva_ruta[indice1], nueva_ruta[indice2] = nueva_ruta[indice2], nueva_ruta[indice1]
            
            # Calcular la distancia de la nueva ruta
            nueva_distancia = distancia_total(nueva_ruta, ciudades)
            
            # Calcular la diferencia entre las distancias
            diferencia = nueva_distancia - mejor_distancia
            
            # Si la nueva ruta es mejor o es aceptada según la probabilidad de Boltzmann
            if diferencia < 0 or random.random() < math.exp(-diferencia / temperatura):
                mejor_ruta = nueva_ruta
                mejor_distancia = nueva_distancia
        
        # Enfriar el sistema
        temperatura *= factor_enfriamiento
    
    return mejor_ruta, mejor_distancia

# Ejemplo de uso
if __name__ == "__main__":
    # Definir las coordenadas de las ciudades
    ciudades = [(0, 0), (1, 3), (2, 5), (3, 2), (5, 2)]
    
    # Resolver el problema del viajante
    mejor_ruta, mejor_distancia = recorrido_simulado(ciudades)
    
    # Mostrar la mejor ruta encontrada y su distancia
    print("Mejor ruta encontrada:", mejor_ruta)
    print("Distancia total de la mejor ruta:", mejor_distancia)