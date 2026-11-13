Tarea: Aplicación de Arreglos Multidimensionales en Ingeniería
Este repositorio contiene una solución modular en Python para cinco problemas de ingeniería que utilizan arreglos bidimensionales y tridimensionales con NumPy. Las visualizaciones se realizan con Matplotlib.
Requisitos
- Python 3 instalado.
- NumPy.
- Matplotlib.
Instalación de dependencias:
python -m pip install numpy matplotlib
En Windows también puede utilizarse:
py -m pip install numpy matplotlib
Estructura del proyecto
.
├── app.py
└── README.md
Ejecución
Desde la terminal, ubíquese en la carpeta del proyecto y ejecute:
python app.py
En Windows también puede ejecutar:
py app.py
Aparecerá un menú que permite seleccionar cualquiera de los cinco problemas o salir del programa.
Descripción de las soluciones
1. Análisis de fuerzas en una estructura (matriz 3x3)
Se utiliza una matriz bidimensional de 3x3 para representar cargas verticales en una malla de nodos. Para poder calcular reacciones mediante estática se declara un modelo simplificado: las cargas de cada columna se agrupan en una posición de una viga simplemente apoyada, con apoyos en x = 0 m y x = 2 m.

Se calculan la carga total y el momento de las cargas respecto al apoyo A. Después se obtienen las reacciones verticales mediante:
- Equilibrio de fuerzas verticales: RA + RB = carga_total.
- Equilibrio de momentos respecto a A: RB * L = momento_de_las_cargas.
También se imprimen comprobaciones de ambas ecuaciones de equilibrio.

Eficiencia: las sumas por columnas se calculan con np.sum y el momento se obtiene mediante operaciones vectorizadas. El recorrido y almacenamiento de la matriz son proporcionales al número de nodos, por lo que el costo es O(N²) para una matriz N x N.

Alcance del modelo: es un modelo equivalente de viga simplemente apoyada, no un análisis estructural completo de una losa bidimensional.
2. Simulación de fluido en una cuadrícula 3D (3x3x3)
Se utilizan tres arreglos tridimensionales independientes de dimensiones 3x3x3 para representar presión, temperatura y rapidez del fluido.

La presión se actualiza mediante una ecuación de onda discreta simplificada que utiliza el laplaciano calculado con los seis vecinos ortogonales. La temperatura y la rapidez se actualizan mediante una regla difusiva basada en el promedio de esos seis vecinos.

Se actualizan las 27 celdas. Para las fronteras se utiliza padding con modo edge, que replica los valores del borde y permite definir los vecinos sin salir del volumen.

Eficiencia: los vecinos se obtienen mediante cortes de arreglos de NumPy y operaciones vectorizadas, sin recorrer las celdas individualmente con bucles Python. Para un volumen D x H x W, el trabajo por paso es O(D*H*W).

Alcance del modelo: es una simulación numérica didáctica simplificada. No sustituye un modelo completo de dinámica de fluidos computacional (CFD).
3. Análisis de imágenes médicas en 3D
Se genera un volumen tridimensional sintético que representa capas de una imagen médica. Se añade ruido aleatorio y se aplica un filtro de promedio 3x3x3 a cada vóxel.

Se utiliza np.pad con mode="edge" para replicar los valores de los bordes y procesar también los vóxeles de las fronteras. El programa muestra una comparación gráfica de una capa con ruido y la misma capa después del suavizado.

Eficiencia: cada vóxel requiere calcular el promedio de una vecindad de tamaño fijo de 27 valores. Por tanto, el costo es O(D*H*W) para un volumen de dimensiones D x H x W, porque el tamaño del filtro no cambia.

Alcance del modelo: los datos son sintéticos; no corresponden a estudios médicos reales ni deben utilizarse para diagnóstico.
4. Manejo de datos en una tabla de sensores (5x5)
Se utiliza una matriz 5x5: las filas representan cinco momentos de tiempo y las columnas representan cinco sensores.

Se calculan las medias y desviaciones estándar muestrales por columnas (axis=0) y por filas (axis=1). Para la desviación estándar se utiliza ddof=1.

El programa presenta:
- La matriz de temperaturas.
- Las estadísticas por sensor.
- Las estadísticas por momento.
- Un mapa de calor de las lecturas.
- Un gráfico de barras de las medias por sensor con barras de error.
Eficiencia: NumPy ejecuta las reducciones por ejes en rutinas optimizadas. El procesamiento de una matriz N x M requiere O(N*M) operaciones.
5. Transformación de coordenadas en un sistema cartesiano
Se representa un polígono mediante una matriz bidimensional de puntos (x, y). Se aplica una rotación de 90 grados en sentido antihorario y luego una traslación mediante el vector [2, 4].

La operación se realiza con producto matricial de NumPy y suma vectorizada. Se muestran los puntos originales y transformados en una misma gráfica.

Eficiencia: la transformación se aplica al conjunto completo de puntos mediante álgebra matricial, con costo O(P) para P puntos en dos dimensiones.

Nota matemática: la rotación es una transformación lineal; al añadir una traslación, la transformación compuesta es afín.
Capturas de pantalla
Después de ejecutar el programa, agregue aquí capturas reales de:
1. Opción 1: matriz de cargas, reacciones y comprobaciones de equilibrio.
2. Opción 2: valores iniciales y actualizados de presión, temperatura y rapidez.
3. Opción 3: comparación gráfica de la capa con ruido y suavizada.
4. Opción 4: mapa de calor y gráfico de barras de los sensores.
5. Opción 5: gráfico de puntos originales y transformados.
Las capturas deben corresponder a la versión final de app.py incluida en este repositorio.
Organización del código
El archivo app.py contiene una función independiente para cada problema, funciones auxiliares cuando son necesarias y un menú principal. Cada función incluye un docstring que explica su propósito, los arreglos utilizados y las operaciones principales.
