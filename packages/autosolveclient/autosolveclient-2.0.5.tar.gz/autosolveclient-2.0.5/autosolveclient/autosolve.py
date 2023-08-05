import pika, requests, threading, json, time
from logzero import logger
from pymitter import EventEmitter
from autosolveclient.autosolveconstants import AutoSolveConstants
from autosolveclient.autosolve_errors import AutoSolveConnectionError


class Instance:
    auto_solve = None


class AutoSolve:

    def __init__(self, params):
        self.params = params

    def get_instance(self):
        if Instance.auto_solve is None:
            Instance.auto_solve = InternalAutoSolve(self.params)
            return Instance.auto_solve
        else:
            return Instance.auto_solve


class InternalAutoSolve:

    def __init__(self, params):
        self.autosolve_constants = AutoSolveConstants()
        self.emitter = EventEmitter()
        self.vhost = self.autosolve_constants.VHOST

        self.access_token = params["access_token"]
        self.api_key = params["api_key"]
        self.client_key = params["client_key"]
        self.debug = params["debug"]
        self.should_alert_on_cancel = params["should_alert_on_cancel"]
        self.queue = []

        self.routing_key = ""
        self.send_routing_key = ""
        self.account_id = ""
        self.directExchangeName = ""
        self.fanoutExchangeName = ""
        self.receiver_queue_name = ""
        self.routing_key_receiver = ""
        self.routing_key_cancel = ""
        self.token_send_routing_key = ""
        self.cancel_send_routing_key = ""

        self.delay = None
        self.attempts = None
        self.connection = None
        self.channel = None
        self.cancel_channel = None
        self.consumer_thread = None
        self.ready = False
        self.connected = False

    def initialized(self):
        while self.attempts < self.autosolve_constants.MAX_ATTEMPTS:
            time.sleep(.5)
            if self.ready:
                time.sleep(.5)
                break
        return self.ready

    def init(self, access_token=None, api_key=None):
        self.attempts = 0
        self.delay = self.autosolve_constants.RETRY_DELAY
        self.connection = None
        self.channel = None
        self.cancel_channel = None
        self.consumer_thread = None
        self.ready = False
        self.connected = False

        if access_token is not None and api_key is not None:
            self.reset_credentials(access_token, api_key)

        self.set_routing_objects()
        self.begin_connection()

    def set_routing_objects(self):
        self.routing_key = self.api_key.replace("-", "")
        self.send_routing_key = self.access_token.replace("-", "")

        self.account_id = self.access_token.split("-")[0]

        self.directExchangeName = self.build_with_account_id(self.autosolve_constants.DIRECT_EXCHANGE)
        self.fanoutExchangeName = self.build_with_account_id(self.autosolve_constants.FANOUT_EXCHANGE)

        self.receiver_queue_name = self.build_prefix_with_credentials(self.autosolve_constants.RECEIVER_QUEUE_NAME)

        self.routing_key_receiver = self.build_prefix_with_credentials(self.autosolve_constants.TOKEN_RECEIVE_ROUTE)
        self.routing_key_cancel = self.build_prefix_with_credentials(self.autosolve_constants.CANCEL_RECEIVE_ROUTE)

        self.token_send_routing_key = self.build_with_access_token(self.autosolve_constants.TOKEN_SEND_ROUTE)
        self.cancel_send_routing_key = self.build_with_access_token(self.autosolve_constants.CANCEL_SEND_ROUTE)

    def reset_credentials(self, access_token, api_key):
        self.close_connection()
        self.access_token = access_token
        self.api_key = api_key

    def begin_connection(self):
        if self.check_input_values():
            self.close_connection()
            status_code = self.validate_connection()
            if status_code == 200:
                self.log("Validation complete", self.autosolve_constants.SUCCESS)
                self.consumer_thread = threading.Thread(target=self.connect)
                self.consumer_thread.start()
            elif status_code == 400:
                self.log(self.autosolve_constants.INVALID_CLIENT_KEY, self.autosolve_constants.ERROR)
                raise AuthException(self.autosolve_constants.INVALID_CLIENT_KEY)
            elif status_code == 429:
                self.log(self.autosolve_constants.TOO_MANY_REQUESTS, self.autosolve_constants.ERROR)
                raise AuthException(self.autosolve_constants.TOO_MANY_REQUESTS)
            else:
                self.log(self.autosolve_constants.INVALID_API_KEY_OR_ACCESS_TOKEN, self.autosolve_constants.ERROR)
                raise AuthException(self.autosolve_constants.INVALID_API_KEY_OR_ACCESS_TOKEN)
        else:
            raise AuthException(self.autosolve_constants.INVALID_API_KEY_OR_ACCESS_TOKEN)

    def connect(self):
        self.log("Beginning connection establishment", self.autosolve_constants.STATUS)
        sleep_time = self.get_delay(self.delay)
        self.delay += 1
        if sleep_time > 0:
            time.sleep(sleep_time)

        credentials = pika.PlainCredentials(self.account_id, self.access_token)
        parameters = pika.ConnectionParameters(host=self.autosolve_constants.HOSTNAME,
                                               port=5672,
                                               virtual_host=self.vhost,
                                               credentials=credentials,
                                               connection_attempts=10,
                                               retry_delay=5,
                                               blocked_connection_timeout=60)
        try:
            self.connected = self.establish_connection(parameters) \
                             and self.create_channels() \
                             and self.register_response_queue()

            if self.connected:

                self.log("Beginning message consumption", self.autosolve_constants.SUCCESS)
                self.delay = 0
                self.ready = True
                self.channel.start_consuming()
                self.log("Stopped Message Consuming", self.autosolve_constants.SUCCESS)
                self.emitter.emit(self.autosolve_constants.ERROR_EVENT, AutoSolveConnectionError.CONNECTION_CLOSED_UNEXPECTEDLY)
            else:
                self.log("Error with RabbitMQ connection, attempting to re-establish", self.autosolve_constants.WARNING)
                self.handle_connection_error()

        except pika.exceptions.AMQPConnectionError or pika.exceptions.ConnectionClosedByBroker:
            self.log("Error with RabbitMQ connection, attempting to re-establish", self.autosolve_constants.WARNING)
            self.emitter.emit(self.autosolve_constants.ERROR_EVENT, AutoSolveConnectionError.CONNECTION_ERROR_INIT)
            self.handle_connection_error()

        except Exception:
            self.log("Unknown error occurred during connection.", self.autosolve_constants.ERROR)
            self.emitter.emit(self.autosolve_constants.ERROR_EVENT, AutoSolveConnectionError.CONNECTION_ERROR_INIT)
            self.handle_connection_error()

    def close_connection(self):
        self.log("Closing Connection", self.autosolve_constants.STATUS)
        if self.connection is not None and self.connection.is_open:
            self.connection.close()
        else:
            self.log("Connection does not exist", self.autosolve_constants.STATUS)

    def establish_connection(self, parameters):
        self.log("Attempting connection establishment", self.autosolve_constants.STATUS)

        try:
            self.connection = pika.BlockingConnection(parameters)
        except Exception:
            self.log("Connection Exception", self.autosolve_constants.ERROR)

        self.log("Connection established", self.autosolve_constants.SUCCESS)
        return True

    def create_channels(self):
        self.log("Creating channel", self.autosolve_constants.STATUS)
        self.channel = self.connection.channel()
        self.cancel_channel = self.connection.channel()

        self.log("Channels created", self.autosolve_constants.SUCCESS)
        return True

    def register_response_queue(self):
        try:
            self.log("Binding queue to exchange", self.autosolve_constants.STATUS)
            self.channel.queue_bind(queue=self.receiver_queue_name,
                                    exchange=self.directExchangeName,
                                    routing_key=self.routing_key_receiver)
            self.channel.queue_bind(queue=self.receiver_queue_name,
                                    exchange=self.directExchangeName,
                                    routing_key=self.routing_key_cancel)
            self.log("Queue binded to exchange " + self.directExchangeName,
                     self.autosolve_constants.SUCCESS)
            self.channel.basic_consume(queue=self.receiver_queue_name, auto_ack=self.autosolve_constants.AUTO_ACK,
                                       on_message_callback=self.receive_message)
            return True
        except pika.exceptions.ChannelClosedByBroker:
            self.emitter.emit(self.autosolve_constants.ERROR_EVENT, AutoSolveConnectionError.CONNECTION_ERROR_INIT)

    def receive_message(self, channel, method_frame, header_frame, body):
        if method_frame.routing_key == self.routing_key_receiver:
            self.on_receiver_message(channel, method_frame, header_frame, body)
        else:
            self.on_cancel_message(channel, method_frame, header_frame, body)

    def on_receiver_message(self, channel, method_frame, header_frame, body):
        json_string = "".join(chr(x) for x in body)
        self.log("Message Received: " + json_string, self.autosolve_constants.SUCCESS)
        self.emitter.emit(self.autosolve_constants.RESPONSE_EVENT, json_string)

    def on_cancel_message(self, channel, method_frame, header_frame, body):
        json_string = "".join(chr(x) for x in body)
        self.log("Message Received: " + json_string, self.autosolve_constants.SUCCESS)
        self.emitter.emit(self.autosolve_constants.CANCEL_RESPONSE_EVENT, json_string)

    def handle_connection_error(self):
        self.connected = False
        self.attempts += 1

        self.log("Handling reconnect", self.autosolve_constants.STATUS)
        try:
            self.begin_connection()
        except Exception as ex:
            print(ex)

        if self.connected:
            self.log("Connection attempt successful, sending any unsent messages", self.autosolve_constants.SUCCESS)
            self.attempt_message_backlog_send()
        else:
            self.log("Connection attempts unsuccessful", self.autosolve_constants.ERROR)
            self.emitter.emit(self.autosolve_constants.ERROR_EVENT, AutoSolveConnectionError.CONNECTION_REESTABLISH_FAILED)

    def send(self):
        req = None
        try:
            req = self.queue.pop()
            if req is not None:
                message = req["message"]
                route = req["route"]
                exchange = req["exchange"]
                message["createdAt"] = round(time.time())
                message["apiKey"] = self.api_key
                message_string = json.dumps(message)
                byte_string = message_string.encode()
                if self.fanoutExchangeName == exchange:
                    return self.cancel_channel.basic_publish(exchange=exchange,
                                                    routing_key=route,
                                                    body=byte_string)

                return self.channel.basic_publish(exchange=exchange,
                                                  routing_key=route,
                                                  body=byte_string)
        except Exception as e:
            print(e)
            if req is not None:
                self.queue.append(req)

    def send_token_request(self, message):
        self.log("Sending request message for task: " + str(message['taskId']), self.autosolve_constants.STATUS)
        try:
            self.queue.append({"message": message, "route": self.token_send_routing_key, "exchange": self.directExchangeName})
            send_result = self.connection.add_callback_threadsafe(self.send)
            if send_result is None:
                self.log("Message with TaskId: " + str(message['taskId']) + " sent successfully",
                         self.autosolve_constants.SUCCESS)
        except Exception as e:
            self.log(e, self.autosolve_constants.WARNING)
            self.resend(message, self.token_send_routing_key, self.directExchangeName)

    def cancel_token_request(self, taskId):
        message = dict()
        message["taskId"] = taskId
        message["responseRequired"] = self.should_alert_on_cancel

        self.log("Sending cancel message for task: " + message['taskId'], self.autosolve_constants.STATUS)
        try:
            self.queue.append({"message": message, "route": self.cancel_send_routing_key, "exchange": self.fanoutExchangeName})
            send_result = self.connection.add_callback_threadsafe(self.send)
            if send_result is None:
                self.log("Cancel message with TaskId: " + message['taskId'] + " sent successfully",
                         self.autosolve_constants.SUCCESS)
        except Exception as e:
            self.log(e, self.autosolve_constants.WARNING)
            self.resend(message, self.cancel_send_routing_key, self.fanoutExchangeName)

    def cancel_all_requests(self):
        message = {"apiKey": self.api_key}
        self.log("Sending cancel all request for api key ::  " + message['apiKey'], self.autosolve_constants.STATUS)
        try:
            self.queue.append(
                {"message": message, "route": self.cancel_send_routing_key, "exchange": self.fanoutExchangeName})
            send_result = self.connection.add_callback_threadsafe(self.send)
            if send_result is None:
                self.log("Cancel all requests sent successfully", self.autosolve_constants.SUCCESS)
        except Exception as e:
            self.log(e, self.autosolve_constants.WARNING)
            self.resend(message, self.cancel_send_routing_key, self.fanoutExchangeName)

    def resend(self, message, route, exchange):
        time.sleep(5)
        result = self.connection.add_callback_threadsafe(self.send)
        if result is None:
            self.log("Resend attempt successful", self.autosolve_constants.SUCCESS)
        else:
            self.log("Attempt to resend after wait unsuccessful. Pushing message to backlog",
                     self.autosolve_constants.WARNING)
            self.add_message_to_backlog({"message": message, "route": route, "exchange": exchange})

    def add_message_to_backlog(self, message):
        self.queue.append(message)

    def attempt_message_backlog_send(self):
        self.log("Sending messages from backlog", self.autosolve_constants.STATUS)
        for message in self.queue:
            self.log("Backlog message sending: " + str(message["message"]["taskId"]), self.autosolve_constants.STATUS)
            result = self.connection.add_callback_threadsafe(self.send)
            if result is not None:
                self.log("Backlog resend unsuccessful for message: " + str(message["message"]["taskId"]), self.autosolve_constants.STATUS)

    ## VALIDATION FUNCTIONS ##

    def check_input_values(self):
        if self.validate_inputs():
            return True
        else:
            self.log(self.autosolve_constants.INPUT_VALUE_ERROR, self.autosolve_constants.ERROR)
            raise InputValueException(self.autosolve_constants.INPUT_VALUE_ERROR)

    def validate_inputs(self):
        valid_access_token = self.validate_access_token()
        valid_client_key = self.client_key is not None
        valid_api_key = self.api_key is not None

        return valid_access_token and valid_client_key and valid_api_key

    def validate_access_token(self):
        if self.access_token is None:
            return False

        access_token_split = self.access_token.split("-")
        username_valid = access_token_split[0].isdigit()

        if username_valid is not True:
            return False

        return True

    def validate_connection(self):
        self.log("Validating input values with AutoSolve API", self.autosolve_constants.STATUS)
        url = "https://dash.autosolve.io/rest/" + self.access_token + "/verify/" + self.api_key + "?clientId=" + self.client_key
        response = requests.get(url)
        return response.status_code

    def build_prefix_with_credentials(self, prefix):
        return prefix + "." + self.account_id + "." + self.routing_key

    def build_with_access_token(self, prefix):
        return prefix + "." + self.send_routing_key

    def build_with_account_id(self, prefix):
        return prefix + "." + self.account_id

    def get_delay(self, n):
        if n < len(self.autosolve_constants.SEQUENCE):
            return self.autosolve_constants.SEQUENCE[n]
        else:
            return self.autosolve_constants.SEQUENCE[len(self.autosolve_constants.SEQUENCE) - 1]

    def log(self, message, type):
        if self.debug:
            if type == self.autosolve_constants.ERROR:
                logger.error(message)
            if type == self.autosolve_constants.WARNING:
                logger.warning(message)
            if type == self.autosolve_constants.STATUS:
                logger.debug(message)
            if type == self.autosolve_constants.SUCCESS:
                logger.info(message)


class AuthException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'AuthException: {}'.format(self.value)


class InputValueException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'InputValueException: {}'.format(self.value)


