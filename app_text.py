import os
from google import genai
from dotenv import load_dotenv

# =========================================================
# EJERCICIO 1: CONEXIÓN Y PETICIÓN BÁSICA
# =========================================================
# Objetivo: Inicializar cliente Gemini y consultar sobre
# "Inferencia en IA" en menos de 50 palabras

# 1. CARGAR VARIABLES DE ENTORNO
# Cargamos la clave API desde el archivo .env para mantenerla segura
load_dotenv()
clave_api = os.getenv("GEMINI_API_KEY")

# Validar que la clave API está disponible
if not clave_api:
    print("❌ Error: La clave API de Gemini no está configurada en las variables de entorno")
    exit(1)

# 2. INICIALIZAR EL CLIENTE DE GEMINI
# Creamos una instancia del cliente que se conectará a los servicios de Google Gemini
# Esta conexión gestiona la comunicación con los modelos
try:
    client = genai.Client(api_key=clave_api)
    print("✅ Cliente de Gemini inicializado correctamente")
except Exception as e:
    print(f"❌ Error al inicializar el cliente: {e}")
    exit(1)

# 3. PREPARAR LA SOLICITUD (PROMPT)
# Creamos un prompt que pide al modelo explicar "Inferencia en IA" en menos de 50 palabras
prompt = """Explica qué es la "Inferencia en IA" en menos de 50 palabras. 
Sé conciso y claro en tu explicación."""

print("\n📝 Enviando solicitud al modelo Gemini...")
print(f"Prompt: {prompt}\n")

# 4. REALIZAR LA CONSULTA AL MODELO
# Enviamos la solicitud al modelo gemini-2.0-flash (última versión disponible)
# y obtenemos la respuesta
response = None
try:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    print("✅ Solicitud enviada y respuesta recibida correctamente\n")
except Exception as e:
    print(f"❌ Error al conectar con Gemini: {e}")
    exit(1)

# 5. PROCESAR Y MOSTRAR LA RESPUESTA
# Verificamos si recibimos una respuesta válida del modelo
if response and response.text:
    print("=" * 60)
    print("🤖 RESPUESTA DEL MODELO GEMINI:")
    print("=" * 60)
    print(response.text)
    print("=" * 60)
    
    # Contar palabras para verificar que cumple con el requisito
    palabras = response.text.strip().split()
    cantidad_palabras = len(palabras)
    print(f"\n📊 Cantidad de palabras: {cantidad_palabras}")
    
    if cantidad_palabras <= 50:
        print("✅ ¡La respuesta cumple con el límite de 50 palabras!")
    else:
        print(f"⚠️  La respuesta excede el límite: {cantidad_palabras - 50} palabras adicionales")
else:
    print("❌ No se pudo obtener respuesta válida del modelo")