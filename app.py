from flask import Flask, render_template, url_for, request, redirect, jsonify
import matplotlib.pyplot as plt
from base64 import b64encode, b64decode
from io import BytesIO
from PIL import Image
from test import style_image, style_interpolation, style_video
import numpy as np
from skimage.transform import resize
import cv2
from os import listdir, system, remove, environ
from random import randint
from imageio import get_reader
from shutil import copy, move
import glob
from pymediainfo import MediaInfo

app = Flask(__name__)


@app.route('/')
def index():
    if glob.glob("content_video.*"):
        for f in glob.glob("content_video.*"):
            remove(f)
    return render_template('index.html')


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


@app.route('/upload_video', methods=["POST"])
def upload_video():
    try:
        video = request.files['video']
        filepath = "content_video." + video.filename.split(".")[1]
        video.save(filepath)
        media_info = MediaInfo.parse(filepath)
        duration = media_info.tracks[0].duration/1000
        fps = media_info.tracks[0].frame_rate
        print(fps)
        return jsonify({'duration': duration, 'frame_rate': fps})
    except KeyError:
        filepath = "paulvideo.mp4"
        copy(f"static/img/{filepath}", f"{filepath}")
        move(f"{filepath}", "content_video.mp4")
        return jsonify({'duration': 11.562667, 'frame_rate': 29.856})


@app.route('/style_video', methods=["POST"])
def StyleIT_video():
    filepath = "content_video.mp4"
    resolution = (int(request.form['resolution2']),
                  int(request.form['resolution1']))
    style_base64 = request.form['style']
    style = resize(np.asarray(Image.open(
        BytesIO(b64decode(style_base64))).convert("RGB")), resolution)
    alpha = float(request.form['alpha'])
    fps = int(request.form['fps'])
    preserve_color = False if request.form['preserve_color'] == 'false' else True

    style_video(filepath, style,
                "result", alpha, preserve_color, resolution, frame_skip=fps)
    remove(filepath)
    move('result.mp4', 'static/result.mp4')

    return jsonify({'path': "result.mp4"})


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


@app.route('/rotate', methods=["POST"])
def rotate():
    f = request.form['file']
    result = Image.open(BytesIO(b64decode(f.split(",")[1]))).rotate(
        90, resample=0, expand=True)
    buffered = BytesIO()
    result.save(buffered, format="JPEG")
    result = f.split(",")[0] + "," + \
        b64encode(buffered.getvalue()).decode('ascii')
    return jsonify({'result': result})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(environ.get('PORT', 8080)))
