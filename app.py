from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "udulguun"
app.config['MYSQL_PASSWORD'] = "rHmQxy"
app.config['MYSQL_DB'] = "udulguun_db"

mysql_client = mysql.connector.connect(
    host="localhost",
    user="udulguun",
    password="rHmQxy",
    database="dresszenfinder5",
    buffered=True
)

@app.route('/location', methods=['GET'])
def location():
    # Get the client's IP address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Perform geolocation lookup using ipinfo.io
    try:
        response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        if response.status_code == 200:
            data = response.json()
            location = data.get('loc', '0,0')  # Default to '0,0' if location is unavailable
            lat, lng = map(float, location.split(','))
            return render_template('location.html', lat=lat, lng=lng, ip=client_ip)
    except Exception as e:
        print(f"Error during IP geolocation: {e}")
    
    # Fallback to default location if lookup fails
    return render_template('location.html', lat=0.0, lng=0.0, ip='Unknown')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term')  # The search term typed by the user
    if term:
        term = term.lower()  # Normalize to lowercase for case-insensitive search

        # Query for matching items from the database
        cur = mysql_client.cursor()
        cur.execute(
            """
            SELECT cloth_description FROM clothing_item 
            WHERE LOWER(cloth_description) LIKE %s LIMIT 10
            """,
            (f'%{term}%',)
        )

        results = cur.fetchall()
        cur.close()

        # Extract only the name column from the results
        suggestions = [result[0] for result in results]
        
        return jsonify(suggestions)  # Return suggestions as a JSON response
    return jsonify([])  # Return an empty list if no term was provided


@app.route('/', methods=['GET', 'POST'])
def register():  # Changed function name from `index` to `register`
    if request.method == 'POST':
        username = request.form['username']
        size = request.form['size']
        age = request.form['age']
        email = request.form['email']
        gender = request.form['gender']
        password = request.form['password']

        cur = mysql_client.cursor()
        cur.execute("INSERT INTO users(username, size, age, email, gender, password) VALUES(%s, %s, %s, %s, %s, %s)", 
                    (username, size, age, email, gender, password))
        mysql_client.commit()
        cur.close()

        flash("User added successfully!", "success")  # Flash a success message
        return redirect(url_for('register'))  # Changed redirection to `register`

    return render_template('register.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        # Normalize the query
        query = query.lower()

        # Search for clothing items based on the query
        cur = mysql_client.cursor()
        cur.execute(
            "SELECT * FROM clothing_item WHERE LOWER(color) LIKE %s OR LOWER(season) LIKE %s OR LOWER(cloth_description) LIKE %s",
            (f'%{query}%', f'%{query}%', f'%{query}%')
        )
        results = cur.fetchall()
        cur.close()
        
        return render_template('search_results.html', results=results)
    
    return redirect(url_for('index'))


# Route to serve individual item HTML pages
@app.route('/item/<item_name>')
def item(item_name):
    # Render the specific item HTML page
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
    # Check if the user is logged in and is 'admin'
    if 'loggedin' in session and session['username'] == 'admin':
        return render_template('maintenance.html')
    else:
        return redirect(url_for('maintenance_err'))



@app.route('/index')  
def index():
    if 'loggedin' in session:
        # Query clothing descriptions from the database
        query = "SELECT cloth_description FROM clothing_item"
        cur = mysql_client.cursor()
        cur.execute(query)
        clothing_descriptions = cur.fetchall()  # Get all descriptions
        cur.close()

        # Pass clothing descriptions to the template
        return render_template('index.html', username=session['username'], clothing_descriptions=clothing_descriptions)
    
    return redirect(url_for('signin'))  # Redirect to sign-in if not logged in


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

        cur = mysql_client.cursor()
        cur.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        record = cur.fetchone()

        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            return redirect(url_for('index'))  # Redirect to the main index page
        else:
            msg = 'Incorrect username or password'

    return render_template('signin.html', msg=msg)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8006)
