import psycopg2

def conectar():
    """
    Establece la conexión con la base de datos de Supabase.
    """
    return psycopg2.connect(
        host="aws-1-us-west-2.pooler.supabase.com",
        database="postgres",
        user="postgres.ervrzydvnspoyqmjzwok",
        password="Wolf@1109788",
        port="5432"
    )
