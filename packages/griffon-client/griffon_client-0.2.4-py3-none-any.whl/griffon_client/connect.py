import socketio
import json
import threading
from urllib.parse import urlencode


#************************************************************************
#* Private Functions
#***********************************************************************/

def normalize_consumer(consumer):

    if consumer is None:
        return {'or': []}

    elif isinstance(consumer, str):

        return {'or': [consumer]}

    elif isinstance(consumer, list):

        return {'or': consumer}

    else:
        return consumer

def normalize_array(producer):

    if producer is None:
        return []

    elif not isinstance(producer, list):
        return [producer]

    else:
        return producer


#************************************************************************
#* Public Functions
#***********************************************************************/


class Client():


    def __init__(self, uri=None, username=None, password=None, task=None, environment='default', consume=None, produce=None, channels=['default'], gather=False):
        
        self.channels=channels

        print(f'connecting to server at {uri}')


        consume = normalize_array(consume)

        self.consumers = {}

        self.gatherer = None

        config = {}

        config['and' if gather is True else 'or'] = consume

        consume = config

        query = json.dumps({
            'username': username,
            'password': password,
            'operator': task,
            'environment': environment,
            'consume': normalize_consumer(consume),
            'produce': normalize_array(produce),
            'channels': normalize_array(channels),
        })



        self.socket = socketio.Client()


        @self.socket.on('connect')
        def on_connect():
            print('Successfully connected.')


        class task():
            def __init__(self, socket, topic, topics, data, payload):
                self.payload = payload
                self.data = data
                self.topics = topics
                self.topic = topic
                self.socket = socket


            def produce(self, topic=None, data=None):

                if topic is None:
                    raise Exception('Producers must include a topic.')
                if data is None:
                    raise Exception("'data', must not be 'None'.")

                production_payload = {
                    'completed_task_id': self.payload['task_id'],
                    'topic': topic,
                    'stream_id': self.payload['stream_id'],
                    'channel': self.payload['channel'],
                    'data': data,
                }

                print(f'Producing Topic: {topic}')

                self.socket.emit('production', production_payload)




        @self.socket.on('consumption')
        def consumption(payload):


            def execute_task(self, payload):
                if self.gatherer is not None:

                    print(f'Consuming Topics: {payload["topics"]}')

                    self.gatherer(task(self.socket, None, payload['topics'], payload['data'], payload))
                
                else:

                    for topic in payload['topics']:


                        consumer = None

                        if topic in self.consumers:
                            consumer = self.consumers[topic]

                        elif '*' in self.consumers:
                            consumer = self.consumers['*']
                        
                        if consumer is not None:

                            print(f'Consuming Topic: {topic}')

                            consumer(task(self.socket, topic, payload['topics'], payload['data'][topic], payload))

                        else:
                            raise Exception("No consumer found for registerd topic.")


            t = threading.Thread(target=execute_task, args=[self, payload])
            t.setDaemon(False)
            t.start()

            return {'code': 200}



        @self.socket.on('error')
        def on_error(error):
            print(error)

        @self.socket.on('info')
        def on_info(info):
            print(info)

        self.socket.connect(f'{uri}?init={query}')

        self.socket.sleep(3)


    def consume(self, topics):

        def register_consumers(func):

            nonlocal topics

            topics = normalize_array(topics)

            for topic in topics:

                if topic in self.consumers or '*' in self.consumers:
                    raise Exception(f'Consumer for topic {topic} has already been registered.')

                self.consumers[topic] = func

        if callable(topics):
            func = topics
            topics = ['*']
            register_consumers(func)

        else:
            return register_consumers




    def gather(self, func):

        if len(self.consumers.keys()) > 0:
            raise Exception(f'Gather listens for all topics and can not be used with consume.')
        
        self.gatherer = func


    def produce(self, topic=None, channel=None, data=None):

        if channel is None and len(self.channels) == 1 and self.channels[0] == 'default':
            channel = 'default'

        if topic is None:
            raise Exception('Producers must include a topic.')
        if channel is None:
            raise Exception('Raw production must include a channel.')
        if data is None:
            raise Exception("'data', must not be 'None'.")

        print(f'Producing Topic: {topic}')

        self.socket.emit('production', {
            'topic': topic,
            'channel': channel,
            'data': data,
        })



