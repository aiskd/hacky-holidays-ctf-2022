import asyncio
import websockets
URL = "wss://3acca90731734e08041fdd3367c215a0.challenge.hackazon.org/ws"

import websocket

def on_message(wsapp, message):
    print(message)

wsapp = websocket.WebSocketApp(URL, on_message=on_message)
wsapp.run_forever()

# import websocket
# import _thread
# import time
# import rel

# def on_message(ws, message):
#     print(message)

# def on_error(ws, error):
#     print(error)

# def on_close(ws, close_status_code, close_msg):
#     print("### closed ###")

# def on_open(ws):
#     ws.send({"type": "SHIP_STEER", "ship_id": 0})
#     print("Opened connection")

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp(URL,
#                               on_open=on_open,
#                               on_message=on_message,
#                               on_error=on_error,
#                               on_close=on_close)

#     ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
#     rel.signal(2, rel.abort)  # Keyboard Interrupt
#     rel.dispatch()