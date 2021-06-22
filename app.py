
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request, redirect
from flask import url_for
from flask_cors import CORS
from flask_socketio import SocketIO
from repositories.DataRepository import DataRepository
from flask import render_template


import time
import threading
import Adafruit_DHT
import queue
import serial
from datetime import datetime
import datetime
from subprocess import check_output


appSetup = False

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    socketio.emit('connected', 1)


# SENSOR CODE


# LCD
status = 0

RS = 21
E = 20
D0 = 16
D1 = 12
D2 = 25
D3 = 24
D4 = 23
D5 = 26
D6 = 19
D7 = 13

lijst_pinnen = [16, 12, 25, 24, 23, 26, 19, 13]

DELAY = 0.001


# SETUP


GPIO.setmode(GPIO.BCM)


dht_sensor = Adafruit_DHT.DHT11

dht_sensor2 = Adafruit_DHT.DHT22


# Sensors
ldr_pin = 27

dht_pin = 4

dht2_pin = 26

# actuator + knop
knop = 18
servoPin = 22

GPIO.setup(servoPin, GPIO.OUT)

# +GPIO.setup(servo, GPIO.OUT)


def setup():
    global appSetup
    GPIO.setup(knop, GPIO.IN, GPIO.PUD_UP)
    GPIO.remove_event_detect(knop)

    if not appSetup:
        GPIO.add_event_detect(knop, GPIO.FALLING,
                              call_back_knop1_event, bouncetime=300)
    #     print("setup")
    appSetup = True

    # LCD

    GPIO.setup(RS, GPIO.OUT)

    GPIO.setup(E, GPIO.OUT)

    GPIO.setup(D0, GPIO.OUT)

    GPIO.setup(D1, GPIO.OUT)

    GPIO.setup(D2, GPIO.OUT)

    GPIO.setup(D3, GPIO.OUT)

    GPIO.setup(D4, GPIO.OUT)

    GPIO.setup(D5, GPIO.OUT)

    GPIO.setup(D6, GPIO.OUT)
    GPIO.setup(D7, GPIO.OUT)

    # output

    GPIO.output(RS, GPIO.LOW)

    GPIO.output(E, GPIO.LOW)

    GPIO.output(D0, GPIO.HIGH)
    GPIO.output(D1, GPIO.HIGH)
    GPIO.output(D2, GPIO.HIGH)
    GPIO.output(D3, GPIO.HIGH)
    GPIO.output(D4, GPIO.HIGH)
    GPIO.output(D5, GPIO.HIGH)
    GPIO.output(D6, GPIO.HIGH)
    GPIO.output(D7, GPIO.HIGH)

    init_LCD()

# LCD


def set_data_bits(value):
    mask = 0b00000001  # of 01
    for index in range(0, 8):
        pin = lijst_pinnen[index]
        #
        if value & mask:
            GPIO.output(pin, GPIO.HIGH)
            #
        else:
            GPIO.output(pin, GPIO.LOW)

        mask = mask << 1


def send_instruction(value):
    # Hier RS laag voor  instructie
    GPIO.output(RS, GPIO.LOW)

    # klokpuls met E lijn
    GPIO.output(E, GPIO.HIGH)

    # data klaarzetten
    set_data_bits(value)

    GPIO.output(E, GPIO.LOW)
    time.sleep(0.01)


def send_character(value):
    # E en RS
    # Hier RS hoog voor  data input
    GPIO.output(RS, GPIO.HIGH)

    # klokpuls met E lijn
    GPIO.output(E, GPIO.HIGH)
    # data klaarzetten
    set_data_bits(value)
    GPIO.output(E, GPIO.LOW)
    time.sleep(0.01)


def init_LCD():
    send_instruction(0b11000)  # function set

    send_instruction(0b1100)  # display on
    # end_instruction(0b1111)
    send_instruction(0b0001)  # clear display


def write_message(message):
    for character in message:
        send_character(ord(character))  # naar ascii code


#       print(ips)


def set_LCD():

    if status == 0:
        ips = check_output(['hostname', '--all-ip-addresses'])
        print(str(ips)[2:14])

        write_message(str(ips)[2:14])


def cursor_home():
    send_instruction(0b10)


# servo1 = GPIO.PWM(servo, 50)
servo = GPIO.PWM(servoPin, 50)

# SERVO


def call_back_knop1_event(knop):
    if GPIO.event_detected(knop):
        duty = 4

        # start met 0
        servo.start(4)
        print('wait 2 seconds')
        print('opened chest')
        time.sleep(1)

        # while duty <= 12:

        # loop from 2 to 12 (0 to 180)

        servo.ChangeDutyCycle(duty)
        time.sleep(1)
        # duty = duty + 1

        time.sleep(5)

        # terugdraaien naar 0graden  voor 2 seconden
        print("terugdraaien naar 0")
        servo.ChangeDutyCycle(8)
        time.sleep(0.5)

        # servo.stop()

        GPIO.remove_event_detect(knop)
        time.sleep(1)
        call_back_knop1_event(knop)


def open_chest():
    duty = 4

    # start met 0
    servo.start(0)
    print('wait 2 seconds')
    print('opened chest')
    time.sleep(1)

    # while duty <= 12:

    # loop from 2 to 12 (0 to 180)

    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    duty = duty + 1

    time.sleep(5)  # pauze

    # terugdraaien naar 0graden  voor 2 seconden
    print("terugdraaien naar 0")
    servo.ChangeDutyCycle(8)
    time.sleep(0.5)
    # servo.ChangeDutyCycle(5)
    # servo.stop()
    # time.sleep(0.5)


@socketio.on("message")
def listen_to_cta_click(msg):
    if msg == 'F2B_open_kist':
        open_chest()

        # dateTime om te gebruiken als paramater hieronder en voor de MYSQL Databse:
currentTime = datetime.datetime.now()


def sensor_vochtigheid():
    while True:
        humidity, temperature = Adafruit_DHT.read(dht_sensor, dht_pin)
        DataRepository.create_vochtigheid(
            1, humidity, currentTime, currentTime)
        print("Inserted humidity")
        time.sleep(5)  # om de x seconden inserten

        if humidity is not None and temperature is not None:
            return humidity, temperature


def sensor_temperatuur():

    while True:
        humidity, temperature = Adafruit_DHT.read(dht_sensor, dht_pin)
        DataRepository.create_temperatuur(
            2, temperature, currentTime, currentTime)
        print("Inserted temperature")
        time.sleep(5)  # om de x seconden inserten

        if humidity is not None and temperature is not None:
            return temperature, humidity


def sensor_licht():
    light = read_sensor_licht()
    while True:
        DataRepository.create_licht(3, light, currentTime, currentTime)
        print("Inserted light")
        time.sleep(5)
        if light is not None:
            return light


def read_sensor_licht():
    while True:
        GPIO.setup(ldr_pin, GPIO.OUT)
        GPIO.output(ldr_pin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(ldr_pin, GPIO.IN)

        current_time = time.time()
        diff = 0

        while(GPIO.input(ldr_pin) == GPIO.LOW):
            diff = time.time() - current_time
            if diff is not None:
                diff = str(round((diff * 1000000), 2))
                # str(round((diff * 1000000)), 2)

            # print((diff))

              #  print("light {0:0.2f}".format(diff))
                time.sleep(1)
                return diff


# # ENDLESS LOOP SENSORS(anders INSERT het max 2 keer naar Database)


def loop():
    while True:

        sensor_vochtigheid()

        sensor_temperatuur()

        sensor_licht()

        time.sleep(0.5)

        set_LCD()
        # time.sleep(0.01)
        cursor_home()

    # API ENDPOINT
    # Custom endpoint
endpoint = '/api/v1'


@ app.route('/')
def index():
   # temperature, humidity = sensor_vochtigheid()
    # temperature=temperature, humidity=humidity
    return render_template("index.html")


# ALLE METINGEN
@ app.route(endpoint + '/metingen/<id>', methods=['GET'])
def read_alle_metingen(id):
    if request.method == 'GET':
        data = DataRepository.read_alle_metingen(id)
        if data is not None:
            return jsonify(read_alle_metingen=data), 200
        else:
            return jsonify(message="error, could not reach endpoint of 'metingen'"), 404


# VOCHTIGHEID
@ app.route(endpoint + '/vochtigheid', methods=['GET'])
def vochtigheid():
    if request.method == 'GET':
        data = DataRepository.read_vochtigheid()
        if data is not None:
            return jsonify(vochtigheid=data), 200
        else:
            return jsonify(message="error, could not reach endpoint of 'vochtigheid'"), 404

# TEMPERATUUR


@ app.route(endpoint + '/temperatuur', methods=['GET'])
def temperatuur():
    if request.method == 'GET':
        data = DataRepository.read_temperatuur()
        if data is not None:
            return jsonify(temperatuur=data), 200
        else:
            return jsonify(message="error, could not reach endpoint of 'temperatuur'"), 404


# LICHT


@ app.route(endpoint + '/licht', methods=['GET'])
def licht():
    if request.method == 'GET':
        data = DataRepository.read_licht()
        if data is not None:
            return jsonify(licht=data), 200
        else:
            return jsonify(message="error, could not reach endpoint of 'licht'"), 404


# setup()
if __name__ == '__main__':
    try:
        # nodig zodat setup goed werkt

        # threading.Thread(target=sensor_vochtigheid).start()
        # threading.Thread(target=sensor_temperatuur).start()
        # threading.Thread(target=sensor_licht).start()

        #
        setup()
        while True:
            # call_back_knop1_event(knop)

            threading.Thread(target=call_back_knop1_event(knop)).start()
            time.sleep(1)
            threading.Thread(target=loop).start()
            time.sleep(1)

            # app.run(host='localhost', port=5000, debug=True)
            socketio.run(app, debug=True, host='0.0.0.0')

    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
        print("cleanup pi")

    # deze gebuiken, anders socket error
