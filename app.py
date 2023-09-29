from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps

app = Flask(__name__)
app.secret_key = "fgf43kjlk4jnc87sdjnm5kjd89jksd8jc8smdmnxcy7mk"

http_username = 'admin'
http_password = 'Brian@NutriStop'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in', False):
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == http_username and password == http_password:
            session['logged_in'] = True
            return render_template("index.html", logged_in=True)
        else:
            session['logged_in'] = False
            return render_template("index.html", logged_in=False, error="Invalid credentials")
    else:
        return render_template("index.html", logged_in=session.get('logged_in', False))

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session['logged_in'] = False
    return render_template("index.html", logged_in=False)

@app.route('/submit', methods=['POST'])
@login_required
def submit():
    i_ssid = request.form['i_ssid']
    i_pass = request.form['i_pass']
    vm_ssid = request.form['vm_ssid']
    vm_pass = request.form['vm_pass']

    data = {
        "i_ssid": i_ssid,
        "i_pass": i_pass,
        "vm_ssid": vm_ssid,
        "vm_pass": vm_pass
    }

    config_handler.save_config(data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

# gunicorn --chdir /root/server/ --bind 192.168.3.1:8081 app:app
# ps | grep gunicorn
# kill -9 (PID)
