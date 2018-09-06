from message import *

def route(session, request):
    session.send_message(Response(ServerSender(), str(request.body)))