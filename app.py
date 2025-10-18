import os
import random

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cambia-esta-clave")

# -----------------------------
# Utilidades de estado (por sesión)
# -----------------------------

# Función 1: Asegura que las variables de sesión estén inicializadas (puntos, intentos, número secreto, estado del juego)
# Autor: Marvin Rafael
def ensure_session_state():
    session.setdefault("points", 0)
    session.setdefault("tries", 0)
    session.setdefault("secret", random.randint(1, 100))
    session.setdefault("game_over", False)

# Función 2: Genera un nuevo número secreto aleatorio entre 1 y 100
# Autor: Leandro Demian
def new_secret():
    session["secret"] = random.randint(1, 100)
BASE_HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Juego: Adivina el número</title>
  <style>
    :root { --accent: #6C5CE7; --bg: #F5F7FB; --ok: #00B894; --warn: #E17055; }
    * { box-sizing: border-box; }
    body {
      margin: 0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: var(--bg); color: #222; display: grid; place-items: center; min-height: 100vh;
    }
    .card {
      width: min(560px, 92vw); background: #fff; border-radius: 16px; padding: 28px; box-shadow: 0 10px 25px rgba(0,0,0,.08);
    }
    h1 { margin: 0 0 8px; font-size: 28px; letter-spacing: .2px; }
    p.sub { margin: 0 0 20px; color:#555; }
    form { display:flex; gap:12px; align-items:center; }
    input[type=text] {
      flex: 1; padding: 12px 14px; font-size: 16px; border: 2px solid #e9ecf3; border-radius: 12px;
      outline: none; transition: border-color .2s ease;
    }
    input[type=text]:focus { border-color: var(--accent); }
    button {
      padding: 12px 18px; font-size: 16px; border: none; border-radius: 12px; cursor: pointer;
      background: var(--accent); color: white; font-weight: 600; letter-spacing:.3px;
    }
    .btn-outline { background: #fff; color: var(--accent); border: 2px solid var(--accent); }
    .msg { margin-top: 14px; font-size: 16px; padding: 10px 12px; border-radius: 10px; background: #f6f6ff; }
    .msg.ok { background: #e8fbf3; color: #05603a; border: 1px solid #b5efd5; }
    .msg.warn { background: #fff0ed; color: #7a2e14; border: 1px solid #ffd5cb; }
    .row { display:flex; gap:12px; margin-top: 12px; flex-wrap: wrap; }
    .pill { padding:8px 12px; border-radius: 999px; background:#f0f3fa; font-size:14px; }
    .points { font-weight:700; color: var(--accent); }
    .foot { margin-top: 14px; font-size: 13px; color:#666; }
    code { background:#f0f3fa; padding:2px 6px; border-radius:6px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Adivina el número del 1 al 100</h1>
    <p class="sub">Escribe un número o <code>terminar</code> para reiniciar el juego. Si aciertas ganas <strong>+100</strong> y se genera un nuevo número.</p>

    <form method="POST" action="{{ url_for('index') }}" autocomplete="off">
      <input type="text" name="user_input" placeholder="Número (1-100) o 'terminar'" required {% if game_over %}disabled{% endif %} autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" inputmode="text">
      <button type="submit" {% if game_over %}disabled{% endif %}>Probar</button>
    </form>

    {% if message %}
      <div class="msg {{ css_class }}">{{ message }}</div>
    {% endif %}

    <div class="row">
      <span class="pill">Puntos: <span class="points">{{ points }}</span></span>
      <span class="pill">Intentos: {{ tries }}</span>
    </div>

    {% if game_over %}
    <div class="row">
      <form method="POST" action="{{ url_for('reiniciar') }}">
        <button type="submit">Volver a jugar</button>
      </form>
    </div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/peticion", methods=["GET", "POST"])
@app.route("/juego", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
# Función 3: Controla la lógica principal del juego desde el navegador (rutas /, /peticion y /juego)
# Autor: Isaak Cabrera
def index():
    ensure_session_state()

    message = ""
    css_class = ""

    if request.method == "POST" and not session.get("game_over", False):
        raw_value = (request.form.get("user_input", "") or "").strip()

        if raw_value.lower() == "terminar":
            session["points"] = 0
            session["tries"] = 0
            session["game_over"] = False
            new_secret()
            message = "Juego terminado y reiniciado. ¡Todo a 0!"
            css_class = "ok"
        else:
            try:
                user_number = int(raw_value)
            except Exception:
                user_number = None

            if user_number is None or not (1 <= user_number <= 100):
                message = "Ingresa un número válido entre 1 y 100 o escribe 'terminar'."
                css_class = "warn"
            else:
                session["tries"] += 1
                secret = session.get("secret")

                if user_number == secret:
                    session["points"] += 100
                    message = f"¡Correcto! El número era {secret}. +100 puntos. Se generó un nuevo número secreto."
                    css_class = "ok"
                    new_secret()
                else:
                    new_secret()
                    message = "Incorrecto. Se generó un nuevo número. ¡Prueba de nuevo!"
                    css_class = "warn"

    return render_template_string(
        BASE_HTML,
        message=message,
        css_class=css_class,
        points=session.get("points", 0),
        tries=session.get("tries", 0),
        game_over=session.get("game_over", False),
    )

@app.post("/api/guess")
# Función 4: API del juego que procesa intentos de adivinar el número mediante peticiones JSON
# Autor: Isaak Cabrera
def api_guess():
    ensure_session_state()
    body = request.get_json(silent=True) or {}
    raw = body.get("user_number", body.get("user_input"))

    if isinstance(raw, str) and raw.strip().lower() == "terminar":
        session["points"] = 0
        session["tries"] = 0
        session["game_over"] = False
        new_secret()
        return jsonify({"ok": True, "reset": True, "points": 0, "tries": 0, "message": "Juego terminado y reiniciado."})

    try:
        user_number = int(raw)
    except Exception:
        return jsonify({"ok": False, "error": "'user_number' debe ser un entero o 'terminar'"}), 400

    if not (1 <= user_number <= 100):
        return jsonify({"ok": False, "error": "Número fuera de rango (1-100)"}), 400

    session["tries"] += 1
    secret = session.get("secret")

    if user_number == secret:
        session["points"] += 100
        new_secret()
        return jsonify({"ok": True, "correct": True, "awarded": 100, "points": session["points"], "tries": session["tries"], "message": "¡Correcto! +100 puntos."})
    else:
        new_secret()
        return jsonify({"ok": True, "correct": False, "points": session["points"], "tries": session["tries"], "message": "Incorrecto. Nuevo número generado."})
# -------------------------------------------------------------------------------------------
@app.post("/reiniciar")
# Función 5: Reinicia el juego desde el formulario del sitio web (botón "Volver a jugar")
# Autor: Raul Corcino
def reiniciar():
    
    ensure_session_state()
    session["points"] = 0
    session["tries"] = 0
    session["game_over"] = False
    new_secret()
    return redirect(url_for('index'))

@app.post("/reset")
# Función 6: Reinicia el juego desde una ruta alternativa (/reset)
# Autor: Raul Corcino
def reset_game():
    ensure_session_state()
    session["points"] = 0
    session["tries"] = 0
    session["game_over"] = False
    new_secret()
    return redirect(url_for("index"))

@app.post("/api/reset")
# Función 7: Reinicia el juego mediante la API (ruta /api/reset)
# Autor: Raul Corcino
def api_reset():
    ensure_session_state()
    session["points"] = 0
    session["tries"] = 0
    session["game_over"] = False
    new_secret()
    return jsonify({"ok": True, "message": "Juego reiniciado", "points": 0, "tries": 0})