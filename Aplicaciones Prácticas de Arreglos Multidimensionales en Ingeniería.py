import numpy as np

# PROBLEMA 1: Análisis de Fuerzas en una Estructura (Matriz 3x3)
def resolver_problema_1():
    """
    Representa un sistema de fuerzas aplicadas en una estructura de 3x3 nodos.
    Calcula las reacciones globales utilizando las leyes de la estática (Sumatoria de 
    Fuerzas en X, Y y Momentos de flexión respecto al origen).
    """
    print("\n--- PROBLEMA 1: Análisis de Fuerzas en una Estructura ---")
    
    # Matriz 3x3 que representa las fuerzas aplicadas en cada nodo (ej. en Newtons)
    # Filas: Coordenada Y (0 a 2), Columnas: Coordenada X (0 a 2)
    fuerzas_matriz = np.array([
        [10.5, 15.0, 12.0],
        [8.0,  22.5, 14.1],
        [5.0,  18.0, 20.0]
    ])
    
    print("Matriz de fuerzas aplicadas (N) en la estructura 3x3:\n", fuerzas_matriz)
    
    # 1. Aplicación de Leyes de Estática: Sumatoria de fuerzas totales
    suma_total_fuerzas = np.sum(fuerzas_matriz)
    
    # 2. Suposición de coordenadas espaciales para los nodos (separación de 1 metro)
    reacciones_x = np.sum(fuerzas_matriz, axis=0)  # Reacciones distribuidas en soportes verticales
    reacciones_y = np.sum(fuerzas_matriz, axis=1)  # Reacciones distribuidas en soportes horizontales
    
    # 3. Cálculo de momento flector respecto al nodo origen (0,0) M = F * distancia
    momento_total = 0.0
    filas, columnas = fuerzas_matriz.shape
    for i in range(filas):
        for j in range(columnas):
            # Brazo de palanca vectorial simple (x, y)
            brazo_palanca = np.sqrt(i**2 + j**2)
            momento_total += fuerzas_matriz[i, j] * brazo_palanca

    print(f"[ESTÁTICA] Sumatoria total de fuerza aplicada: {suma_total_fuerzas:.2f} N")
    print(f"[ESTÁTICA] Reacciones calculadas en soportes eje X: {reacciones_x}")
    print(f"[ESTÁTICA] Reacciones calculadas en soportes eje Y: {reacciones_y}")
    print(f"[ESTÁTICA] Momento flector total acumulado: {momento_total:.2f} N·m")


# PROBLEMA 2: Simulación de Fluido en una Cuadrícula 3D (3x3x3)
def resolver_problema_2():
    """
    Utiliza un arreglo tridimensional (3x3x3) para simular el estado de un fluido 
    (Presión, Temperatura y Velocidad). Actualiza la presión propagando ondas 
    mediante un operador de vecindad (Stencil de 6 vecinos adyacentes).
    """
    print("\n--- PROBLEMA 2: Simulación de Fluido en Cuadrícula 3D ---")
    
    # Dimensiones del espacio 3x3x3
    # Canal 0: Presión (Pa), Canal 1: Temperatura (°C), Canal 2: Velocidad (m/s)
    # O representamos con 3 matrices independientes de 3x3x3 para claridad óptima.
    presion = np.random.uniform(100.0, 105.0, (3, 3, 3))
    temperatura = np.random.uniform(20.0, 25.0, (3, 3, 3))
    velocidad = np.random.uniform(1.0, 5.0, (3, 3, 3))
    
    print("Estado inicial de presión en la celda central (1,1,1):", presion[1, 1, 1])
    
    # Simulación de propagación de ondas de presión (Ecuación de onda discreta / Promedio de vecinos)
    # Se actualiza cada celda interna tomando el promedio de sus 6 vecinos directos (von Neumann neighborhood)
    nueva_presion = presion.copy()
    
    # Iteramos sobre celdas internas para evitar desbordamientos de frontera simplificados
    for z in range(1, 2):
        for y in range(1, 2):
            for x in range(1, 2):
                vecinos = [
                    presion[z+1, y, x], presion[z-1, y, x],
                    presion[z, y+1, x], presion[z, y-1, x],
                    presion[z, y, x+1], presion[z, y, x-1]
                ]
                # Actualización de presión basada en la media de los vecinos adyacentes (difusión de onda)
                nueva_presion[z, y, x] = np.mean(vecinos) * 1.01  # Coeficiente de propagación

    print("Estado de presión actualizado tras la propagación de onda:", round(nueva_presion[1, 1, 1], 4))
    print("Simulación de volumen 3D completada con éxito.")


# PROBLEMA 3: Análisis de Imágenes Médicas en 3D
def resolver_problema_3():
    """
    Simula un volumen 3D de imágenes médicas (ej. capas de tomografía computarizada) 
    y aplica un filtro espacial de suavizado (promedio tridimensional) para reducción de ruido.
    """
    print("\n--- PROBLEMA 3: Análisis de Imágenes Médicas en 3D ---")
    
    # Volumen 3D con ruido simulado (ej. 4 capas de 5x5 píxeles)
    volumen_original = np.random.randint(50, 200, size=(4, 5, 5)).astype(float)
    # Inyectamos ruido gaussiano artificial
    ruido = np.random.normal(0, 15, size=(4, 5, 5))
    volumen_con_ruido = np.clip(volumen_original + ruido, 0, 255)
    
    print("Capa 0 del volumen con ruido:\n", np.round(volumen_con_ruido[0], 1))
    
    # Aplicación de filtro de promedio espacial 3D (kernel de 3x3x3 simplificado por capas)
    volumen_suavizado = volumen_con_ruido.copy()
    profundidad, alto, ancho = volumen_con_ruido.shape
    
    for z in range(1, profundidad - 1):
        for y in range(1, alto - 1):
            for x in range(1, ancho - 1):
                # Extraer vecindad cúbica de 3x3x3 alrededor del vóxel
                vecindario = volumen_con_ruido[z-1:z+2, y-1:y+2, x-1:x+2]
                volumen_suavizado[z, y, x] = np.mean(vecindario)
                
    print("Capa 1 del volumen tras aplicar filtro de suavizado espacial 3D:\n", np.round(volumen_suavizado[1], 1))
    print("[ANÁLISIS] El suavizado reduce la varianza local del ruido, mejorando la relación señal-ruido (SNR).")


# PROBLEMA 4: Manejo de Datos en una Tabla de Sensores (5x5)
def resolver_problema_4():
    """
    Organiza datos de 5 sensores en 5 momentos del tiempo en una matriz bidimensional 5x5.
    Calcula con precisión matemática la media y la desviación estándar por filas y columnas.
    """
    print("\n--- PROBLEMA 4: Manejo de Datos en Tabla de Sensores (5x5) ---")
    
    # Matriz 5x5: 5 filas (momentos t0 a t4), 5 columnas (Sensores S1 a S5)
    np.random.seed(42)
    datos_sensores = np.round(np.random.uniform(18.0, 35.0, (5, 5)), 2)
    
    print("Matriz de temperaturas (Filas = Tiempos, Columnas = Sensores S1-S5):\n", datos_sensores)
    
    # Análisis estadístico por columnas (Sensores): axis=0
    media_sensores = np.mean(datos_sensores, axis=0)
    desvest_sensores = np.std(datos_sensores, axis=0, ddof=1) # Desviación estándar muestral
    
    # Análisis estadístico por filas (Momentos en el tiempo): axis=1
    media_momentos = np.mean(datos_sensores, axis=1)
    desvest_momentos = np.std(datos_sensores, axis=1, ddof=1)
    
    print("\n--- Estadísticas por Sensor (Columnas) ---")
    for idx, (m, d) in enumerate(zip(media_sensores, desvest_sensores), start=1):
        print(f"Sensor S{idx} -> Media: {m:.2f} °C | Desviación Estándar: {d:.2f}")
        
    print("\n--- Estadísticas por Momento en el Tiempo (Filas) ---")
    for idx, (m, d) in enumerate(zip(media_momentos, desvest_momentos), start=0):
        print(f"Momento t{idx} -> Media: {m:.2f} °C | Desviación Estándar: {d:.2f}")


# PROBLEMA 5: Transformación de Coordenadas en un Sistema Cartesiano
def resolver_problema_5():
    """
    Representa puntos en un plano cartesiano mediante un arreglo bidimensional y 
    aplica una transformación lineal (Matriz de Rotación y Traslación homogénea).
    """
    print("\n--- PROBLEMA 5: Transformación de Coordenadas Cartesianas ---")
    
    # Conjunto de 4 puntos en coordenadas 2D (Matriz de forma [N_puntos, 2])
    puntos_originales = np.array([
        [1.0, 1.0],
        [3.0, 1.0],
        [3.0, 3.0],
        [1.0, 3.0]
    ])
    print("Puntos originales (X, Y):\n", puntos_originales)
    
    # Definir transformación lineal: Rotación de 90 grados en sentido antihorario
    # Matriz de rotación 2D para theta = 90 grados (pi / 2 radianes)
    theta = np.pi / 2
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    
    matriz_rotacion = np.array([
        [cos_t, -sin_t],
        [sin_t,  cos_t]
    ])
    
    vector_traslacion = np.array([2.0, 4.0]) # Desplazamiento en X e Y
    
    # Aplicar transformación lineal punto a punto: P' = (R @ P.T).T + Traslación
    puntos_transformados = np.dot(puntos_originales, matriz_rotacion.T) + vector_traslacion
    
    print("Matriz de Rotación (90°):\n", np.round(matriz_rotacion, 2))
    print("Puntos transformados (Rotados 90° y trasladados +[2, 4]):\n", np.round(puntos_transformados, 2))


# MENÚ PRINCIPAL
if __name__ == "__main__":
    while True:
        print(" TAREA: APLICACIÓN DE ARREGLOS MULTIDIMENSIONALES EN INGENIERÍA")
        print("1. Problema 1: Análisis de Fuerzas en Estructura (3x3)")
        print("2. Problema 2: Simulación de Fluido en Cuadrícula 3D (3x3x3)")
        print("3. Problema 3: Análisis de Imágenes Médicas 3D")
        print("4. Problema 4: Manejo de Datos en Tabla de Sensores (5x5)")
        print("5. Problema 5: Transformación de Coordenadas Cartesianas")
        print("6. Salir")
        
        opcion = input("\nSeleccione una opción (1-6): ").strip()
        
        if opcion == '1':
            resolver_problema_1()
        elif opcion == '2':
            resolver_problema_2()
        elif opcion == '3':
            resolver_problema_3()
        elif opcion == '4':
            resolver_problema_4()
        elif opcion == '5':
            resolver_problema_5()
        elif opcion == '6':
            print("\n¡Saliendo del programa con éxito!")
            break
        else:
            print("\n[Error] Opción inválida. Intente de nuevo.")
