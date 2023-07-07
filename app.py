from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import pika

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

# Conexión RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaración de colas
queues = ['robin', 'mauro', 'vero', 'andres', 'cristian', 'samuel']

for queue_name in queues:
    channel.queue_declare(queue=queue_name)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Evento de conexión de SocketIO
@socketio.on('connect')
def connect():
    emit('connected', {'message': 'Connected'})

# Evento de desconexión de SocketIO
@socketio.on('disconnect')
def disconnect():
    emit('disconnected', {'message': 'Disconnected'})

# Evento de envío de mensaje
@socketio.on('send_message')
def send_message(data):
    message = data['message']
    queue_name = data['queue']
    print(f'{queue_name}->{message}')
    # Publicar mensaje en todas las colas, excepto la correspondiente al ID del cliente
    for queue in queues:
        if queue != queue_name:
            channel.basic_publish(exchange='', routing_key=queue, body=message)

# # Función de consumo de mensajes
# def consume_messages(queue_name):
#     def callback(ch, method, properties, body):
#         with app.app_context():
#             socketio.emit('new_message', {'message': body.decode(), 'queue': queue_name})

#     channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
#     try:
#         channel.start_consuming()
#     except KeyboardInterrupt:
#         channel.stop_consuming()

# Evento de conexión de SocketIO
@socketio.on('consume')
def consume(data):
    print("Llamado a funcion para consumo")
    sender = data['sender']
    "Aqui se mandaria a llamar a la funcion de consumo pasando el emisor"


if __name__ == '__main__':

    socketio.run(app, debug = True)
