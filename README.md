
## Estructura del Proyect

```
.
├── requirements.txt
└── src
    ├── geometria.cpp
    └── main.py
```

* `requirements.txt`: Lista de dependencias de Python.
* `src/geometria.cpp`: Código fuente de C++ para las clases`Spaceship` y`Meteor`.
* `src/main.py`: Script principal que utiliza PyOpenGL y Pygame.

## Dependencias

* Python 3.x
* g++ (compilador de C++)
* PyOpenGL
* Pygame
* pybind11

## Cómo Instalar Dependencias

### Arch Linux

1. Instalar Python 3.x:

```bash
sudo pacman -S python
```

2. Instalar g++:

```bash
sudo pacman -S gcc
```

3. Instalar pybind11:

```bash
sudo pacman -S pybind11
```

4. Instalar dependencias de Python:

```bash
pip install -r requirements.txt
```

5. Instalar Tk
Si no has instalado Tk, instálalo ejecutando el siguiente comando:

```bash
sudo pacman -S tk
```

## Cómo Ejecutar el Proyecto

1. Compilar el módulo `geometria`:

```bash
 cd src
 g++ -O3 -Wall -shared -std=c++11 -fPIC `python3 -m pybind11 --includes` geometria.cpp -o geometria`python3-config --extension-suffix`
```

2. Ejecutar el script principal:

```bash
 python main.py
```
