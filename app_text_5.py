import os
from google import genai
from dotenv import load_dotenv

# =========================================================
# EJERCICIO 2: PROCESADOR DE TEXTOS INTELIGENTE (30%)
# =========================================================
# Objetivo: Crear una función que procese textos con dos tareas:
# 1. "resumir": devuelve un resumen ejecutivo
# 2. "profesionalizar": edita el texto para que sea formal y técnico
# Requisito: Usar system_instruction como "Editor Editorial de prestigio"

# 1. CARGAR CONFIGURACIÓN
# Cargamos las variables de entorno para obtener la clave API
load_dotenv()
clave_api = os.getenv("GEMINI_API_KEY")

# Validar disponibilidad de la clave API
if not clave_api:
    print("❌ Error: La clave API no está configurada")
    exit(1)

# 2. INICIALIZAR CLIENTE DE GEMINI
# Creamos la instancia del cliente que usaremos en toda la función
try:
    client = genai.Client(api_key=clave_api)
    print("✅ Cliente de Gemini inicializado\n")
except Exception as e:
    print(f"❌ Error al inicializar cliente: {e}")
    exit(1)


# 3. FUNCIÓN PRINCIPAL: PROCESAR_ARTICULO
def procesar_articulo(texto, tarea):
    """
    Función que procesa un texto según la tarea especificada.
    
    Parámetros:
        texto (str): El texto a procesar
        tarea (str): "resumir" o "profesionalizar"
    
    Retorna:
        str: El texto procesado según la tarea
    """
    
    # Definir la system_instruction que define el rol de la IA
    # Esta instrucción de sistema establece el contexto para todas las respuestas
    system_instruction = (
        "Eres un Editor Editorial de prestigio con 20 años de experiencia. "
        "Tu rol es garantizar que todos los textos sean precisos, claros y de calidad profesional. "
        "Debes mantener la esencia del contenido mientras mejoras su presentación. "
        "Eres experto en redacción técnica, académica y profesional."
    )
    
    # Validar que el parámetro tarea sea válido
    if tarea not in ["resumir", "profesionalizar"]:
        print(f"❌ Tarea no reconocida: {tarea}")
        print("   Usa 'resumir' o 'profesionalizar'")
        return None
    
    # CREAR EL PROMPT SEGÚN LA TAREA SELECCIONADA
    if tarea == "resumir":
        # Tarea 1: RESUMIR - Crear un resumen ejecutivo del texto
        prompt = f"""Por favor, crea un resumen ejecutivo del siguiente texto.
El resumen debe:
- Capturar las ideas principales
- Ser conciso (máximo 200 palabras)
- Mantener la esencia del contenido original
- Usar lenguaje profesional y directo

TEXTO A RESUMIR:
{texto}

Proporciona el resumen ejecutivo:"""
        
    else:  # tarea == "profesionalizar"
        # Tarea 2: PROFESIONALIZAR - Editar para que sea formal y técnico
        prompt = f"""Por favor, profesionaliza y formaliza el siguiente texto.
Debes:
- Convertir el lenguaje a un tono formal y técnico
- Reemplazar expresiones coloquiales por terminología precisa
- Mejorar la estructura y fluidez del texto
- Mantener el mensaje original pero con mayor rigor
- Usar vocabulario profesional y académico

TEXTO A PROFESIONALIZAR:
{texto}

Proporciona el texto profesionalizado:"""
    
    # 4. REALIZAR LA CONSULTA AL MODELO CON SYSTEM_INSTRUCTION
    try:
        # Enviamos la solicitud incluyendo la system_instruction en el contenido
        # Combinamos la instrucción del sistema con el prompt en un solo contenido
        contenido_completo = f"{system_instruction}\n\n{prompt}"
        
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=contenido_completo
        )
        
        # Verificar que la respuesta es válida
        if response and response.text:
            return response.text
        else:
            print("❌ No se recibió respuesta válida del modelo")
            return None
            
    except Exception as e:
        print(f"❌ Error al procesar el texto: {e}")
        return None


# 5. EJEMPLO DE USO Y PRUEBAS
if __name__ == "__main__":
    # Texto de ejemplo para las pruebas
    texto_ejemplo = """
    La inteligencia artificial está revolucionando la forma en que trabajan las empresas hoy en día.
    Los algoritmos de machine learning son muy útiles porque pueden analizar datos gigantes y encontrar
    patrones que los humanos no ven. Es increíble cómo funciona esto. Muchas compañías grandes como
    Google, Amazon y Microsoft están invirtiendo un montón de dinero en IA. Esto está cambiando todo
    en la tecnología y los negocios. En el futuro, la IA va a ser aún más importante para toda la sociedad.
    """
    
    print("=" * 70)
    print("PRUEBA 1: RESUMIR EL ARTÍCULO")
    print("=" * 70)
    print(f"\n📝 Texto original:\n{texto_ejemplo}\n")
    
    resumen = procesar_articulo(texto_ejemplo, "resumir")
    if resumen:
        print("📋 RESUMEN EJECUTIVO:")
        print("-" * 70)
        print(resumen)
        print()
    
    print("\n" + "=" * 70)
    print("PRUEBA 2: PROFESIONALIZAR EL ARTÍCULO")
    print("=" * 70)
    print(f"\n📝 Texto original:\n{texto_ejemplo}\n")
    
    profesionalizado = procesar_articulo(texto_ejemplo, "profesionalizar")
    if profesionalizado:
        print("📘 TEXTO PROFESIONALIZADO:")
        print("-" * 70)
        print(profesionalizado)
        print()
    
  