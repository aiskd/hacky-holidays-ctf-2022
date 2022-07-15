from http.client import SWITCHING_PROTOCOLS
from matplotlib.axis import Tick
import websocket
import rel
import json

LEVEL = 3
PREV_FLAG = "CTF{capt41n-h00k!}"
NEAR_THRESHOLD = 50 # in pixels
TICK_THRESHOLD = 3 # number of ticks to wait before steering again

DIRECTIONS = {"UP": {"next": "RIGHT"}, "RIGHT": {"next": "DOWN"}, "DOWN": {"next": "LEFT"}, "LEFT": {"next": "UP"}}

URL = "wss://3acca90731734e08041fdd3367c215a0.challenge.hackazon.org/ws"

def process_game_start(state):
    pass

def overlap(min1, max1, min2, max2):
    return max(0, min(max1, max2) - max(min1, min2))

def is_near(val1, val2, ship_id):
    # print(f"{ship_id} Is near check: {val1}-{val2}   {abs(val1 - val2) < NEAR_THRESHOLD}")
    return abs(val1 - val2) < NEAR_THRESHOLD

def should_steer(dir, s_x1, s_y1, s_x2, s_y2, o_x1, o_y1, o_x2, o_y2, ship_id):
    return ((dir == "DOWN" and overlap(s_x1, s_x2, o_x1, o_x2) and s_y2 < o_y1 and is_near(s_y2, o_y1, ship_id))
            or (dir == "UP" and overlap(s_x1, s_x2, o_x1, o_x2) and s_y1 > o_y2 and is_near(s_y1, o_y2, ship_id))
            or (dir == "LEFT" and overlap(s_y1, s_y2, o_y1, o_y2) and s_x1 > o_x2 and is_near(s_x1, o_x2, ship_id))
            or (dir == "RIGHT" and overlap(s_y1, s_y2, o_y1, o_y2) and s_x2 < o_x1 and is_near(s_x2, o_x1, ship_id)))

def level3(state):
    # Check if any ships are within {NEAR_THRESHOLD}pixels of colliding something, if it is, then steer it
    for ship in state["ships"]:
        if TICK - SHIPS[ship["id"]]["steer_tick"] < TICK_THRESHOLD: #and SHIPS[ship["id"]]["direction"] != ship["direction"]
            print("tick wait")
            # we've already changed the position during the previous tick so don't change it again or the ship will spin
            continue

        # top left
        s_x1, s_y1 = ship["area"][0]["x"], ship["area"][0]["y"]
        # bottom right
        s_x2, s_y2 = ship["area"][1]["x"], ship["area"][1]["y"]

        steer_ship = False # whether or not the ship needs to be steered

        # Check if near obstructions
        for ob in BOARD["obstructions"]:
            o_x1, o_y1 = ob["area"][0]["x"], ob["area"][0]["y"]
            o_x2, o_y2 = ob["area"][1]["x"], ob["area"][1]["y"]

            if should_steer(ship["direction"], s_x1, s_y1, s_x2, s_y2, o_x1, o_y1, o_x2, o_y2, ship["id"]):
                steer_ship = True
                break
        
        # Check if near other ships
        for s2 in state["ships"]:
            o_x1, o_y1 = s2["area"][0]["x"], s2["area"][0]["y"]
            o_x2, o_y2 = s2["area"][1]["x"], s2["area"][1]["y"]
            if s2["id"] != ship["id"] and should_steer(ship["direction"], s_x1, s_y1, s_x2, s_y2, o_x1, o_y1, o_x2, o_y2, ship["id"]):
                steer_ship = True
                break
        
        # Check if ship is near the edge

        
        if steer_ship:
            print("Steering ship " + str(ship["id"]) + ship["direction"])
            ws.send(json.dumps({"type": "SHIP_STEER", "shipId": ship["id"]}))
            SHIPS[ship["id"]]["direction"] = DIRECTIONS[ship["direction"]]["next"]
            SHIPS[ship["id"]]["steer_tick"] = TICK


def main(message):
    state = json.loads(message)
    if state["type"] == "GAME_START":
        print("Board Set")
        global BOARD
        BOARD = state["level"]["board"]
        global SHIPS
        SHIPS = {}
        for i in range(len(state["level"]["ships"])):
            SHIPS[i] = {"direction": False, "steer_tick": 0}
        global TICK
        TICK = 0
        # NEXT_POS = [False for s in range(len(state["level"]["ships"]))]
    elif state["type"] == "TICK":
        level3(state)
    
    TICK += 1

# Sockets
def on_message(ws, message):
    main(message)

def on_error(ws, error):
    print(f"!!! ERROR !!!: {error}")


def on_close(ws, close_status_code, close_msg):
    print("### CLOSED ###")


def on_open(ws):
    print("### OPEN ###")
    ws.send(json.dumps({"type": "START_GAME",
            "level": LEVEL, "password": PREV_FLAG}))


if __name__ == "__main__":
    ws = websocket.WebSocketApp(URL,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
