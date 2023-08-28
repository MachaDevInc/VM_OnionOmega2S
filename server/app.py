import os
import time
import stripe
from flask import Flask, render_template, request, session, redirect, url_for
from threading import Thread
from functools import wraps
from dotenv import load_dotenv, find_dotenv
from config_handler import (
    save_config,
    load_config,
    save_VM_config,
    load_VM_config,
    save_Terminal_config,
    load_Terminal_config,
)

app = Flask(__name__)
app.secret_key = "fgf43kjlk4jnc87sdjnm5kjd89jksd8jc8smdmnxcy7mk"

http_username = "admin"
http_password = "Brian@NutriStop"

load_dotenv(find_dotenv())

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

reader_id = os.getenv("TERMINAL_ID")


def process_i_ssid(i_ssid, i_pass):
    command = "wifisetup add -ssid " + i_ssid + " -encr psk2 -password " + i_pass
    os.system(command)
    command = "wifisetup priority -ssid " + i_ssid + " -move top"
    os.system(command)
    pass


def process_vm_ssid(vm_ssid, vm_pass):
    command = "uci set wireless.ap.ssid='" + vm_ssid + "'"
    os.system(command)
    command = "uci set wireless.ap.key='" + vm_pass + "'"
    os.system(command)
    command = "uci commit wireless"
    os.system(command)
    command = "wifi"
    os.system(command)


def process_restart_service():
    time.sleep(10)
    command = "/etc/init.d/my_gunicorn_server restart"
    os.system(command)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in", False):
            return redirect(url_for("index", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == http_username and password == http_password:
            session["logged_in"] = True
            return render_template("index.html", logged_in=True)
        else:
            session["logged_in"] = False
            return render_template(
                "index.html", logged_in=False, error="Invalid credentials"
            )
    else:
        return render_template("index.html", logged_in=session.get("logged_in", False))


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session["logged_in"] = False
    return render_template("index.html", logged_in=False)


@app.route("/submitCredentials", methods=["POST"])
@login_required
def submitCredentials():
    i_ssid = request.form["i_ssid"]
    i_pass = request.form["i_pass"]
    vm_ssid = request.form["vm_ssid"]
    vm_pass = request.form["vm_pass"]

    data = load_config()

    if i_ssid != "":
        data["i_ssid"] = i_ssid
    if i_pass != "":
        data["i_pass"] = i_pass
    if vm_ssid != "":
        data["vm_ssid"] = vm_ssid
    if vm_pass != "":
        data["vm_pass"] = vm_pass

    save_config(data)

    if (i_ssid != "") & (i_pass != ""):
        # Run the commands in a separate thread
        command_thread1 = Thread(target=process_i_ssid, args=(i_ssid, i_pass))
        command_thread1.start()

    if (vm_ssid != "") & (vm_pass != ""):
        # Run the commands in a separate thread
        command_thread2 = Thread(target=process_vm_ssid, args=(vm_ssid, vm_pass))
        command_thread2.start()

    if (i_ssid != "") & (i_pass != "") | ((vm_ssid != "") & (vm_pass != "")):
        # Run the commands in a separate thread
        command_thread3 = Thread(target=process_restart_service)
        command_thread3.start()

    return render_template("index.html")


@app.route("/submitLocation", methods=["POST"])
@login_required
def submitLocation():
    display_name = request.form["display_name"]
    line1 = request.form["line1"]
    city = request.form["city"]
    state = request.form["state"]
    country = request.form["country"]
    postal_code = request.form["postal_code"]
    location_added = None
    error_message = None

    data = {}

    if display_name != "":
        data["display_name"] = display_name
    if line1 != "":
        data["line1"] = line1
    if city != "":
        data["city"] = city
    if state != "":
        data["state"] = state
    if country != "":
        data["country"] = country
    if postal_code != "":
        data["postal_code"] = postal_code

    save_Terminal_config(data)

    try:
        # Create a new location here
        location_response = stripe.terminal.Location.create(
            display_name=data["display_name"],
            address={
                "line1": data["line1"],
                "city": data["city"],
                "state": data["state"],
                "country": data["country"],
                "postal_code": data["postal_code"],
            },
        )

        if "id" in location_response:
            data["location_id"] = location_response.id
            save_Terminal_config(data)
            location_added = (
                "New location added as " + str(location_response["display_name"])
            )
            print(location_response["id"])
    except Exception as e:
        error_message = str(e)
        print(f"Error: {error_message}")

    return render_template("index.html", error=error_message, success=location_added)


@app.route("/submitReader", methods=["POST"])
@login_required
def submitReader():
    reader_label = request.form["reader_label"]
    registration_code = request.form["registration_code"]
    reader_added = None
    error_message = None

    data = load_Terminal_config()

    if reader_label != "":
        data["reader_label"] = reader_label
    if registration_code != "":
        data["registration_code"] = registration_code

    save_Terminal_config(data)

    try:
        # Create a new location here
        location_response = stripe.terminal.Reader.create(
        registration_code=data["registration_code"],
        label=data["reader_label"],
        location=data["location_id"],
        )

        if "id" in location_response:
            reader_added = (
                "New Reader added as " + str(location_response["label"])
            )
            print(location_response["id"])
    except Exception as e:
        error_message = str(e)
        print(f"Error: {error_message}")

    return render_template("index.html", error=error_message, success=reader_added)


@app.route("/submitVMConfig", methods=["POST"])
@login_required
def submitVMConfig():
    left_compartment_unit_price = request.form["left_compartment_unit_price"]
    right_compartment_unit_price = request.form["right_compartment_unit_price"]

    data = load_VM_config()

    if left_compartment_unit_price != "":
        data["left_compartment_unit_price"] = left_compartment_unit_price
    if right_compartment_unit_price != "":
        data["right_compartment_unit_price"] = right_compartment_unit_price

    save_VM_config(data)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

# gunicorn --chdir /root/server/ --bind 192.168.3.1:8081 app:app
# ps | grep gunicorn
# kill -9 (PID)
