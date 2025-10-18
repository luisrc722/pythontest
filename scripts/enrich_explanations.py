#!/usr/bin/env python3
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QPATH = ROOT / "src/data/questions.json"


AREA_DOCS = {
    "fundamentals/data_structures": "https://docs.python.org/3/tutorial/datastructures.html",
    "fundamentals/operators": "https://docs.python.org/3/reference/expressions.html",
    "fundamentals/variables": "https://docs.python.org/3/tutorial/introduction.html",
    "control_flow/conditionals": "https://docs.python.org/3/tutorial/controlflow.html#if-statements",
    "control_flow/loops": "https://docs.python.org/3/tutorial/controlflow.html#for-statements",
    "control_flow/comprehensions": "https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions",
    "functions/definitions": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
    "functions/decorators": "https://docs.python.org/3/library/functools.html#functools.wraps",
    "functions/generators": "https://docs.python.org/3/reference/expressions.html#generator-expressions",
    "functions/async": "https://docs.python.org/3/library/asyncio-task.html",
    "oop/classes": "https://docs.python.org/3/tutorial/classes.html",
    "oop/inheritance": "https://docs.python.org/3/tutorial/classes.html#inheritance",
    "oop/magic_methods": "https://docs.python.org/3/reference/datamodel.html",
    "data_science/numpy": "https://numpy.org/doc/stable/user/whatisnumpy.html",
    "data_science/pandas": "https://pandas.pydata.org/docs/",
    "data_science/visualization": "https://matplotlib.org/stable/tutorials/introductory/pyplot.html",
    "web/flask": "https://flask.palletsprojects.com/",
    "web/django": "https://docs.djangoproject.com/",
    "web/fastapi": "https://fastapi.tiangolo.com/",
    "courses/cuda_python_course": "https://developer.nvidia.com/cuda-zone",
    "other/modules_packages": "https://docs.python.org/3/tutorial/modules.html",
    "other/exceptions": "https://docs.python.org/3/tutorial/errors.html",
    "other/file_io": "https://docs.python.org/3/tutorial/inputoutput.html",
    "other/testing": "https://docs.pytest.org/en/stable/",
    "other/async_programming": "https://docs.python.org/3/library/asyncio.html",
    "other/best_practices": "https://peps.python.org/pep-0008/",
}


def specific_reason(q: dict) -> str | None:
    t = q.get("text", "").lower()
    c = (q.get("correct") or "").lower()
    area = q.get("area", "")

    # Fundamentals / Data Structures
    if area == "fundamentals/data_structures":
        if c == "list":
            return "list es mutable; tuple/str/int son inmutables"
        if c == "append":
            return "append agrega al final; insert posiciona; add/push no existen en listas"
        if c == "set":
            return "set almacena elementos únicos sin orden"
        if "dict.keys" in t or "keys" in t and "dict" in t:
            return "dict.keys() devuelve una vista dinámica de claves (no una lista)"
        if c == "[0,1,2]":
            return "range(n) genera 0..n-1; list materializa la secuencia"
        if "a, b = b, a" in t:
            return "El desempaquetado múltiple intercambia referencias en una sola expresión"

    # Fundamentals / Operators
    if area == "fundamentals/operators":
        if c == "3":
            return "// realiza división entera (descarta decimales)"
        if c == "1":
            return "% devuelve el resto de la división"
        if c == "*":
            return "La multiplicación tiene mayor precedencia que +, == y and"
        if c == "true":
            if "not (true and false)" in t:
                return "True and False es False; not invierte a True"
            if "1 < 2 < 3" in t:
                return "Las comparaciones encadenadas evalúan de izquierda a derecha"
        if "'is'" in t or c == "compara identidad de objeto":
            return "is compara identidad (mismo objeto), == compara igualdad de valor"

    # Fundamentals / Variables
    if area == "fundamentals/variables":
        if c == "var_2":
            return "Los nombres deben iniciar con letra/_ y usar snake_case (PEP8)"
        if "referencia" in c or c == "crea una referencia a y":
            return "La asignación ata el nombre al mismo objeto (no copia)"
        if c == "global":
            return "global declara que el nombre se refiere al ámbito del módulo"
        if c == "none":
            return "Se usa None como valor nulo; referenciar sin asignar produce NameError"
        if c == "snake_case":
            return "PEP8 recomienda snake_case para nombres de variables y funciones"
        if c == "dinámicos" or "dinám" in c:
            return "Python es de tipado dinámico: el tipo pertenece al objeto, no al nombre"

    # Control Flow / Conditionals
    if area == "control_flow/conditionals":
        if c == "false" and "lista vacía" in t:
            return "Las secuencias vacías son falsy (bool([]) == False)"
        if "ternario" in t or "if-else" in t:
            if c == "ternario":
                return "x if cond else y es la expresión condicional (ternaria) de Python"
        if c == "else" and "if/elif" in t:
            return "Una cadena if/elif se cierra con else como caso por defecto"
        if c == "b" and "a if false else b" in t:
            return "condición False elige el operando del else"
        if "if > elif > else" in c:
            return "El flujo evalúa if, luego elif, y finalmente else si ninguno coincide"
        if c == "and":
            return "and combina condiciones y cortocircuita al primer False"

    # Control Flow / Loops
    if area == "control_flow/loops":
        if "continue" in t:
            return "continue omite el resto del bloque y salta a la siguiente iteración"
        if "break" in t and c == "termina el bucle":
            return "break sale inmediatamente del bucle actual"
        if "enumerate" in t:
            return "enumerate produce pares (indice, valor), iniciando en 0 por defecto"
        if "for" in t and "else" in t:
            return "El else del for se ejecuta si el bucle no terminó por break"
        if "while false" in t:
            return "La condición False impide entrar al cuerpo del while"

    # Control Flow / Comprehensions
    if area == "control_flow/comprehensions":
        if "x*x for x in range(3)" in t:
            return "range(3) da 0..2; el cuadrado produce [0,1,4]"
        if "{x:x*x" in t and c.startswith("{1:1"):
            return "Dict comprehension genera pares clave:valor por cada elemento"
        if "if x%2==0" in t:
            return "El filtro 'if' mantiene solo pares"
        if "{x for x in" in t:
            return "Set comprehension elimina duplicados al construir el conjunto"
        if c == "legibilidad y concisión":
            return "Comprehensions condensan mapeo/filtrado en una sola expresión legible"
        if "(x for x in" in t:
            return "Una generator expression crea un generador lazily evaluated"

    # Functions
    if area == "functions/definitions":
        if c == "def":
            return "Las funciones se definen con la palabra clave 'def'"
        if "mutables" in t:
            return "Los valores por defecto se crean una vez; si son mutables, comparten estado entre llamadas"
        if c == "none" and "sin return" in t:
            return "Una función sin return explícito devuelve None"
        if "*args" in t and "**kwargs" in t:
            return "*args agrupa posicionales variables; **kwargs agrupa de palabra clave variables"
        if "->" in t:
            return "'-> T' es una anotación de tipo del valor de retorno"
        if "nonlocal" in t:
            return "nonlocal vincula el nombre al scope exterior inmediato (no global)"

    if area == "functions/decorators":
        if c.startswith("una función que envuelve"):
            return "Un decorador toma una función y devuelve otra, añadiendo comportamiento"
        if "@" in t and "decorator" in t:
            return "La sintaxis @decorator aplica decorator(func) al definirla"
        if "wraps" in t:
            return "functools.wraps preserva __name__/__doc__/__module__ de la función envuelta"
        if "@staticmethod" in t:
            return "@staticmethod define un método sin self ni cls"
        if "@property" in t:
            return "@property expone un método como atributo de solo lectura"
        if "múltiples decoradores" in t or "orden" in t:
            return "Se aplican de abajo hacia arriba (el más cercano primero)"

    if area == "functions/generators":
        if c == "yield":
            return "yield convierte una función en generador y produce valores sucesivos"
        if "next(" in t:
            return "next(gen) obtiene el siguiente valor producido por yield"
        if "yield from" in t:
            return "yield from delega a un subgenerador simplificando el código"
        if "(x for x" in t:
            return "(x for x in ...) es un generador (tipo generator)"
        if "no tiene 'yield'" in t:
            return "Sin yield no es generador: se comporta como una función normal"
        if "fin de un generador" in t and c == "stopiteration":
            return "Al agotar un generador se lanza StopIteration"

    if area == "functions/async":
        if c == "async def":
            return "Las funciones asíncronas se declaran con 'async def'"
        if c.startswith("suspende") or "await" in t:
            return "await cede el control hasta que el awaitable complete"
        if c == "asyncio":
            return "La librería estándar para async/await es asyncio"
        if c == "coroutine":
            return "Llamar a una función async devuelve una coroutine (no ejecuta)"
        if "asyncio.run" in t:
            return "asyncio.run() crea el loop, ejecuta la coroutine y cierra el loop"
        if "gather" in t:
            return "asyncio.gather ejecuta awaitables concurrentemente y agrega resultados"

    # OOP
    if area == "oop/classes":
        if c.startswith("class "):
            return "class Nombre: define una clase"
        if c == "self":
            return "Por convención, 'self' es el primer parámetro de métodos de instancia"
        if "atributo de clase" in t or "instancia" in t:
            return "Los atributos de clase se comparten; los de instancia son por objeto"
        if c == "__init__":
            return "__init__ inicializa la instancia tras __new__"
        if c == "crea instancia":
            return "__new__ crea la instancia; __init__ la inicializa"
        if c == "@classmethod":
            return "@classmethod recibe 'cls' y opera a nivel de clase"

    if area == "oop/inheritance":
        if c.startswith("class "):
            return "class B(A): declara herencia de A"
        if "super" in t:
            return "super() accede a métodos/atributos de la clase base en el MRO"
        if c.startswith("orden de resolución"):
            return "MRO define el orden en que se buscan atributos/métodos en herencia múltiple"
        if "sobreescribir" in t:
            return "Redefinir un método en el hijo reemplaza el del padre"
        if "abc.abc" in t or "abstractas" in t:
            return "abc.ABC permite definir clases abstractas y métodos abstractmethod"
        if "múltiples padres" in t or "multiple inheritance" in t:
            return "Python soporta herencia múltiple; el MRO resuelve conflictos"

    if area == "oop/magic_methods":
        if c == "__str__":
            return "__str__ devuelve una representación amigable para usuarios"
        if c == "__repr__":
            return "__repr__ devuelve una representación precisa para desarrolladores"
        if c == "__len__":
            return "len(obj) invoca obj.__len__()"
        if c == "__eq__":
            return "'==' invoca __eq__ para comparar igualdad de valor"
        if c == "__iter__":
            return "__iter__ devuelve un iterador para recorrer el objeto"
        if c == "instancia invocable" or "__call__" in t:
            return "Definir __call__ hace que la instancia sea invocable como función"

    # Data science
    if area == "data_science/numpy":
        if "arange(3)" in t:
            return "np.arange(3) genera [0,1,2]; inclusivo en 0 y exclusivo en 3"
        if c == "shape":
            return "El atributo shape retorna la forma (dimensiones) del array"
        if "broadcast" in t:
            return "Broadcasting aplica reglas para operar arrays de formas compatibles"
        if c == "float64":
            return "np.zeros usa float64 por defecto salvo que se indique dtype"
        if "ndim" in t and c == "1":
            return "Un array 1D tiene ndim == 1"
        if "a[a>0]" in t:
            return "La indexación booleana selecciona elementos donde la condición es True"
        if "seed" in t:
            return "np.random.seed fija la semilla para reproducibilidad"
        if "vectoriz" in t:
            return "Las operaciones NumPy están vectorizadas: se aplican elemento a elemento eficientemente"

    if area == "data_science/pandas":
        if c == "series":
            return "Series representa una secuencia etiquetada (columna)"
        if "read_csv" in t:
            return "pd.read_csv carga datos desde un CSV a un DataFrame"
        if "loc" in t and "iloc" in t:
            return "loc indexa por etiquetas; iloc por posición"
        if "head(" in t:
            return "head(n) devuelve las primeras n filas"
        if "dropna" in t:
            return "dropna elimina filas/columnas con valores nulos"
        if "merge" in t:
            return "merge une DataFrames por claves comunes (join)"

    if area == "data_science/visualization":
        if c == "matplotlib":
            return "Matplotlib es la base; Seaborn y otras se apoyan en ella"
        if "plt.show" in t:
            return "plt.show() muestra la figura en pantalla"
        if "figsize" in t:
            return "figsize controla el tamaño de la figura en pulgadas"
        if "seaborn" in t:
            return "Seaborn añade estilos y utilidades estadísticas sobre Matplotlib"
        if "ax.plot" in t:
            return "ax.plot crea una gráfica de líneas"
        if "heatmap" in t:
            return "Un heatmap utiliza colores para representar intensidades en una matriz"

    # Web
    if area == "web/flask":
        if "@app.route" in t:
            return "@app.route asocia una ruta URL a una función de vista"
        if c == "flask run":
            return "El comando 'flask run' inicia el servidor de desarrollo"
        if c == "jinja2":
            return "Flask usa Jinja2 como motor de plantillas por defecto"
        if c == "request.args":
            return "request.args accede a parámetros de consulta (query string)"
        if "debug" in t:
            return "FLASK_DEBUG=1 activa recarga y depuración en desarrollo"
        if c.startswith("devuelve response json"):
            return "jsonify serializa a JSON y devuelve una Response con mimetype application/json"

    if area == "web/django":
        if "startproject" in t:
            return "django-admin startproject crea la estructura base de un proyecto"
        if "startapp" in t:
            return "django-admin startapp crea una nueva aplicación dentro del proyecto"
        if c == "models.py":
            return "models.py define los modelos (tablas) del ORM"
        if "migrate" in t and c.startswith("python manage.py migrate"):
            return "migrate aplica migraciones pendientes a la base de datos"
        if c == "settings.py":
            return "settings.py configura la aplicación, incluidas INSTALLED_APPS"
        if c.startswith("mapea objetos a bd"):
            return "El ORM traduce objetos Python a operaciones SQL y viceversa"

    if area == "web/fastapi":
        if c == "@app.get":
            return "@app.get define una ruta HTTP GET"
        if c == "pydantic":
            return "FastAPI usa Pydantic para validación y serialización de datos"
        if "uvicorn" in t:
            return "Uvicorn ejecuta aplicaciones ASGI como FastAPI"
        if c == "/docs":
            return "FastAPI expone documentación interactiva Swagger UI en /docs"
        if c.startswith("agrupador de rutas"):
            return "APIRouter permite modularizar rutas y middlewares"
        if c == "coroutine":
            return "Una función async devuelve una coroutine si no se await-ea"

    # Courses / CUDA
    if area == "courses/cuda_python_course":
        if "plataforma" in q.get("correct", "").lower():
            return "CUDA es una plataforma y API para cómputo paralelo en GPU"
        if c == "cupy":
            return "CuPy replica API de NumPy pero ejecuta en GPU"
        if "cuda.jit" in t:
            return "Numba @cuda.jit compila funciones Python para ejecutarse en la GPU"
        if c.startswith("función que ejecuta"):
            return "Un kernel es la función que corre en la GPU lanzada por bloques/hilos"
        if "host" in t and "device" in t:
            return "Transferir datos CPU↔GPU es costoso; minimizar copias mejora rendimiento"
        if "coalescencia" in t:
            return "El acceso coalescente optimiza el ancho de banda de memoria global en GPU"

    # Other
    if area == "other/modules_packages":
        if c == "__init__.py":
            return "__init__.py marca un directorio como paquete importable"
        if "from . import" in t:
            return "El punto indica importación relativa dentro del mismo paquete"
        if c == "sys.path":
            return "sys.path lista las rutas donde Python busca módulos"
        if c == "__main__.py":
            return "__main__.py permite ejecutar el paquete con 'python -m paquete'"
        if c == "setuptools":
            return "setuptools y wheel construyen paquetes distribuibles"
        if c.startswith("define exports"):
            return "__all__ controla los nombres exportados por from paquete import *"

    if area == "other/exceptions":
        if c == "except":
            return "try/except captura excepciones manejables"
        if c == "finally":
            return "finally se ejecuta siempre, útil para liberar recursos"
        if "raise" in t:
            return "raise Exception() lanza una excepción explícitamente"
        if "except exception as e" in t or "derivada" in t:
            return "Captura cualquier excepción que herede de Exception"
        if "class e(exception)" in t:
            return "Las excepciones personalizadas heredan de Exception"
        if c == "keyerror":
            return "Acceder a una clave inexistente en dict lanza KeyError"

    if area == "other/file_io":
        if "open('f','r')" in t:
            return "'r' abre en modo lectura de texto"
        if c == "with":
            return "with garantiza cerrar el archivo al salir del bloque"
        if c == "'a'":
            return "'a' abre para agregar al final sin truncar"
        if c == "lee todas las líneas":
            return "readlines() devuelve una lista con todas las líneas"
        if "write(" in t:
            return "f.write escribe texto en el archivo"
        if c == "filenotfounderror":
            return "Abrir en modo 'r' un archivo inexistente lanza FileNotFoundError"

    if area == "other/testing":
        if c == "pytest":
            return "pytest es el framework más usado en Python para testing"
        if c == "assert":
            return "pytest usa assert para aserciones simples y expresivas"
        if c == "un setup reusable":
            return "Las fixtures proveen datos/recursos reusables para tests"
        if "-k" in t:
            return "-k permite seleccionar tests por subcadena/expresión"
        if "parametrize" in t:
            return "@pytest.mark.parametrize ejecuta el test con múltiples entradas"
        if c == "pytest.ini":
            return "pytest.ini centraliza configuración por proyecto"

    if area == "other/async_programming":
        if c.startswith("planificador"):
            return "El event loop coordina la ejecución de tareas async"
        if c.startswith("cede el control"):
            return "await cede el control al loop hasta completar"
        if c.startswith("programar coroutine"):
            return "asyncio.create_task agenda la coroutine para ejecución concurrente"
        if "sleep(0)" in t:
            return "asyncio.sleep(0) cede inmediatamente al event loop"
        if "__await__" in t or "awaitable" in t:
            return "Un awaitable implementa el protocolo __await__ (Future/Task/Coroutine)"
        if "gather" in t:
            return "asyncio.gather corre awaitables en paralelo cooperativo"

    if area == "other/best_practices":
        if c == "black":
            return "black formatea código automáticamente siguiendo PEP8"
        if c == "mypy":
            return "mypy verifica tipos estáticos a partir de anotaciones PEP484"
        if c == "pyproject.toml":
            return "pyproject.toml centraliza config de build/deps en proyectos modernos"
        if c == "snake_case":
            return "PEP8 recomienda snake_case para funciones y variables"
        if c.startswith("confianza en cambios"):
            return "Las pruebas automatizadas previenen regresiones al refactorizar"
        if "docstring" in t:
            return "Los estilos Google/NumPy facilitan documentación consistente"

    return None


def build_explanation(q: dict) -> str:
    area = q.get("area", "")
    doc = AREA_DOCS.get(area, "")
    reason = specific_reason(q)
    base = reason or f"La opción '{q.get('correct')}' es la correcta para este concepto."
    if doc:
        return f"{base}. Ver: {doc}"
    return base


def main() -> int:
    data = json.loads(QPATH.read_text(encoding="utf-8"))
    changed = 0
    for q in data:
        if not q.get("explanation"):
            q["explanation"] = build_explanation(q)
            changed += 1
    QPATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Explicaciones añadidas/actualizadas: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

