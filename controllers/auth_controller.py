from flask import Blueprint, render_template, request, redirect, url_for, session
from services.db_service import DatabaseService
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print("="*50)
        print("INTENTO DE LOGIN")
        print(f"Email recibido: '{email}'")
        print(f"Password recibido: '{password}'")
        print(f"Longitud password: {len(password)}")
        
        user = DatabaseService.get_user_by_email(email)
        
        if user:
            print(f"Usuario encontrado en BD:")
            print(f"  Email en BD: '{user.email}'")
            print(f"  Password en BD: '{user.password_hash}'")
            print(f"  Longitud password BD: {len(user.password_hash)}")
            print(f"  Rol: {user.rol}")
            
            # Comparación directa de texto plano (SIN HASEAR)
            if password == user.password_hash:
                print("✅ CONTRASEÑA CORRECTA")
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['user_rol'] = user.rol
                session['nutriologo_id'] = user.nutriologo_id
                session['paciente_id'] = user.paciente_id
                
                return redirect(url_for('menu'))
            else:
                print("❌ CONTRASEÑA INCORRECTA")
                print(f"Comparación: '{password}' vs '{user.password_hash}'")
                return render_template('login.html', error='Email o contraseña incorrectos')
        else:
            print(f"❌ Usuario NO encontrado con email: '{email}'")
            return render_template('login.html', error='Email o contraseña incorrectos')
    
    return render_template('login.html')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apP = request.form['apP']
        apM = request.form.get('apM', '')
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        sexo = request.form['sexo']
        edadNac = request.form['edadNac']
        telefono = request.form.get('telefono', '')
        
        # Validar que las contraseñas coincidan
        if password != confirm_password:
            return render_template('register.html', error='Las contraseñas no coinciden')
        
        # Verificar si el email ya existe
        if DatabaseService.get_user_by_email(email):
            return render_template('register.html', error='El email ya está registrado')
        
        # Obtener el primer nutriólogo disponible (USANDO DatabaseService)
        nutriologo = DatabaseService.get_primer_nutriologo()
        
        if not nutriologo:
            return render_template('register.html', error='Error en el sistema. Contacte al administrador.')
        
        # Crear paciente
        paciente_id = DatabaseService.create_paciente(
            nombre, apP, apM, sexo, edadNac, telefono, nutriologo['idNutriologo']
        )
        
        # Crear usuario
        DatabaseService.create_usuario(email, password, 'paciente', None, paciente_id)
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
