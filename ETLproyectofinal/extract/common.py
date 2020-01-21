import yaml

__config = None  # Es importante porque estamos leyendo a disco


def config():
    global __config  # Hace la variable global
    if not __config:  # Si no fue leida antes la lee
        with open('config.yaml', mode='r') as f:
            __config = yaml.safe_load(f)  # Carga la informacion en el archivo yaml en config

    return __config  # Devuelve los datos del archivo yaml
