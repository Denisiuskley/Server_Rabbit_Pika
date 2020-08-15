import numpy as np
from sklearn.datasets import load_diabetes
import pika
import json
import datetime
import time

# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

X, y = load_diabetes(return_X_y=True)

# Подключение к серверу на локальном хосте:
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создадим очередь, с которой будем работать:
channel.queue_declare(queue='Features')
channel.queue_declare(queue='y_true')

# Опубликуем сообщение
i = 0
while i == 0:
    random_row = np.random.randint(0, X.shape[0]-1)
    m = str(datetime.datetime.now()) 
    channel.basic_publish(exchange='',
                          routing_key='Features',
                          body=json.dumps([m, list(X[random_row, :])]))
    
    channel.basic_publish(exchange='',
                          routing_key='y_true',
                          body=json.dumps([m, y[random_row]]))
    print(f'Сообщение с правильным ответом, отправлено в очередь в {m}')
    time.sleep(5)
# Закроем подключение 
connection.close()
