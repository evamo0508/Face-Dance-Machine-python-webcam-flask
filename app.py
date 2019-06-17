from sys import stdout
from makeup_artist import Makeup_artist
import logging
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from flask_sslify import SSLify
from camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64


app = Flask(__name__)
sslify = SSLify(app)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False #for the purpose of SSLify
socketio = SocketIO(app)
camera = Camera(Makeup_artist())


@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    camera.enqueue_input(input)
    #camera.enqueue_input(base64_to_pil_image(input))

@socketio.on('request condition', namespace='/test')
def return_condition(input):
    #print("return rate: {}".format(camera.get_framecount()))
    return camera.get_output_list_length(), camera.get_process_list_length()


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")

@socketio.on('input audio', namespace='/test')
def test_audio(input):
    #input = input.split(",")[1]
    camera.audio(input)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""

    app.logger.info("starting to generate frames!")
    while True:
        frame = camera.get_frame() #pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
    #app.run(host='0.0.0.0', port=5000)
