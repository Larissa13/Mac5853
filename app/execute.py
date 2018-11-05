from gevent import monkey
import zmq.green as zmq
from app import app

if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    ZMQ_LISTENING_PORT = 6557
    
    context = zmq.Context()
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

