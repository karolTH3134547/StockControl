from flask import Flask, render_template, request, redirect, session, flash
import pymysql

app = Flask(__name__)
app.secret_key = "sena3134547"

def conectar():
    return pymysql.connect(
        host='localhost', 
        user='root', 
        password='', 
        database='inventario_barrio'
    )

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['usuario']
        clave = request.form['clave']
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM usuarios WHERE usuario=%s AND clave=%s", (user, clave))
        data = cur.fetchone()
        con.close()
        if data:
            session['user'] = user
            return redirect('/inicio')
        else:
            flash("Usuario o clave incorrecta")
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    if 'user' not in session:
        return redirect('/')
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM productos ORDER BY cantidad ASC")
    productos = cur.fetchall()
    cur.execute("SELECT COUNT(*), SUM(cantidad), SUM(cantidad*precio_venta) FROM productos")
    stats = cur.fetchone()
    con.close()
    return render_template('index.html', productos=productos, stats=stats)

@app.route('/agregar', methods=['GET','POST'])
def agregar():
    if 'user' not in session:
        return redirect('/')
    if request.method == 'POST':
        datos = (
            request.form['nombre'], 
            request.form['categoria'], 
            request.form['cantidad'], 
            request.form['p_compra'], 
            request.form['p_venta'], 
            request.form['proveedor']
        )
        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO productos(nombre,categoria,cantidad,precio_compra,precio_venta,proveedor) VALUES (%s,%s,%s,%s,%s,%s)", datos)
        con.commit()
        con.close()
        return redirect('/inicio')
    return render_template('agregar.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM productos WHERE id=%s", (id,))
    con.commit()
    con.close()
    return redirect('/inicio')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
