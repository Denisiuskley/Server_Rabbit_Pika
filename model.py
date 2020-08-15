import pika
import pickle
import numpy as np
import json

with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

# Подключимся к серверу:    
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Укажем, с какой очередью будем работать:
channel.queue_declare(queue='Features')
channel.queue_declare(queue='y_predict')

# Напишем функцию, определяющую, как работать с полученным сообщением:
def callback(ch, method, properties, body):
    print(f'Из очереди {method.routing_key} получено значение {body}')
    y_pred = regressor.predict(np.array(json.loads(body)[1]).reshape(1, -1))
    channel.basic_publish(exchange='',
                      routing_key='y_predict',
                      body=json.dumps([json.loads(body)[0], y_pred[0]]))

# Зададим правила чтения из очереди, указанной в параметре queue:
# on_message_callback показывает какую функцию вызвать при получении сообщения
channel.basic_consume(
    queue='Features', on_message_callback=callback, auto_ack=True)
print('...Ожидание сообщений, для выхода нажмите CTRL+C')

# Запустим чтение очереди. Скрипт будет работать до принудительной остановки: так мы не пропустим ни одного сообщения.
channel.start_consuming()
