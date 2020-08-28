from flask import Flask, render_template, url_for, request, redirect, jsonify
import matplotlib.pyplot as plt
from base64 import b64encode, b64decode
from io import BytesIO
from PIL import Image
from test import *
import numpy as np
from skimage.transform import resize
import cv2
from os import listdir
from random import randint
from imageio import get_reader

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/style_interpolation', methods=["POST"])
def StyleIT_interpolation():
    content_base64 = request.form['content']
    styles_base64 = request.form.getlist('styles[]')
    resolution = (int(request.form['resolution2']),
                  int(request.form['resolution1']))
    alpha = float(request.form['alpha'])
    preserve_color = False if request.form['preserve_color'] == 'false' else True

    content = resize(np.asarray(Image.open(
        BytesIO(b64decode(content_base64))).convert("RGB")), resolution)
    styles = [resize(np.asarray(Image.open(
        BytesIO(b64decode(style_base64))).convert("RGB")), resolution) for style_base64 in styles_base64]
    weights = [1/len(styles) for i in range(len(styles))]
    result = cv2.convertScaleAbs(
        style_interpolation(content, styles, weights, alpha=alpha, preserve_color=preserve_color, plot=False)*255)
    result = Image.fromarray(result)
    buffered = BytesIO()
    result.save(buffered, format="JPEG")
    result = b64encode(buffered.getvalue()).decode('ascii')
    return jsonify({'result': result})


@app.route('/style_image', methods=["POST"])
def StyleIT():
    content_base64 = request.form['content']
    style_base64 = request.form['style']
    resolution = (int(request.form['resolution2']),
                  int(request.form['resolution1']))
    alpha = float(request.form['alpha'])
    preserve_color = False if request.form['preserve_color'] == 'false' else True

    content = resize(np.asarray(Image.open(
        BytesIO(b64decode(content_base64))).convert("RGB")), resolution)
    style = resize(np.asarray(Image.open(
        BytesIO(b64decode(style_base64))).convert("RGB")), resolution)
    result = cv2.convertScaleAbs(
        style_image(content, style, alpha=alpha, preserve_color=preserve_color, plot=False)*255)
    result = Image.fromarray(result)
    buffered = BytesIO()
    result.save(buffered, format="JPEG")
    result = b64encode(buffered.getvalue()).decode('ascii')
    return jsonify({'result': result})


@app.route('/random', methods=["POST"])
def random():
    image_type = request.form['type']
    size = len(listdir(f"static/img/{image_type}"))
    n = randint(1, size)
    img = Image.open(f"static/img/{image_type}/{image_type}{n}.jpg")
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img = b64encode(buffered.getvalue()).decode('ascii')
    return jsonify({'img': img})


@app.route('/style_video', methods=["POST"])
def style_video():
    video = request.files['content']


if __name__ == "__main__":
    app.run(debug="True", host="0.0.0.0")
