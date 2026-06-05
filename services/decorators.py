import functools
import inspect

def validar_medidas_abertura(func):
    """
    Decorador para validar que el ancho y el alto sean valores numéricos y positivos.
    Se aplica sobre funciones que reciben (id_cliente, ancho, alto, ...).
    """
    @functools.wraps(func)
    def wrapper(id_cliente, ancho, alto, *args, **kwargs):
        try:
            ancho_f = float(ancho)
            alto_f = float(alto)
        except (ValueError, TypeError):
            raise ValueError("El ancho y el alto deben ser valores numéricos válidos (ej: 1.50).")
        
        if ancho_f <= 0 or alto_f <= 0:
            raise ValueError("Las medidas de la abertura (ancho y alto) deben ser mayores a cero.")
            
        # Ejecutar la función original pasando los valores ya convertidos a float
        return func(id_cliente, ancho_f, alto_f, *args, **kwargs)
    return wrapper

def validar_nombre_cliente(func):
    """
    Decorador para validar que el nombre del cliente no esté vacío.
    Detecta automáticamente el parámetro 'nombre' inspeccionando la firma de la función.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Enlazamos los argumentos recibidos con la firma de la función
        sig = inspect.signature(func)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        
        nombre = bound.arguments.get('nombre')
                
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre del cliente es obligatorio y no puede estar vacío.")
            
        return func(*args, **kwargs)
    return wrapper
