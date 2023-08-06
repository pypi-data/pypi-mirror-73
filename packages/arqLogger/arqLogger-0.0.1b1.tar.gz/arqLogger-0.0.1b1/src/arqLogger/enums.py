from enum import Enum


class Order:
    Created = 0
    Submitted = 1
    Accepted = 2
    Partial = 3
    Completed = 4
    Canceled = 5
    Rejected = 6
    Expired = 7


class LogTypes(Enum):
    Event = "EV"
    Response = "RE"
    Own = "PR"


class EventTypes(Enum):
    Initialize = "INI"
    MarketData = "MD"
    ExecReport = "OR"
    Pause = "PA"
    Error = "ER"
    Internal = "INT"


class ResponseTypes(Enum):
    NewOrder = "NO"
    CancelOrder = "CO"
    ReplaceOrder = "RO"

