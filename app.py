from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = "flash message"


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'crudapp'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM estudantes")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', estudantes = data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Dados inseridos com sucesso!!")
        nome = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO estudantes (nome, email) VALUES (%s, %s)", (nome, email))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Registro excluído com sucesso.")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM estudantes WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('index'))




@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE estudantes
               SET nome=%s, email=%s
               WHERE id=%s
            """, (name, email, id_data))
        flash("Dados atualizados com sucesso!!")
        mysql.connection.commit()
        return redirect(url_for('index'))





if __name__ == "__main__":
    app.run(debug=True)