"""
TAREA: APLICACIÓN DE ARREGLOS MULTIDIMENSIONALES EN INGENIERÍA

Solución modular de cinco problemas usando NumPy y Matplotlib.
Los modelos físicos son simplificaciones didácticas y sus supuestos
se explican en los comentarios y en el README.
"""

import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# PROBLEMA 1: ANÁLISIS DE FUERZAS EN UNA ESTRUCTURA 3x3
# =============================================================================
def resolver_problema_1():
    """
    Calcula las reacciones de una viga simplemente apoyada a partir de una
    matriz 3x3 de cargas verticales.

    Modelo adoptado:
    - Cada columna representa una posición de la viga: x = 0, 1 y 2 metros.
    - Las tres cargas de cada columna se agrupan como una carga equivalente
      aplicada en esa posición.
    - La viga tiene dos apoyos: A en x=0 m y B en x=2 m.
    - Las cargas son verticales y se expresan como magnitudes positivas.
    """
    print("\n--- PROBLEMA 1: Análisis de Fuerzas en una Estructura ---")

    cargas = np.array([
        [10.5, 15.0, 12.0],
        [8.0, 22.5, 14.1],
        [5.0, 18.0, 20.0]
    ], dtype=float)

    separacion = 1.0  # metros entre columnas
    posiciones_x = np.arange(cargas.shape[1]) * separacion
    cargas_por_posicion = np.sum(cargas, axis=0)

    longitud = posiciones_x[-1]
    fuerza_total = np.sum(cargas_por_posicion)

    # Momento de las cargas respecto al apoyo A.
    momento_cargas_A = np.sum(cargas_por_posicion * posiciones_x)

    # Equilibrio: RB * L - momento_cargas_A = 0
    reaccion_B = momento_cargas_A / longitud

    # Equilibrio vertical: RA + RB - fuerza_total = 0
    reaccion_A = fuerza_total - reaccion_B

    # Comprobaciones numéricas de equilibrio.
    suma_fuerzas = reaccion_A + reaccion_B - fuerza_total
    suma_momentos_A = reaccion_B * longitud - momento_cargas_A

    print("Matriz de cargas verticales (N):\n", cargas)
    print("\nCargas equivalentes por posición x=0, 1 y 2 m (N):",
          np.round(cargas_por_posicion, 2))
    print(f"\nCarga vertical total: {fuerza_total:.2f} N")
    print(f"Momento de las cargas respecto a A: {momento_cargas_A:.2f} N·m")
    print(f"Reacción vertical en A (x=0 m): {reaccion_A:.2f} N")
    print(f"Reacción vertical en B (x={longitud:.1f} m): {reaccion_B:.2f} N")
    print(f"Comprobación de sumatoria de fuerzas: {suma_fuerzas:.10f} N")
    print(f"Comprobación de sumatoria de momentos: {suma_momentos_A:.10f} N·m")

    print("\nNota: es un modelo equivalente de viga simplemente apoyada; "
          "no representa el análisis completo de una losa bidimensional.")


# =============================================================================
# PROBLEMA 2: SIMULACIÓN DE FLUIDO EN UNA CUADRÍCULA 3D
# =============================================================================
def promedio_seis_vecinos(campo):
    """
    Calcula el promedio de los seis vecinos ortogonales de cada celda.
    Se utiliza padding de borde para definir los vecinos en las fronteras.
    """
    padded = np.pad(campo, pad_width=1, mode="edge")

    vecino_z_mas = padded[2:, 1:-1, 1:-1]
    vecino_z_menos = padded[:-2, 1:-1, 1:-1]
    vecino_y_mas = padded[1:-1, 2:, 1:-1]
    vecino_y_menos = padded[1:-1, :-2, 1:-1]
    vecino_x_mas = padded[1:-1, 1:-1, 2:]
    vecino_x_menos = padded[1:-1, 1:-1, :-2]

    return (
        vecino_z_mas + vecino_z_menos +
        vecino_y_mas + vecino_y_menos +
        vecino_x_mas + vecino_x_menos
    ) / 6.0


def resolver_problema_2():
    """
    Simula un paso de evolución de tres campos 3D: presión, temperatura
    y rapidez del fluido.

    La presión usa una ecuación de onda discreta simplificada:
    p(t+1) = 2*p(t) - p(t-1) + c²*Laplaciano(p(t)).
    Temperatura y rapidez usan una actualización difusiva basada en
    el promedio de los seis vecinos. Se actualizan las 27 celdas,
    usando condiciones de frontera de borde replicado.
    """
    print("\n--- PROBLEMA 2: Simulación de Fluido 3D (3x3x3) ---")

    forma = (3, 3, 3)

    # Estado anterior de presión y estado actual con una perturbación central.
    presion_anterior = np.full(forma, 100.0)
    presion_actual = presion_anterior.copy()
    presion_actual[1, 1, 1] = 110.0

    temperatura = np.full(forma, 22.0)
    temperatura[1, 1, 1] = 28.0

    velocidad = np.full(forma, 2.0)
    velocidad[1, 1, 1] = 5.0

    # Laplaciano discreto: suma de vecinos menos seis veces el valor central.
    promedio_presion = promedio_seis_vecinos(presion_actual)
    laplaciano_presion = 6.0 * (promedio_presion - presion_actual)

    coeficiente_onda = 0.10
    nueva_presion = (
        2.0 * presion_actual - presion_anterior
        + (coeficiente_onda ** 2) * laplaciano_presion
    )

    # Difusión simplificada de temperatura y rapidez.
    alpha_temperatura = 0.20
    alpha_velocidad = 0.15

    nueva_temperatura = temperatura + alpha_temperatura * (
        promedio_seis_vecinos(temperatura) - temperatura
    )
    nueva_velocidad = velocidad + alpha_velocidad * (
        promedio_seis_vecinos(velocidad) - velocidad
    )

    print("Dimensiones de cada campo:", forma)
    print(f"Presión central inicial: {presion_actual[1, 1, 1]:.2f} kPa")
    print(f"Presión central actualizada: {nueva_presion[1, 1, 1]:.4f} kPa")
    print(f"Temperatura central inicial: {temperatura[1, 1, 1]:.2f} °C")
    print(f"Temperatura central actualizada: {nueva_temperatura[1, 1, 1]:.4f} °C")
    print(f"Rapidez central inicial: {velocidad[1, 1, 1]:.2f} m/s")
    print(f"Rapidez central actualizada: {nueva_velocidad[1, 1, 1]:.4f} m/s")
    print("\nPresión actualizada en todo el volumen (kPa):\n",
          np.round(nueva_presion, 3))
    print("\nTemperatura actualizada en todo el volumen (°C):\n",
          np.round(nueva_temperatura, 3))
    print("\nRapidez actualizada en todo el volumen (m/s):\n",
          np.round(nueva_velocidad, 3))

    print("\nNota: es un modelo numérico didáctico simplificado, no una "
          "simulación CFD completa.")


# =============================================================================
# PROBLEMA 3: ANÁLISIS DE IMÁGENES MÉDICAS EN 3D
# =============================================================================
def resolver_problema_3():
    """
    Genera un volumen 3D sintético, añade ruido y aplica un filtro de
    promedio 3x3x3. El padding 'edge' replica los valores de los bordes
    para poder filtrar también los vóxeles de las fronteras.
    """
    print("\n--- PROBLEMA 3: Análisis de Imágenes Médicas 3D ---")

    np.random.seed(42)
    volumen_original = np.random.randint(60, 180, size=(4, 5, 5)).astype(float)
    ruido = np.random.normal(0, 12, size=volumen_original.shape)
    volumen_con_ruido = np.clip(volumen_original + ruido, 0, 255)

    volumen_padded = np.pad(
        volumen_con_ruido, pad_width=1, mode="edge"
    )
    volumen_suavizado = np.zeros_like(volumen_con_ruido)

    profundidad, alto, ancho = volumen_con_ruido.shape

    # Se calcula el promedio de los 27 vóxeles de cada vecindad 3x3x3.
    for z in range(profundidad):
        for y in range(alto):
            for x in range(ancho):
                vecindario = volumen_padded[z:z + 3, y:y + 3, x:x + 3]
                volumen_suavizado[z, y, x] = np.mean(vecindario)

    print("Dimensiones del volumen:", volumen_con_ruido.shape)
    print("\nCapa 1 con ruido:\n", np.round(volumen_con_ruido[1], 1))
    print("\nCapa 1 suavizada:\n", np.round(volumen_suavizado[1], 1))
    print(f"\nDesviación estándar de capa ruidosa: "
          f"{np.std(volumen_con_ruido[1]):.2f}")
    print(f"Desviación estándar de capa suavizada: "
          f"{np.std(volumen_suavizado[1]):.2f}")

    # Comparación visual de la misma capa antes y después del filtro.
    fig, ejes = plt.subplots(1, 2, figsize=(10, 4))

    imagen_1 = ejes[0].imshow(volumen_con_ruido[1], cmap="gray", vmin=0, vmax=255)
    ejes[0].set_title("Capa 1 con ruido")
    ejes[0].set_xlabel("Coordenada X")
    ejes[0].set_ylabel("Coordenada Y")
    fig.colorbar(imagen_1, ax=ejes[0], fraction=0.046, label="Intensidad")

    imagen_2 = ejes[1].imshow(volumen_suavizado[1], cmap="gray", vmin=0, vmax=255)
    ejes[1].set_title("Capa 1 suavizada 3x3x3")
    ejes[1].set_xlabel("Coordenada X")
    ejes[1].set_ylabel("Coordenada Y")
    fig.colorbar(imagen_2, ax=ejes[1], fraction=0.046, label="Intensidad")

    fig.suptitle("Comparación del volumen médico sintético")
    plt.tight_layout()
    plt.show()


# =============================================================================
# PROBLEMA 4: MANEJO DE DATOS EN UNA TABLA DE SENSORES 5x5
# =============================================================================
def resolver_problema_4():
    """
    Organiza lecturas de cinco sensores en cinco momentos.
    Calcula medias y desviaciones estándar muestrales (ddof=1) por
    columnas y filas, y presenta un mapa de calor y un gráfico de barras.
    """
    print("\n--- PROBLEMA 4: Tabla de Sensores (5x5) ---")

    np.random.seed(2026)
    datos_sensores = np.round(
        np.random.uniform(18.0, 32.0, (5, 5)), 2
    )

    media_sensores = np.mean(datos_sensores, axis=0)
    desv_sensores = np.std(datos_sensores, axis=0, ddof=1)
    media_momentos = np.mean(datos_sensores, axis=1)
    desv_momentos = np.std(datos_sensores, axis=1, ddof=1)

    print("Matriz de temperaturas (filas=tiempos, columnas=sensores):\n",
          datos_sensores)

    print("\nEstadísticas por sensor:")
    for indice, (media, desviacion) in enumerate(
        zip(media_sensores, desv_sensores), start=1
    ):
        print(f"Sensor S{indice}: media={media:.2f} °C, "
              f"desviación muestral={desviacion:.2f} °C")

    print("\nEstadísticas por momento:")
    for indice, (media, desviacion) in enumerate(
        zip(media_momentos, desv_momentos)
    ):
        print(f"Momento t{indice}: media={media:.2f} °C, "
              f"desviación muestral={desviacion:.2f} °C")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    mapa = ax1.imshow(datos_sensores, cmap="coolwarm", aspect="auto")
    fig.colorbar(mapa, ax=ax1, label="Temperatura (°C)")
    ax1.set_title("Mapa de calor de temperaturas")
    ax1.set_xlabel("Sensores")
    ax1.set_ylabel("Momentos")
    ax1.set_xticks(range(5), [f"S{i}" for i in range(1, 6)])
    ax1.set_yticks(range(5), [f"t{i}" for i in range(5)])

    ax2.bar(
        [f"S{i}" for i in range(1, 6)],
        media_sensores,
        yerr=desv_sensores,
        capsize=5
    )
    ax2.set_title("Media y desviación por sensor")
    ax2.set_xlabel("Sensor")
    ax2.set_ylabel("Temperatura (°C)")
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    fig.suptitle("Análisis estadístico de los sensores")
    plt.tight_layout()
    plt.show()


# =============================================================================
# PROBLEMA 5: TRANSFORMACIÓN DE COORDENADAS CARTESIANAS
# =============================================================================
def resolver_problema_5():
    """
    Aplica a cuatro puntos una rotación de 90 grados antihoraria y
    una traslación [2, 4]. Compara gráficamente las coordenadas.
    La traslación hace que la transformación compuesta sea afín.
    """
    print("\n--- PROBLEMA 5: Transformación de Coordenadas ---")

    puntos_originales = np.array([
        [1.0, 1.0],
        [3.0, 1.0],
        [3.0, 3.0],
        [1.0, 3.0]
    ])

    theta = np.pi / 2
    matriz_rotacion = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    vector_traslacion = np.array([2.0, 4.0])

    puntos_transformados = (
        puntos_originales @ matriz_rotacion.T + vector_traslacion
    )

    print("Puntos originales:\n", puntos_originales)
    print("\nMatriz de rotación de 90 grados:\n",
          np.round(matriz_rotacion, 2))
    print("\nVector de traslación:", vector_traslacion)
    print("Puntos transformados:\n", np.round(puntos_transformados, 2))

    # Se repite el primer punto al final para cerrar el polígono.
    original_cerrado = np.vstack(
        [puntos_originales, puntos_originales[0]]
    )
    transformado_cerrado = np.vstack(
        [puntos_transformados, puntos_transformados[0]]
    )

    plt.figure(figsize=(7, 7))
    plt.plot(
        original_cerrado[:, 0], original_cerrado[:, 1],
        "bo-", linewidth=2, label="Puntos originales"
    )
    plt.plot(
        transformado_cerrado[:, 0], transformado_cerrado[:, 1],
        "ro--", linewidth=2, label="Puntos transformados"
    )
    plt.axhline(0, color="gray", linewidth=1)
    plt.axvline(0, color="gray", linewidth=1)
    plt.grid(True, linestyle=":")
    plt.title("Rotación de 90° y traslación [2, 4]")
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.legend()
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


# =============================================================================
# MENÚ PRINCIPAL
# =============================================================================
def menu_principal():
    """Permite ejecutar individualmente cualquiera de los cinco problemas."""
    opciones = {
        "1": resolver_problema_1,
        "2": resolver_problema_2,
        "3": resolver_problema_3,
        "4": resolver_problema_4,
        "5": resolver_problema_5
    }

    while True:
        print("\n" + "=" * 65)
        print(" APLICACIÓN DE ARREGLOS MULTIDIMENSIONALES EN INGENIERÍA")
        print("=" * 65)
        print("1. Análisis de fuerzas en una estructura (3x3)")
        print("2. Simulación de fluido en una cuadrícula 3D (3x3x3)")
        print("3. Análisis de imágenes médicas en 3D")
        print("4. Manejo de datos en una tabla de sensores (5x5)")
        print("5. Transformación de coordenadas cartesianas")
        print("6. Salir")

        opcion = input("\nSeleccione una opción (1-6): ").strip()

        if opcion == "6":
            print("\nPrograma finalizado.")
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            print("\nOpción inválida. Ingrese un número del 1 al 6.")


if __name__ == "__main__":
    menu_principal()
