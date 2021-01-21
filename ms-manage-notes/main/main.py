from flask import Flask, request, Response
from main.controllers.note_controller import NoteController
from main.util.config import Config
from main.log.log import logger
import json

app = Flask(__name__)
config = Config()
note = NoteController(config)

@app.route('/')
def running():
    return "Temp Notes - Running"

@app.route('/ms/temp-notes/<username>/create', methods=['POST'])
def insert(username):
    try:
        if request.is_json:
            payload = request.get_json()
            result = note.insert(username=username, payload=payload)
            if result:
                return Response(json.dumps(result), mimetype='application/json')
            return Response(json.dumps({}),status=500, mimetype='application/json')
        return {}, 500
    except Exception as e:
        print(e)
        logger.error('insert', e)
        return {}, 500

@app.route('/ms/temp-notes/<username>/<noteId>/get', methods=['GET'])
def get(username, noteId):
    try:
        result = note.get(username=username, noteId=noteId)
        return (result, 200) if result else ({}, 204)
    except Exception as e:
        print(e)
        logger.error('get', e)
        return {}, 500

@app.route('/ms/temp-notes/<username>/get-all', methods=['GET'])
def get_all(username):
    try:
        result = note.get_all(username=username)
        if result and len(result) > 0:
            return Response(json.dumps(result), mimetype='application/json')
        return Response(json.dumps({}),status=204, mimetype='application/json')
    except Exception as e:
        print(e)
        logger.error('get_all', e)
        return {}, 500

@app.route('/ms/temp-notes/<username>/<noteId>/update', methods=['PUT'])
def update(username, noteId):
    try:
        if request.is_json:
            payload = request.get_json()
            result = note.update(username=username, noteId=noteId, payload=payload)
            if result:
                return Response(json.dumps(result), status=200, mimetype='application/json')
            return Response(json.dumps({}),status=204, mimetype='application/json')
        return {}, 500
    except Exception as e:
        print(e)
        logger.error('update', e)
        return {}, 500

@app.route('/ms/temp-notes/<username>/<noteId>/delete', methods=['DELETE'])
def delete(username, noteId):
    try:
        result = note.delete(username=username, noteId=noteId)
        if result and result > 0:
            return Response(json.dumps({'result' : result}), status=200, mimetype='application/json')
        return Response(json.dumps({}),status=204, mimetype='application/json')
    except Exception as e:
        print(e)
        logger.error('delete', e)
        return {}, 500

@app.after_request
def after_request(response):
    response.headers.add(['Access-Control-Allow-Origin'], '*')
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

