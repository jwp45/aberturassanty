from services.database import conectar
import hashlib

def validar_usuario(email, password):
    """
    Verifica si el email y la contraseña existen en la base de datos.
    Compara el hash SHA-256 de la contraseña ingresada con el almacenado.
    """
    # Generamos el hash de la contraseña para comparar de forma segura
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    conn = conectar()
    try:
        with conn.cursor() as cur:
            # Buscamos el usuario por email y hash de contraseña
            query = "SELECT id FROM usuarios WHERE email = %s AND password_hash = %s"
            cur.execute(query, (email, password_hash))
            usuario = cur.fetchone()
            
            # Si devuelve un resultado, las credenciales son válidas
            return usuario is not None
    except Exception as e:
        print(f"Error en la validación de usuario: {e}")
        return False
    finally:
        conn.close()
