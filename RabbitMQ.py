
import os
import pika
from LoggerUtil import LoggerUtil
from FileUtil import getConfig

class RabbitMQUtil(object):
    '''
    RabbitMQUtil is used to connect the rabbitmq, publish and consume the message.
    '''
    
    def __init__(self, log_obj = None, channel_id = '', exchange = '', exchange_type = 'direct', queue_name = ''):
        '''
        The constructor of class RabbitMQUtil.
        @param exchange: the name of exchange
        @param exchange_type: the type of exchange(direct, fanout, topic)
        '''
        
        if log_obj:
            self.log_obj = log_obj
        else:
            self.log_obj = LoggerUtil(os.path.join(os.path.dirname(__file__), 'log.txt')).getLogger()
            
        conf_dict = getConfig(os.path.join(os.path.dirname(__file__), 'common.conf'))
        
        if conf_dict:
            self.host = conf_dict['rabbitmq']['host']
            self.port = int(conf_dict['rabbitmq']['port']) if len(conf_dict['rabbitmq']['port']) > 0 else 5672
            self.user = conf_dict['rabbitmq']['user']
            self.password = conf_dict['rabbitmq']['password']
            self.vhost = conf_dict['rabbitmq']['vhost']
            
            self.exchange = exchange
            self.type = exchange_type
            self.channel_id = channel_id
            self.queue_name = queue_name
            
        self.connect()
    
    def connect(self):
        '''
        Create connection with rabbitmq server.
        The process is as following: first create a connect object, then create channel, at last declare exchange and queue
        '''
        
        try:
            credentials = pika.PlainCredentials(self.user, self.password)
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, 
                                                                           port=self.port, 
                                                                           virtual_host=self.vhost, 
                                                                           credentials=credentials))
            self.channel = self.connection.channel(channel_number = self.channel_id)
            
            #durable is used to sign that the message store persistencely
            if self.exchange != '':
                self.channel.exchange_declare(exchange=self.exchange, type=self.type, durable = True, auto_delete=False)
        except Exception, e:
            self.log_obj.error('Connect rabbitmq server exception:%s' % e)
    
    def publish(self, routing_key = '', message = ''):
        '''
        Proucer publish a message to rabbitmq server.
        @param routing_key: the routing key is used to send a message to a specific queue when the type is not fanout
        @param message: the content want to send
        '''
        
        self.channel.basic_publish(exchange=self.exchange, 
                                   routing_key=routing_key, 
                                   body=message,
                                   properties=pika.BasicProperties(delivery_mode = 2,),)    # make message persistent
    
    def consume(self, callback, routing_key = '', tag = ''):
        '''
        Consumer get a message from rabbitmq server, it is a daemon process.
        @param callback: the callback function is excuted after getting a message
        @param routing_key: the routing key is used to get a message from a specific queue when the type is not fanout
        @param tag: the tag is used to acknowledge getting the message
        '''
        
        self.channel.queue_declare(queue=self.queue_name, durable=True, exclusive=False, auto_delete=False)
        
        if self.exchange != '':
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name, routing_key=routing_key)
            
        self.channel.basic_qos(prefetch_count=1)            #Fair dispatch
        self.channel.basic_consume(callback, queue=self.queue_name, consumer_tag=tag, no_ack=False)
        self.channel.start_consuming()
    
    def close(self):
        '''
        Close the connection with rabbitmq server.
        '''
        
        if self.connection:
            self.connection.close()
    
if __name__ == '__main__':
    pass