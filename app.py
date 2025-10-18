from flask import Flask, request, render_template_string, session, jsonify, redirect, url_for
import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get(&quot;FLASK_SECRET_KEY&quot;, &quot;cambia-esta-
clave&quot;)
@app.route(&quot;/&quot;)
def root():
return &quot;OK&quot;
if __name__ == &quot;__main__&quot;:
app.run(debug=True, host=&quot;0.0.0.0&quot;, port=5000)
