from logging import StreamHandler
from kafka import KafkaProducer
import json
from datetime import datetime
import graphyte
import consul
from jsonformatter import JsonFormatter
from cloudevents.sdk.event import v03
import os
import logging

class ApplicationConfigurator():

    def get(self,config_key):
        config = {}
        try:
            c = consul.Consul(host=os.environ['CONSUL_HOST'], port=os.environ['CONSUL_PORT'])
            index = None
            index, data = c.kv.get(config_key, index=None)
            the_json = data['Value'].decode("utf-8")
            config = json.loads(the_json)
        except Exception as ex:
            print('Exception in getting key')
            print(ex)

        return config

class KafkaConfig(object):
    def __init__(self, kafka_brokers, json=False):
        self.json = json
        if not json:
            self.producer = KafkaProducer(
                bootstrap_servers=kafka_brokers
            )
        else:
            self.producer = KafkaProducer(
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                bootstrap_servers=kafka_brokers
            )
    def send(self, data, topic):
        if self.json:
            result = self.producer.send(topic, key=b'log', value=data)
        else:
            result = self.producer.send(topic, bytes(data, 'utf-8'))
        print("kafka send result: {}".format(result.get()))


class FerrisKafkaLoggingHandler(StreamHandler):

    def __init__(self,topic):
        StreamHandler.__init__(self)
        self.broker = os.environ['KAFKA_BOOTSTRAP_SERVER'] + ':' + os.environ['KAFKA_PORT']
        self.topic = topic
        # Kafka Broker Configuration
        self.kafka_broker = KafkaConfig(self.broker)
    def emit(self, record):
        msg = self.format(record)
        self.kafka_broker.send(msg, self.topic)


class MetricMessage(object):
    def __init__(self, metric_key, metric_value, update_time=None):
        self.metric_key = metric_key
        self.metric_value = metric_value
        if update_time == None:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            self.update_time = timestampStr
        else:
            self.update_time = update_time

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class MetricsAPI:

    def __init__(self):
        #print("in init")
        pass

    def send(self,metric_message:MetricMessage):
        try:
            graphyte.init(os.environ['GRAPHYTE_HOST'], prefix='ai.ferris')
            graphyte.send(metric_message.metric_key, metric_message.metric_value)
        except Exception as ex:
            print('Exception in publishing message')
            print(ex)
        pass


class CloudEventsAPI():

    def __init__(self, topic='ferris.cloudevents'):
        self.broker = os.environ['GRAPHYTE_HOST'] + ':' + os.environ['GRAPHYTE_HOST']
        self.topic = topic
        # Kafka Broker Configuration
        self.kafka_broker = KafkaConfig(broker)
    def send(self, event):
        s = json.dumps(event.Properties())
        self.kafka_broker.send(s, self.topic)
