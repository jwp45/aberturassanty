import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
from models.Presupuesto import Presupuesto
from services.config_service import cargar_configuracion

def exportar_presupuesto_a_txt_local(presupuesto: Presupuesto):
    """
    Guarda el presupuesto como un archivo de texto plano (.txt) estructurado
    en una carpeta local del proyecto ("presupuestos_guardados/") y lo abre automáticamente
    con el editor de textos nativo del sistema para facilitar la impresión directa (Ctrl+P).
    No depende de navegadores ni conexiones a internet (100% offline).
    """
    # 1. Definir y crear la carpeta local en el directorio del proyecto
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(BASE_DIR, "presupuestos_guardados")
    os.makedirs(output_dir, exist_ok=True)
    
    # 2. Generar el nombre de archivo basado en el ID del presupuesto
    filename = f"presupuesto_{presupuesto.id_presupuesto}.txt"
    filepath = os.path.join(output_dir, filename)
    
    # 3. Obtener el comprobante de texto generado por el modelo de negocio
    comprobante_texto = presupuesto.generar_comprobante()
    
    # 4. Escribir el archivo en codificación UTF-8
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(comprobante_texto)
    
    # 5. Invocar el editor de texto nativo de forma multiplataforma
    if sys.platform == "win32":
        os.startfile(filepath)
    elif sys.platform == "darwin":
        subprocess.run(["open", filepath])
    else: # Linux y otros entornos Unix (como xdg-open)
        subprocess.run(["xdg-open", filepath])
        
    return filepath

def obtener_html_email_sencillo(presupuesto: Presupuesto) -> str:
    """
    Genera una estructura de correo en HTML que es limpia, completa y funcional,
    pero lo suficientemente simple y acotada para explicar fácilmente en una defensa de examen.
    """
    res = presupuesto.procesar_presupuesto()
    m = presupuesto.MARGEN_GANANCIA
    
    # Formatear importes monetarios con separadores
    c_al = f"${res['c_al'] * m:,.2f}"
    c_vi = f"${res['c_vi'] * m:,.2f}"
    c_he = f"${res['c_he'] * m:,.2f}"
    total = f"${res['total']:,.2f}"
    
    vidrio = "DVH (Doble Vidrio Hermético)" if presupuesto.tipo_vidrio == "dvh" else "Simple 4mm"
    
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #1d4ed8; border-bottom: 2px solid #1d4ed8; padding-bottom: 8px; margin-bottom: 20px;">
            SANTY ABERTURAS - Presupuesto #{presupuesto.id_presupuesto}
        </h2>
        <p>Estimado/a cliente, le enviamos el presupuesto solicitado para su abertura a medida:</p>
        
        <table cellpadding="6" style="margin-bottom: 20px; font-size: 14px;">
            <tr><td><strong>Fecha de Emisión:</strong></td><td>{presupuesto.fecha}</td></tr>
            <tr><td><strong>Nombre Cliente:</strong></td><td>{presupuesto.cliente.nombre}</td></tr>
            <tr><td><strong>Tipo de Abertura:</strong></td><td>{presupuesto.tipo_abertura} ({presupuesto.color})</td></tr>
            <tr><td><strong>Dimensiones:</strong></td><td>{presupuesto.ancho:.2f} m (Ancho) x {presupuesto.alto:.2f} m (Alto)</td></tr>
            <tr><td><strong>Vidriado Elegido:</strong></td><td>{vidrio}</td></tr>
        </table>
        
        <h3 style="color: #1e3a8a; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Detalle de Costos</h3>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; font-size: 14px;">
            <thead>
                <tr bgcolor="#f3f4f6">
                    <th align="left">Concepto del Material (Mano de Obra Incluida)</th>
                    <th align="right">Precio Final</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Estructura de Aluminio y Perfiles</td>
                    <td align="right">{c_al}</td>
                </tr>
                <tr>
                    <td>Vidrio y Colocación</td>
                    <td align="right">{c_vi}</td>
                </tr>
                <tr>
                    <td>Kit de Accesorios, Burletes y Selladores</td>
                    <td align="right">{c_he}</td>
                </tr>
                <tr bgcolor="#eff6ff" style="font-weight: bold; color: #1d4ed8; font-size: 16px;">
                    <td>TOTAL NETO A PAGAR:</td>
                    <td align="right">{total}</td>
                </tr>
            </tbody>
        </table>
        
        <p style="margin-top: 25px; font-size: 12px; color: #666666; font-style: italic;">
            * Nota: Los precios incluyen IVA y armado. Este presupuesto tiene una validez de 15 días corridos a partir del día de su emisión.
        </p>
        <p style="font-weight: bold; color: #1d4ed8; margin-top: 20px;">¡Muchas gracias por su consulta!</p>
    </body>
    </html>
    """
    return html

def enviar_presupuesto_por_email(presupuesto: Presupuesto, destinatario: str):
    """
    Realiza una petición HTTP POST a la API de Resend para enviar el email.
    Usa la biblioteca estándar 'urllib.request' evitando dependencias externas.
    """
    config = cargar_configuracion()
    api_key = config.get("resend_api_key", "")
    from_email = config.get("resend_from_email", "Santy Aberturas <onboarding@resend.dev>")
    if not api_key or api_key == "re_coloca_aqui_tu_api_key":
        raise ValueError("Debe configurar una API Key de Resend válida en el archivo config.json")
    
    html_content = obtener_html_email_sencillo(presupuesto)
    
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    payload = {
        "from": from_email,
        "to": destinatario,
        "subject": f"Presupuesto #{presupuesto.id_presupuesto} - Santy Aberturas",
        "html": html_content
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            return res_body
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_msg)
            msg = error_json.get("message", error_msg)
        except Exception:
            msg = error_msg
        raise Exception(f"API Resend (HTTP {e.code}): {msg}")
    except Exception as e:
        raise Exception(f"No se pudo conectar con el servidor: {str(e)}")
