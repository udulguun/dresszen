from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
from mysql.connector import pooling, Error
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection pool
db_config = {
    "host": "localhost",
    "user": "udulguun",
    "password": "rHmQxy",
    "database": "dresszenfinder5",
    "buffered": True
}
mysql_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)


# Utility function for database queries
def execute_query(query, params=None, fetch=False):
    try:
        conn = mysql_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params if params else ())
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result

        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Database Error: {e}")
        if conn.is_connected():
            conn.close()


@app.route('/location', methods=['GET'])
def location():
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    try:
        response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        if response.status_code == 200:
            data = response.json()
            location = data.get('loc', '0,0')  # Default to '0,0' if unavailable
            lat, lng = map(float, location.split(','))
            return render_template('location.html', lat=lat, lng=lng, ip=client_ip)
    except Exception as e:
        print(f"Error during IP geolocation: {e}")
    return render_template('location.html', lat=0.0, lng=0.0, ip='Unknown')


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term')
    if term:
        query = """
        SELECT cloth_description FROM clothing_item 
        WHERE LOWER(cloth_description) LIKE %s LIMIT 10
        """
        results = execute_query(query, (f'%{term.lower()}%',), fetch=True)
        suggestions = [result[0] for result in results]
        return jsonify(suggestions)
    return jsonify([])


@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        size = request.form['size']
        age = request.form['age']
        email = request.form['email']
        gender = request.form['gender']
        password = request.form['password']

        query = """
        INSERT INTO users(username, size, age, email, gender, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (username, size, age, email, gender, password))
        flash("User added successfully!", "success")
        return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        search_query = """
        SELECT * FROM clothing_item
        WHERE LOWER(color) LIKE %s OR LOWER(season) LIKE %s OR LOWER(cloth_description) LIKE %s
        """
        results = execute_query(search_query, (f'%{query.lower()}%',) * 3, fetch=True)
        return render_template('search_results.html', results=results)
    return redirect(url_for('index'))


@app.route('/item/<item_name>')
def item(item_name):
    return render_template(f'{item_name}.html')


@app.route('/tops')
def tops():
    return render_template('tops.html')


@app.route('/bottoms')
def bottoms():
    return render_template('bottoms.html')


@app.route('/shoes')
def shoes():
    return render_template('shoes.html')


@app.route('/acc')
def acc():
    return render_template('acc.html')


@app.route('/brands')
def brands():
    return render_template('brands.html')


@app.route('/saved')
def saved():
    return render_template('saved.html')


@app.route('/imprint')
def imprint():
    return render_template('imprint.html')


@app.route('/maintenance_err')
def maintenance_err():
    return render_template('maintenance_err.html')


@app.route('/maintenance')
def maintenance():
    if 'loggedin' in session and session['username'] == 'admin':
        return render_template('maintenance.html')
    else:
        return redirect(url_for('maintenance_err'))


@app.route('/index')
def index():
    if 'loggedin' in session:
        query = "SELECT cloth_description FROM clothing_item"
        clothing_descriptions = execute_query(query, fetch=True)
        return render_template('index.html', username=session['username'], clothing_descriptions=clothing_descriptions)
    return redirect(url_for('signin'))


@app.route('/signout')
def signout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('signin'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        record = execute_query(query, (username, password), fetch=True)

        if record:
            session['loggedin'] = True
            session['username'] = record[0][1]
            return redirect(url_for('index'))
        else:
            msg = 'Incorrect username or password'
    return render_template('signin.html', msg=msg)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8006)
