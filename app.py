import os
import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def create_connection(path: str):
    """Open path as a database"""
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful!")
    except Error as e:
        print(f"The error {e} occured")
    return connection


def execute_read_query(connection, query: str):
    """Use this function to read data from database"""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error {e} occured")


def execute_query(connection, query: str):
    """Used to create tabs in database"""
    connection = sqlite3.connect('my_discbag')
    print("Opened databas my_discbag succesfully!")

    connection.execute('CREATE TABLE discs ('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'name TEXT NOT NULL, speed INTEGER NOT NULL, '
                       'glide INTEGER NOT NULL, '
                       'turn REAL NOT NULL, '
                       'fade REAL NOT NULL, '
                       'weight INTEGER, '
                       'player_id INTEGER)')

    connection.close()


def execute_query_new_table(connection, query: str):
    """Used to create tabs in database"""
    connection = sqlite3.connect('my_discbag')
    print("Opened databas my_discbag succesfully!")

    connection.execute('CREATE TABLE discs ('
                       'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'name TEXT NOT NULL, speed INTEGER NOT NULL, '
                       'glide INTEGER NOT NULL, '
                       'turn REAL NOT NULL, '
                       'fade REAL NOT NULL, '
                       'weight INTEGER, '
                       'player_id INTEGER)')

    connection.close()


@app.route('/')
def home():
    # Find your current folder:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    dbfile_path = os.path.join(current_folder, "my_discbag.db")
    connection = create_connection(dbfile_path)

    query = """
        SELECT id ,name, speed, glide, turn, fade
        FROM discs
        ORDER BY speed DESC;
        """

    answer = execute_read_query(connection, query)

    return render_template("index.html", discs=answer)


@app.route('/info/<int:disc>')
def info(disc):

    # Find your current folder:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    dbfile_path = os.path.join(current_folder, "my_discbag.db")
    connection = create_connection(dbfile_path)

    result = None
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM discs WHERE id=?", (disc,))
        result = cursor.fetchall()[0]
    except Error as e:
        print(f"The error {e} occured")

    return render_template("info.html", disc=result)


@app.route('/remove/<int:disc>', methods=["GET"])
def remove(disc):

    # Find your current folder:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    dbfile_path = os.path.join(current_folder, "my_discbag.db")
    connection = create_connection(dbfile_path)

    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM discs WHERE id=?", (disc,))
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

    return redirect('/')


@app.route('/add', methods=["POST"])
def add():
    disc_name = request.form["name"]
    disc_speed = request.form["speed"]
    disc_glide = request.form["glide"]
    disc_turn = request.form["turn"]
    disc_fade = request.form["fade"]
    new_disc = disc_name, disc_speed, disc_glide, disc_turn, disc_fade

    query = f"INSERT INTO discs(name, speed, glide, turn, fade) VALUES{new_disc};"

    # Find your current folder:
    current_folder = os.path.abspath(os.path.dirname(__file__))
    dbfile_path = os.path.join(current_folder, "my_discbag.db")
    connection = create_connection(dbfile_path)

    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

    return redirect('/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
