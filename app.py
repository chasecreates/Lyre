import json
import os
from flask import Flask, render_template, request, redirect, send_from_directory, jsonify
import indicoio
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import operator
import spotipy
import cv2
import httplib, urllib, base64
import locale
from spotipy.oauth2 import SpotifyClientCredentials
import requests

client_credentials_manager = SpotifyClientCredentials('d4cf6e1110fb4404976e9aa4c0d637af', '0863f4c36ba540358ac8a50baa9c8312')

TOP_TRACKS_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}/top-tracks'

GET_ARTIST_ENDPOINT = 'https://api.spotify.com/v1/artists/{id}'

locale.setlocale(locale.LC_ALL, "")

app = Flask(__name__)

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = set(['png', 'tiff', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

spotify = spotipy.Spotify()



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        




@app.route('/go/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = image_analysis(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            j_result = jsonify(result)
            
            the_max = max(result, key=result.get)
            
            if the_max == 'anger':
                id = '2QsynagSdAqZj3U9HgDzjD'
                artist = get_artist(id)
                
                
                tracksdata = get_artist_top_tracks(id)
                tracks = tracksdata['tracks']
                
                html = render_template('results.html',
                                      artist=artist,
                                      tracks=tracks
                                      
                                      )
                return html
            
            elif the_max == 'fear':
                id = '2gCsNOpiBaMNh20jQ5prf0'
                artist = get_artist(id)
                
                
                tracksdata = get_artist_top_tracks(id)
                tracks = tracksdata['tracks']
                
                html = render_template('results.html',
                                      artist=artist,
                                      tracks=tracks
                                      
                                      )
                return html
            elif the_max == 'disgust':
                id = '2wOqMjp9TyABvtHdOSOTUS'
                artist = get_artist(id)
                
                
                tracksdata = get_artist_top_tracks(id)
                tracks = tracksdata['tracks']
                
                html = render_template('results.html',
                                      artist=artist,
                                      tracks=tracks
                                      
                                      )
                return html

                
                
                
            elif the_max == 'contempt':
                id = '2f9PTWJfMMDTAFZcvHy1Z5'
                artist = get_artist(id)
                
                
                tracksdata = get_artist_top_tracks(id)
                tracks = tracksdata['tracks']
                
                html = render_template('results.html',
                                      artist=artist,
                                      tracks=tracks
                                      
                                      )
                

                return html
                
            elif the_max == 'surprise':
                id = '6l3HvQ5sa6mXTsMTB19rO5'
                artist = get_artist(id)
                
                
                tracksdata = get_artist_top_tracks(id)
                tracks = tracksdata['tracks']
                
                html = render_template('results.html',
                                      artist=artist,
                                      tracks=tracks
                                      
                                      )
                

                
                return html
            elif the_max == 'happiness':
                id = '6sFIWsNpZYqfjUpaCgueju'
                artist = get_artist(id)
                
                
                tracksdata = get_artist_top_tracks(id)
                tracks = tracksdata['tracks']
                
                html = render_template('results.html',
                                      artist=artist,
                                      tracks=tracks
                                      
                                      )
            
                
            
                return html
            

            
        
        
    return render_template('index.html')

def image_analysis(filepath):
    headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '13cdd7a1665f4928bfccc726cd521700',
}
    params = urllib.urlencode({
    # Request parameters
    'language': 'unk',
    'detectOrientation ': 'true',
})
    data = open(filepath, 'rb').read()
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, data, headers)
    response = conn.getresponse()
    data = response.read()
    data = json.loads(data)
    data = data[0]['scores']
    for key, value in data.iteritems():
        data[key] = locale.format("%f", value, 1)
        
    return data
    
# https://developer.spotify.com/web-api/get-artists-top-tracks/
def get_artist_top_tracks(artist_id, country='US'):
    url = TOP_TRACKS_ENDPOINT.format(id=artist_id)
    myparams = {'country': country}
    resp = requests.get(url, params=myparams)
    return resp.json()

# https://developer.spotify.com/web-api/get-artist/
def get_artist(artist_id):
    url = GET_ARTIST_ENDPOINT.format(id=artist_id)
    resp = requests.get(url)
    return resp.json()
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)