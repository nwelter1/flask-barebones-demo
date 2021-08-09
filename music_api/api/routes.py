from flask import Blueprint, jsonify, request, url_for
from music_api.helpers import token_required
from music_api.models import Song, song_schema, songs_schema, db


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/tester')
def getrando():
    return {'CodingTemple': 'Rules'}

@api.route('/songs', methods = ['POST'])
@token_required
def create_song(current_user_token):
    name = request.json['name']
    duration = request.json['duration']
    genre = request.json['genre']
    bpm = request.json['bpm']
    key = request.json['key']
    user_token = current_user_token.token

    song = Song(name, duration, genre, bpm, key, user_token=user_token)

    db.session.add(song)
    db.session.commit()

    response = song_schema.dump(song)
    return jsonify(response)

@api.route('/songs', methods = ['GET'])
@token_required
def get_songs(current_user_token):
    owner = current_user_token.token
    songs = Song.query.filter_by(user_token = owner).all()
    response = songs_schema.dump(songs)
    return jsonify(response)

@api.route('/songs/<id>', methods = ['GET'])
@token_required
def get_song(current_user_token, id):
    song = Song.query.get(id)
    if song:
        response = song_schema.dump(song)
        return jsonify(response)
    else:
        return jsonify({'message':"That song does not exist pal..."})


@api.route('/songs/<id>', methods = ['POST'])
@token_required
def update_song(current_user_token, id):
    song = Song.query.get(id)
    if song:
        song.name = request.json['name']
        song.duration = request.json['duration']
        song.genre = request.json['genre']
        song.bpm = request.json['bpm']
        song.key = request.json['key']
        song.user_token = current_user_token.token

        db.session.commit()

        response = song_schema.dump(song)
        return jsonify(response)
    else:
        jsonify({'message': 'That song does not exist pal...'})

@api.route('/songs/<id>', methods = ['DELETE'])
@token_required
def delete_song(current_user_token, id):
    song = Song.query.get(id)
    if song:
        db.session.delete(song)
        db.session.commit()
        response = song_schema.dump(song)
        return jsonify(response)
    else:
        return jsonify({'message':"That song does not exist pal..."})
