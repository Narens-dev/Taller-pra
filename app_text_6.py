import os
from google import genai
from dotenv import load_dotenv

# =========================================================
# EJERCICIO 3: CHAT DE SOPORTE CON HISTORIAL (50%)
# =========================================================
# Objetivo: Construir un sistema de chat para una tienda de tecnología
# con soporte few-shot learning y bucle interactivo
# - Role: Vendedor amable (via system_instruction)
# - Few-shot: Pre-cargar historial con al menos 2 ejemplos
# - Bucle: Usuario pregunta hasta escribir "finalizar"

# 1. CARGAR VARIABLES DE ENTORNO
# Cargamos la clave API desde el archivo .env de forma segura
load_dotenv()
clave_api = os.getenv("GEMINI_API_KEY")

# Validar que la clave API está disponible
if not clave_api:
    print("❌ Error: La clave API no está configurada en las variables de entorno")
    exit(1)

# 2. INICIALIZAR CLIENTE DE GEMINI
# Creamos la instancia del cliente para gestionar la comunicación
try:
    client = genai.Client(api_key=clave_api)
    print("[OK] Cliente de Gemini inicializado\n")
except Exception as e:
    print(f"[ERROR] Error al inicializar cliente: {e}")
    exit(1)

# 3. DEFINIR SYSTEM_INSTRUCTION
# Esta instrucción define el rol del asistente como vendedor amable
system_instruction = (
    "Eres un vendedor amable y experto de una tienda de tecnología llamada 'TechPro'. "
    "Tu objetivo es ayudar a los clientes encontrando los mejores productos para sus necesidades. "
    "Eres conocedor de especificaciones técnicas, precios y características de productos. "
    "Siempre eres cortés, paciente y ofreces recomendaciones personalizadas. "
    "Si el cliente pregunta sobre un producto específico, proporciona detalles técnicos precisos. "
    "Cuando sea apropiado, sugiere productos alternativos o accesorios relacionados."
)

# 4. CREAR HISTORIAL INICIAL CON EJEMPLOS (FEW-SHOT)
# Pre-cargamos el historial con al menos 2 ejemplos de interacción
# Esto enseña al modelo el patrón de cómo responder
historial = [
    # EJEMPLO 1: Pregunta sobre laptop
    {
        "role": "user",
        "parts": ["Hola, estoy buscando una laptop para programación. ¿Qué me recomiendas?"]
    },
    {
        "role": "model",
        "parts": [
            "¡Hola! Te recomiendo nuestra laptop gaming ASUS ROG Strix G16. "
            "Es perfecta para programación con:\n"
            "- Procesador Intel i9-13ª gen\n"
            "- RAM: 32GB DDR5\n"
            "- SSD: 1TB NVMe\n"
            "- GPU: RTX 4070\n"
            "- Pantalla 16\" 165Hz\n"
            "Precio: $2,499 USD\n"
            "¿Te interesa este modelo o prefieres algo más económico?"
        ]
    },
    
    # EJEMPLO 2: Pregunta sobre accesorios
    {
        "role": "user",
        "parts": ["¿Qué mouse gaming me recomiendas?"]
    },
    {
        "role": "model",
        "parts": [
            "Perfecto, para gaming te recomiendo dos opciones:\n\n"
            "1. Logitech G Pro X Superlight 2:\n"
            "   - Peso: 60g (ultra ligero)\n"
            "   - DPI: hasta 32,000\n"
            "   - Conexión: 2.4GHz inalámbrica\n"
            "   - Precio: $149 USD\n\n"
            "2. Razer DeathAdder V3:\n"
            "   - Peso: 63g\n"
            "   - DPI: hasta 30,000\n"
            "   - Conexión: USB-C inalámbrica o con cable\n"
            "   - Precio: $129 USD\n\n"
            "¿Cuál te parece mejor? ¿Te interesa alguno?"
        ]
    }
]

# 5. FUNCIÓN PRINCIPAL DEL CHAT
def chat_tienda_tecnologia():
    """
    Función que ejecuta el bucle de chat interactivo.
    Permite al usuario hacer preguntas hasta escribir 'finalizar'.
    """
    
    print("=" * 70)
    print("[CHAT] BIENVENIDO A TECHPRO - SOPORTE DE TIENDA DE TECNOLOGÍA")
    print("=" * 70)
    print("Soy tu vendedor asistente. Estoy aquí para ayudarte a encontrar")
    print("el producto perfecto para tus necesidades.")
    print("Escribe 'finalizar' para terminar la conversación.\n")
    
    # Copiar el historial para no modificar el original
    conversacion = historial.copy()
    
    # BUCLE PRINCIPAL DEL CHAT
    # El chat continúa hasta que el usuario escriba 'finalizar'
    while True:
        # Solicitar entrada del usuario
        print("-" * 70)
        usuario_input = input("[TU]: ").strip()
        
        # Verificar si el usuario quiere finalizar
        if usuario_input.lower() == "finalizar":
            print("\n[OK] ¡Gracias por tu visita a TechPro! Hasta pronto.")
            break
        
        # Validar que el usuario ingresó algo
        if not usuario_input:
            print("[AVISO] Por favor, ingresa una pregunta.")
            continue
        
        # Añadir la pregunta del usuario al historial
        conversacion.append({
            "role": "user",
            "parts": [usuario_input]
        })
        
        # 6. REALIZAR CONSULTA AL MODELO CON HISTORIAL
        # Enviamos todo el historial para mantener contexto de la conversación
        try:
            # Construir el mensaje de forma simple combinando el historial en texto
            # Esto es más compatible con la API de Gemini
            historial_texto = system_instruction + "\n\n"
            
            # Añadir los ejemplos del historial (few-shot)
            for item in historial:
                rol = "[User]" if item["role"] == "user" else "[Assistant]"
                mensaje = item["parts"][0] if isinstance(item["parts"], list) else item["parts"]
                historial_texto += f"{rol}: {mensaje}\n\n"
            
            # Añadir la nueva pregunta del usuario
            historial_texto += f"[User]: {usuario_input}\n[Assistant]:"
            
            # Enviar al modelo Gemini usando texto plano
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=historial_texto
            )
            
            # Obtener la respuesta del modelo
            if response and response.text:
                respuesta_modelo = response.text.strip()
                
                # Añadir la respuesta del modelo al historial para futuras consultas
                conversacion.append({
                    "role": "model",
                    "parts": [respuesta_modelo]
                })
                
                # Mostrar la respuesta formateada
                print(f"\n[VENDEDOR]: {respuesta_modelo}\n")
            else:
                print("[ERROR] No se recibió respuesta válida del modelo\n")
                
        except Exception as e:
            print(f"[ERROR] Error al procesar tu pregunta: {e}\n")
            # Remover la pregunta del usuario del historial si hubo error
            conversacion.pop()


# 7. PUNTO DE ENTRADA DEL PROGRAMA
if __name__ == "__main__":
    try:
        chat_tienda_tecnologia()
    except KeyboardInterrupt:
        print("\n\n[AVISO] Conversación interrumpida por el usuario.")
    except Exception as e:
        print(f"\n[ERROR] Error general: {e}")