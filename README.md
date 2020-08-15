# Server_Rabbit_Pika
1. features.py generates features and labels from dataset and send it to quene.
2. model.py reads features from quene and predict label using linear regression model from bynary pikle. Then it send to new quene this prediction.
3. metric.py reads true and prediction labels to the lists (which grows up step by step) and calculate error. 
