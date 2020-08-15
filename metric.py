try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass

import pika
import json
from sklearn.metrics import mean_squared_error


class connect():
    def __init__(self):
        self.y_true = []
        self.y_predict = []
        self.m_tr = 0
        self.m_pr = 1
        self.y_tr = 0
        self.y_pr = 1
    def callback(self, ch, method, properties, body):
        if method.routing_key == 'y_true':
            self.y_tr = json.loads(body)[1]
            self.m_tr = json.loads(body)[0]
        if method.routing_key == 'y_predict':
            self.y_pr = json.loads(body)[1]
            self.m_pr = json.loads(body)[0]
        if self.m_tr == self.m_pr:
            self.y_true.append(self.y_tr)
            self.y_predict.append(self.y_pr)
            rmse = mean_squared_error(self.y_true, self.y_predict, squared = False)
            print(rmse)
    
    def connection_func(self):        
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        
        self.channel = connection.channel()
        
        self.channel.queue_declare(queue='y_true')
        self.channel.queue_declare(queue='y_predict')
        
        self.channel.basic_consume(
              queue='y_true', on_message_callback=self.callback, auto_ack=True)
        self.channel.basic_consume(
              queue='y_predict', on_message_callback=self.callback, auto_ack=True)
    def consume(self):
        print('...Ожидание сообщений, для выхода нажмите CTRL+C')        
        self.channel.start_consuming()
   
c = connect()
c.connection_func()
c.consume()
 

