from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  

@app.before_request
def init_session():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def gestion_productos():
    productos = session['productos']
    return render_template('index.html', productos=productos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # Obtén los datos del formulario
        id = len(session['productos']) + 1
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        categoria = request.form['categoria']
        fecha_vencimiento = request.form['fecha_vencimiento']
        
        try:
            precio = float(precio)  
        except ValueError:
            
            return "Error: El precio debe ser un número válido."

        producto = {'id': id, 'nombre': nombre, 'cantidad': cantidad, 'precio': precio, 'categoria': categoria, 'fecha_vencimiento': fecha_vencimiento}
        session['productos'].append(producto)
        session.modified = True
        return redirect(url_for('gestion_productos'))

    return render_template('nuevo.html')



@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    productos = session['productos']
    session['productos'] = [producto for producto in productos if producto['id'] != id]
    session.modified = True
    return redirect(url_for('gestion_productos'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session['productos']
    producto = next((prod for prod in productos if prod['id'] == id), None)

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('gestion_productos'))

    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
