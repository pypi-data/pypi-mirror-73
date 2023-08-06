import sys
import logging
import ctypes
import os
import signal
import pandas
import time
import json


class ZinnionAPI(object):
    def __init__(self):
        format = "%(asctime)s: %(message)s"
        self.mauro = 0
        logging.basicConfig(
            format=format, level=logging.INFO, datefmt="%H:%M:%S")

        logging.info("Python ZTrading    : Version: 0.0.21")

        logging.info("Python ZTrading    : Starting threads")

        if sys.platform == "linux" or sys.platform == "linux2":
            # linux
            logging.info("Python ZTrading    : Plataform: Linux")
        elif sys.platform == "darwin":
            # OS X
            logging.info("Python ZTrading    : Plataform: OS X")
            # sys.exit()
        elif sys.platform == "win32":
            # Windows...
            logging.info("Python ZTrading    : sys.platform not supported")
            sys.exit()

        if 'DEPLOYMENT_ID' not in os.environ:
            logging.info(
                "Python ZTrading    : DEPLOYMENT_ID : not set")
            sys.exit()

        if 'TOKEN' not in os.environ:
            logging.info("Python ZTrading    : TOKEN: not set")
            sys.exit()

        if 'ZTRADING_LIB' in os.environ:
            self.ztrading_lib = ctypes.cdll.LoadLibrary(
                os.environ['ZTRADING_LIB'])
        else:
            logging.error(
                "Python ZTrading    : Please export ZTRADING_LIB, for more details go to: https://github.com/Zinnion/zpytrading/wiki")
            sys.exit()

        if 'SIMULATION' in os.environ:
            self.simulation = os.environ.get('SIMULATION').lower() == 'true'
        else:
            self.simulation = False

        if 'DEBUG' in os.environ:
            self.debug = os.environ.get('DEBUG').lower() == 'true'
        else:
            self.debug = False

        logging.info("Python ZTrading    : API startup")
        self.ztrading_lib.init_ztrading.restype = ctypes.c_int
        if self.ztrading_lib.init_ztrading() == 1:
            os.kill(os.getpid(), signal.SIGUSR1)

    def add_streaming(self, streaming_config):
        self.ztrading_lib.add_streaming.restype = ctypes.c_bool
        if self.ztrading_lib.add_streaming(bytes(streaming_config, 'utf-8')) == False:
            os.kill(os.getpid(), signal.SIGUSR1)

    def add_indicators(self, indicators_config):
        self.ztrading_lib.add_indicators.restype = ctypes.c_bool
        if self.ztrading_lib.add_indicators(bytes(indicators_config, 'utf-8')) == False:
            os.kill(os.getpid(), signal.SIGUSR1)

    def send_order(self, order):
        self.ztrading_lib.order_send.restype = ctypes.c_char_p
        result = self.ztrading_lib.order_send(bytes(order, 'utf-8'))
        json_object = json.loads(result)
        return json.dumps(json_object, indent=2)

    def close_position(self, position):
        self.ztrading_lib.close_position.restype = ctypes.c_char_p
        result = self.ztrading_lib.close_position(bytes(position, 'utf-8'))
        json_object = json.loads(result)
        return json.dumps(json_object, indent=2)

    def modify_position(self, position):
        self.ztrading_lib.modify_position.restype = ctypes.c_char_p
        result = self.ztrading_lib.modify_position(bytes(position, 'utf-8'))
        json_object = json.loads(result)
        return json.dumps(json_object, indent=2)

    def cancel_order(self, order):
        # json_object = json.loads(order)
        # return json.dumps(json_object, indent=2)
        self.ztrading_lib.cancel_order.restype = ctypes.c_char_p
        result = self.ztrading_lib.cancel_order(bytes(order, 'utf-8'))
        json_object = json.loads(result)
        return json.dumps(json_object, indent=2)

    def get_orders(self, req):
        result = self.ztrading_lib.get_orders(bytes(req, 'utf-8'))
        json_object = json.loads(ctypes.c_char_p(result).value.decode("utf-8"))
        return json.dumps(json_object, indent=2)

    def get_positions(self, req):
        result = self.ztrading_lib.get_positions(bytes(req, 'utf-8'))
        json_object = json.loads(ctypes.c_char_p(result).value.decode("utf-8"))
        return json.dumps(json_object, indent=2)

    def get_deals(self, req):
        result = self.ztrading_lib.get_deals(bytes(req, 'utf-8'))
        json_object = json.loads(ctypes.c_char_p(result).value.decode("utf-8"))
        return json.dumps(json_object, indent=2)

    def hand_data(self, callback, json):
        callback(self, json)

    def start_streaming(self, callback):
        if self.simulation == True:
            logging.info("Python ZTrading    : SIMULATION MODE")
        while True:
            try:
                self.ztrading_lib.get_next_msg.restype = ctypes.c_char_p
                result = self.ztrading_lib.get_next_msg()
                json_object = json.loads(result)
                # json_formatted_str = json.dumps(json_object, indent=2)
                # Handle the data received
                if self.simulation == True:
                    if "comment" in json_object:
                        if json_object["comment"] == "Finished":
                            libdl = ctypes.CDLL(os.environ['ZTRADING_LIB'])
                            libdl.dlclose(self.ztrading_lib._handle)
                            break
                self.hand_data(callback, json_object)
            except KeyboardInterrupt:
                libdl = ctypes.CDLL(os.environ['ZTRADING_LIB'])
                libdl.dlclose(self.ztrading_lib._handle)
                e = sys.exc_info()[0]
                print('KeyboardInterrupt!')
                print("An exception occurred", e, " data: ", result)
                os._exit(0)
            except:
                libdl = ctypes.CDLL(os.environ['ZTRADING_LIB'])
                libdl.dlclose(self.ztrading_lib._handle)
                e = sys.exc_info()[0]
                print("An exception occurred", e, " data: ", result)
                os._exit(0)
        logging.info("Python ZTrading    : FINISHED")
        os._exit(0)
