import queue
from datetime import datetime
import time
import math
import threading
import schedule
import json
from enum import Enum

import websocket


class ArquantLogger():

    def __init__(self, strategy, strategy_id):
        # Connection related variables
        # Initializing a queue
        self.queue = queue.Queue()
        self.ws_connection = None
        self.ws_thread = None
        self.connected = False
        self.strategy = strategy
        self.strategy_id = strategy_id
        self.execution_id = round(datetime.now().timestamp() * 100)
        self.msg_id = 0
        self.event_id = 0

    def connect(self):
        self.strategy.logs("Starting websocket connection.")
        self.ws_connection = websocket.WebSocketApp("ws://177.231.134.94:8001/",
                                                    on_message=self.on_message,
                                                    on_error=self.on_error,
                                                    on_close=self.on_close,
                                                    on_open=self.on_open)

        # Create a thread and target it to the run_forever function, then start it.
        self.ws_thread = threading.Thread(target=self.ws_connection.run_forever,
                                          kwargs={"ping_interval": 270})
        self.ws_thread.start()

        # Wait 5 sec to establish the connection
        conn_timeout = 5
        time.sleep(1)
        while not self.ws_connection.sock.connected and conn_timeout:
            time.sleep(1)
            conn_timeout -= 1
        if not self.ws_connection.sock.connected:
            self.strategy.logs("Connection could not be established.")

    def start_logging(self):
        schedule.every(1).seconds.do(self.send_logs)
        schedule.run_pending()
        self.strategy.logs("Start Scheduling Logs")

    def send_logs(self):
        self.strategy.logs("Executing send_logs")
        if self.ws_connection.sock.connected:
            while not self.queue.empty():
                msg = self.queue.get()
                self.send_log(msg)
        else:
            self.connect()

    def on_message(self, message):
        self.strategy.logs("message arrived: %s" % message)

    def on_error(self, exception):
        self.strategy.logs("error ocurred in websocket connection %s" % exception)

    def on_close(self):
        self.connected = False

    def on_open(self):
        self.connected = True

    def close_connection(self):
        self.ws_connection.close()

    def append_log(self, log):
        self.queue.put(log)

    def send_log(self, log):
        self.ws_connection.send(log)

    def send_md_event(self, datas, entries):
        md_map = dict()
        idx = 0
        for data in datas:
            md_map[data.tradecontract] = dict()
            for entry in entries[idx]:
                md_map[data.tradecontract] = self.get_data_entry(data, entry)
            idx += 1
        self.append_log(json.dumps(MDEventLog(self.msg_id, self.strategy_id, self.event_id, json.dumps(md_map)).__dict__))
        self.msg_id += 1
        self.event_id += 1

    def get_data_entry(self, data, entry):
        value = None
        if hasattr(data, entry):
            value = getattr(data, entry)
            if not isinstance(value, float):
                value = value[0]
            if not value or math.isnan(value):
                value = None
            else:
                value = round(value, 6)
        return value

# Logs
class LogTypes(Enum):
    Event = "EV"
    Response = "RE"
    Own = "PR"


class EventTypes(Enum):
    MarketData = "MD"
    ExecReport = "OR"
    Pause = "PA"
    Internal = "IN"


class ResponseTypes(Enum):
    NewOrder = "NO"
    CancelOrder = "CO"
    ReplaceOrder = "RO"

class Log:
    def __init__(self, id, strategy_id, log_type):
        self.id = id
        self.strategy_id = strategy_id
        self.type = log_type
        self.timestamp = datetime.now().timestamp()


class EventLog(Log):
    def __init__(self, id, strategy_id, event_id, event_type):
        super().__init__(id, strategy_id, LogTypes.Event.value)
        self.event_id = event_id
        self.event_type = event_type

class ResponseLog(Log):
    def __init__(self, id, strategy_id, event_id, response_type):
        super().__init__(id, strategy_id, LogTypes.Response.value)
        self.event_id = event_id
        self.response_type = response_type


class StrategyLog(Log):
    def __init__(self, id, strategy_id, data):
        super().__init__(id, strategy_id, LogTypes.Own.value)
        for k, v in data.items():
            self.__setattr__(k, v)


class NewOrderResponseLog(ResponseLog):
    def __init__(self, id, strategy_id, event_id, order_id, side, px, qty, instrument):
        super().__init__(id, strategy_id, event_id, ResponseTypes.NewOrder.value)
        self.order_id = order_id
        self.side = side
        self.px = px
        self.qty = qty
        self.instrument = instrument


class CancelOrderResponseLog(ResponseLog):
    def __init__(self, id, strategy_id, event_id, order_id):
        super().__init__(id, strategy_id, event_id, ResponseTypes.CancelOrder.value)
        self.order_id = order_id


class ReplaceOrderResponseLog(ResponseLog):
    def __init__(self, id, strategy_id, event_id, order_id, side, new_px, new_qty, instrument):
        super().__init__(id, strategy_id, event_id, ResponseTypes.ReplaceOrder.value)
        self.order_id = order_id
        self.side = side
        self.new_px = new_px
        self.new_qty = new_qty
        self.instrument = instrument


class MDEventLog(EventLog):
    def __init__(self, id, strategy_id, event_id, md_received):
        super().__init__(id, strategy_id, event_id, EventTypes.MarketData.value)
        self.md_received = md_received


class EREventLog(EventLog):
    def __init__(self, id, strategy_id, event_id, order_id, state, last_px, last_qty, rem_size):
        super().__init__(id, strategy_id, event_id, EventTypes.ExecReport.value)
        self.order_id = order_id
        self.state = state
        self.last_px = last_px
        self.last_qty = last_qty
        self.rem_size = rem_size


class PauseEventLog(EventLog):
    def __init__(self, id, strategy_id, event_id, description):
        super().__init__(id, strategy_id, event_id, EventTypes.Pause.value)
        self.description = description


class InternalEventLog(EventLog):
    def __init__(self, id, strategy_id, event_id, description):
        super().__init__(id, strategy_id, event_id, EventTypes.Internal.value)
        self.description = description
