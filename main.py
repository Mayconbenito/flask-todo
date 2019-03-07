from flask import Flask, request, render_template, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''
mysql.init_app(app)
connection = mysql.connect()

@app.route('/to-do/create', methods=['GET', 'POST', 'PUT', 'DELETE'])
def createTodo():
    if request.method == 'POST':
        cursor = connection.cursor()
        name = request.form['name']
        description = request.form['description']

        cursor.execute("INSERT INTO todos (name, description) VALUES (%s,%s)",(name, description))
        connection.commit()
        cursor.close()

        return redirect('/', code=301)

@app.route('/to-do/delete/<int:id>', methods=['GET'])
def deleteTodo(id):
    if request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("DELETE FROM todos WHERE id = %s" %(id))
        connection.commit()
        cursor.close()

        return redirect('/', code=301)

@app.route('/')
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    return render_template('home.html', todos=todos)

app.run(debug=True)