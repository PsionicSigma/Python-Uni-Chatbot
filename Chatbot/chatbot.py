#main file

#imports
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, join_room, leave_room, send, emit

from mdl_dialog import process_input

chatBotApp = Flask(__name__)
chatBotApp.config['SECRET_KEY'] = 'vilniustech2020'
chatBotAppSIO = SocketIO(chatBotApp)
adm_room = 'adm_chat_room'

@chatBotApp.route("/")
def index():
    return render_template("index.html")

@chatBotApp.route("/usr")
def user_page():
    return render_template("end_ui.html")

@chatBotApp.route("/adm")
def adm_page():
    return render_template("adm_ui.html")

#will be pointless
@chatBotApp.route("/usr/get")
def get_bot_response():
    end_user_query = request.args.get('msg')
    response = process_input(end_user_query)
    return str(response)

@chatBotAppSIO.on('user_connected', namespace='/usr')
def get_bot_response(room_code, methods = ['GET', 'POST']):
    join_room(room_code)

@chatBotAppSIO.on('ask_bot', namespace='/usr')
def get_bot_response(message, room_code, methods = ['GET', 'POST']):
    end_user_query = message
    print(message)
    response = process_input(end_user_query)
    emit('bot_respond', response, room = room_code)

#kind of useless?
@chatBotAppSIO.on('redirect_to_helpdesk', namespace='/usr')
def redirect_user(stat, methods = ['GET', 'POST']):
    print('user redirected')
    return redirect("https://pagalba.vgtu.lt/")

@chatBotAppSIO.on('user_join', namespace='/usr')
def user_connect(stat, usr_name, room_code, methods = ['GET', 'POST']):
    print('user joined')
    leave_room(room_code)
    join_room(adm_room)
    emit('user_connected', usr_name, room = adm_room, namespace = '/adm')

@chatBotAppSIO.on('user_leave', namespace='/usr')
def user_disconnect(stat, usr_name, room_code, methods = ['GET', 'POST']):
    print('user left')
    leave_room(adm_room)
    emit('user_disconnected', usr_name, room = adm_room, namespace = '/adm')
    join_room(room_code)

@chatBotAppSIO.on('adm_join', namespace='/adm')
def adm_connect(stat, methods = ['GET', 'POST']):
    print('admin joined')
    join_room(adm_room)

@chatBotAppSIO.on('user_say', namespace='/usr')
def user_disconnect(message, methods = ['GET', 'POST']):
    emit('user_say', message, room = adm_room, namespace = '/adm')

@chatBotAppSIO.on('adm_say', namespace='/adm')
def user_disconnect(message, methods = ['GET', 'POST']):
    emit('adm_say', message, room = adm_room, namespace ='/usr')
    print('adm said '+message)

if __name__ == "__main__":
    chatBotAppSIO.run(chatBotApp, debug = True)

#flask
#flask_socketio
#eventlet
#numpy
#json
#nltk