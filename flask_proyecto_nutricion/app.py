from flask import Flask, render_template, request, redirect, url_for, session
from controllers.youtube_controller import youtube_bp


app = Flask(__name__, template_folder="templates")
app.secret_key = "clave_secreta"

app.register_blueprint(youtube_bp)

# ----------------
# DATOS EN MEMORIA
# ----------------

usuarios = []
estudiantes = []
# ------
# LOGIN
# ------
@app.route("/", methods = ["GET","POST"])
def login(): 
   if request.method == "POST": 
      user = request.form["usuario"]
      pwd = request.form["password"]
      
      for u in usuarios: 
         if u["usuario"] == user and u["password"] == pwd:
            session["usuario"] = user
            return redirect(url_for("menu"))
         
      return "Usuario o contraseña incorrectos"
      
   return render_template("login.html")
   
# ---------
# REGISTRO
# ---------
@app.route("/registro", methods=["GET", "POST"])
def registro(): 
   if request.method == "POST": 
      usuarios.append({
         "usuario": request.form["usuario"],
         "password": request.form["password"]
      })
      return redirect(url_for("login"))
   
   return render_template("register.html")

# -----------
# MENÚ
# -----------
@app.route("/menu")
def menu():
   if "usuario" not in session:
      return redirect(url_for("login"))

   return render_template("menu.html")

# -----------
# DASHBOARD
# -----------
@app.route("/dashboard", methods=["GET","POST"])
def dashboard(): 
   if "usuario" not in session: 
      return redirect(url_for("login"))
   
   if request.method == "POST": 
      estudiantes.append({
         "nombre": request.form["nombre"],
         "edad": request.form["edad"],
         "carrera": request.form["carrera"]
      })
      
   return render_template("dashboard.html", estudiantes = estudiantes)

# --------------------
# Eliminar estudiante
# --------------------
@app.route("/eliminar/<int:index>")
def eliminar(index): 
   if "usuario" not in session: 
      return redirect(url_for("login"))
   
   estudiantes.pop(index)
   return redirect(url_for("dashboard"))

# --------------------
# Editar estudiante
# --------------------
@app.route("/editar/<int:index>", methods=["POST"])
def editar(index):
   if "usuario" not in session:
      return redirect(url_for("login"))

   estudiantes[index]["nombre"] = request.form["nombre"]
   estudiantes[index]["edad"] = request.form["edad"]
   estudiantes[index]["carrera"] = request.form["carrera"]

   return redirect(url_for("dashboard"))


# --------------
# CERRAR SESIÓN 
# --------------
@app.route("/logout")
def logout(): 
   session.clear()
   return redirect(url_for("login"))

if __name__ == "__main__": 
   app.run(debug=True)

