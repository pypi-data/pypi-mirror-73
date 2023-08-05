import ssl
import threading
import logging
try:
    import thread
except ImportError:
    import _thread as thread
import time
import queue
from threading import Condition
import websocket
from enum import Enum

DEBUG = True

k_condition = Condition()
k_queue = []
k_health_queue = queue.Queue()
k_current_model = None
k_thread_run = True
k_process_completed = "__PROCESS_COMPLETED__"
k_health_message = "__HEALTH_CHECK_STATUS_OK__"
k_error_message = "__ERROR_MESSAGE__"
k_info_message = "__INFO_MESSAGE__"


class ServerConnectionStatus(Enum):
    Alive = 1
    Unsure = 2
    NotReachable = 3


k_server_is_alive = ServerConnectionStatus.NotReachable


def on_message(ws, message):
    global k_current_model
    global k_queue
    global k_condition
    global k_health_queue
    if isinstance(message, str) and message.startswith(k_health_message):
        k_health_queue.put(message)
    elif isinstance(message, str) and message.startswith(k_error_message):
        logging.info(message)
        print("Received an error message from the back-end server, return")
        return
    elif isinstance(message, str) and message.startswith(k_info_message):
        logging.info(message)
        print(message)
    else:
        if k_current_model is None:
            msg = "The model is not set, return"
            logging.info(msg)
            print(msg)
            return

        if isinstance(message, str) and message.startswith(k_process_completed):
            k_condition.acquire()

            # Append the message to the queue
            k_queue.append(message)
            k_condition.notify()
            k_condition.release()
        else:
            # Proceed in parsing the protobuf message
            k_current_model.on_message(message)


def on_error(ws, error):
    logging.error(error)


def on_close(ws):
    msg = "### Connection closed ###"
    logging.info(msg)


def on_open(ws):
    logging.info("Client connected to back-end server")


class HealthMonitorThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, daemon=True)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        global k_thread_run
        global k_health_queue
        global k_server_is_alive

        time.sleep(1)
        while k_thread_run:
            try:
                k_health_queue.get(block=True, timeout=1)
                if DEBUG:
                    print("ALIVE CONNECTION")
                k_server_is_alive = ServerConnectionStatus.Alive
            except:
                if k_server_is_alive is ServerConnectionStatus.Alive:
                    if DEBUG:
                        print("UNSURE CONNECTION")
                    k_server_is_alive = ServerConnectionStatus.Unsure
                else:
                    if DEBUG:
                        print("NO CONNECTION")
                    k_server_is_alive = ServerConnectionStatus.NotReachable

            # Wait for next read
            time.sleep(2)


class FrontendClientRunner:
    address = ""
    port = 0
    web_socket = None
    ws_url = ""

    def __init__(self, address, port):
        # web_socket.enableTrace(True)

        self.address = address
        self.port = port

        self.init_runner()

    def init_runner(self):
        self.ws_url = "ws://" + self.address + \
                      ":" + str(self.port) + "/proto_service"

    def is_online(self):
        global k_server_is_alive
        return k_server_is_alive is ServerConnectionStatus.Alive

    def connect_to_server(self):
        logging.info("Connecting to back-end server...")
        header = {
            'Sec-WebSocket-Protocol': 'graphql-subscriptions'
        }
        try:
            self.web_socket = websocket.WebSocketApp(self.ws_url,
                                                     header=header,
                                                     on_message=on_message,
                                                     on_error=on_error,
                                                     on_close=on_close)
            self.web_socket.on_open = on_open

            # self.web_socket.run_forever()
            th = threading.Thread(
                target=self.connect_to_server_impl, args=(self.web_socket, ), daemon=True)
            th.start()

            # Start the health thread
            health_th = HealthMonitorThread(name="Health_Thread")
            health_th.start()

        except Exception as e:
            logging.exception(e)
            logging.error("Cannot connect to the back-end server, return")
            return False

        global k_server_is_alive
        k_server_is_alive = ServerConnectionStatus.Alive
        return True

    def connect_to_server_impl(self, wb_socket):
        # , sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY),)
        wb_socket.run_forever(
            sslopt={
                "cert_reqs": ssl.CERT_NONE,
                "check_hostname": False})

    def disconnect_from_server(self):
        # Initiate closing protocol with server
        if not self.web_socket or not self.web_socket.sock:
            return
        self.web_socket.sock.send("__CLIENT_LOG_OFF__")

        global k_thread_run
        k_thread_run = False

        # Wait to logoff from server
        time.sleep(1)
        try:
            self.web_socket.sock.close()
        except Exception as e:
            logging.exception(e)
            logging.info("Connection close and exception threw")
        finally:
            if DEBUG:
                print("### Connection closed ###")

    def send_message_to_backend_server(self, model):
        if self.web_socket is None:
            logging.error("Client not connected to back-end server, return")
            return False

        # Set the current global model and send the request to the back-end
        global k_current_model
        k_current_model = model
        sent = self.web_socket.sock.send_binary(model.serialize())
        return sent

    def get_message_from_backend_server(self):
        global k_queue
        global k_condition
        k_condition.acquire()
        if not k_queue:
            k_condition.wait()
        msg = k_queue.pop(0)
        k_condition.notify()
        k_condition.release()
        return msg

    def wait_on_process_completion(self):
        msg = ""
        while msg != k_process_completed:
            msg = self.get_message_from_backend_server()

        # Give time for connections to close-up
        time.sleep(1)
