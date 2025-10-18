import os
import random
from flask import Flask, session
app = Flask(__name__)
app.secret_key = os.environ.get(&quot;FLASK_SECRET_KEY&quot;, &quot;cambia-esta-
clave&quot;)
# -----------------------------
# Utilidades de estado (por sesión)
# -----------------------------
# Función 1: Asegura que las variables de sesión estén inicializadas
(puntos, intentos, número secreto, estado del juego)
# Autor: Marvin Rafael
def ensure_session_state():
session.setdefault(&quot;points&quot;, 0)
session.setdefault(&quot;tries&quot;, 0)
session.setdefault(&quot;secret&quot;, random.randint(1, 100))
session.setdefault(&quot;game_over&quot;, False)
# Función 2: Genera un nuevo número secreto aleatorio entre 1 y 100
# Autor: Leandro Demian
def new_secret():
session[&quot;secret&quot;] = random.randint(1, 100)

@app.route(&quot;/&quot;)
def root():
return &quot;OK&quot;
if __name__ == &quot;__main__&quot;:
app.run(debug=True, host=&quot;0.0.0.0&quot;, port=5000)