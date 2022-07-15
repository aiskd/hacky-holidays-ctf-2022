import websocket
import rel  # to stop websocket using keyboard
import json # to convert dictionaries to/from json

# Constants
#   for starting the correct level
LEVEL = 3
PREV_FLAG = "CTF{capt41n-h00k!}"

#   for the ship moving logic
NEAR_THRESHOLD = 50 # distance between ship and obstacle/other ship to trigger steer
TICK_THRESHOLD = 5 # number of ticks to wait before steering again

#   enum of directions for steering
DIRECTIONS = {"UP": {"next": "RIGHT"}, "RIGHT": {"next": "DOWN"}, "DOWN": {"next": "LEFT"}, "LEFT": {"next": "UP"}}

URL = "wss://260d02c8bbbe6e0dcddef3c23d809ab1.challenge.hackazon.org/ws"

def process_game_start(state):
    pass

### HELPER FUNCTIONS ###
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

def get_points(obj):
    # top left
    s_x1, s_y1 = obj["area"][0]["x"], obj["area"][0]["y"]
    # bottom right
    s_x2, s_y2 = obj["area"][1]["x"], obj["area"][1]["y"]
    return s_x1, s_y1, s_x2, s_y2

### LOGIC FOR LEVELS ###
def level3(state):
    # Check if any ships are within {NEAR_THRESHOLD}pixels of colliding into something. If it is, then steer it
    for ship in state["ships"]:
        # we've already changed the position during the previous tick so don't change it again or the ship will spin
        if abs(TICK - SHIPS[ship["id"]]["steer_tick"]) < TICK_THRESHOLD:
            print("tick wait")
            continue

        s_x1, s_y1, s_x2, s_y2 = get_points(ship)

        steer_ship = False # whether or not the ship needs to be steered

        # Check if near obstructions
        for ob in BOARD["obstructions"]:
            o_x1, o_y1, o_x2, o_y2 = get_points(ob)

            if should_steer(ship["direction"], s_x1, s_y1, s_x2, s_y2, o_x1, o_y1, o_x2, o_y2, ship["id"]):
                steer_ship = True
                break

        # Check if near other ships
        for s2 in state["ships"]:
            s2_x1, s2_y1, s2_x2, s2_y2 = get_points(s2)
            if s2["id"] != ship["id"] and should_steer(ship["direction"], s_x1, s_y1, s_x2, s_y2, s2_x1, s2_y1, s2_x2, s2_y2, ship["id"]):
                steer_ship = True
                break
        
        # TODO Check if ship is near the edge

        if steer_ship:
            print("Steering ship " + str(ship["id"]) + " " + ship["direction"])
            ws.send(json.dumps({"type": "SHIP_STEER", "shipId": ship["id"]}))
            # SHIPS[ship["id"]]["direction"] = DIRECTIONS[ship["direction"]]["next"]
            SHIPS[ship["id"]]["steer_tick"] = TICK

### MAIN FUNCTION ###
def main(message):
    state = json.loads(message) # conver to python dict

    if state["type"] == "GAME_START":
        print("Board Set")

        # store board state
        global BOARD
        BOARD = state["level"]["board"]

        # internally keep track of ship state
        global SHIPS
        SHIPS = {}
        for i in range(len(state["level"]["ships"])):
            SHIPS[i] = {"direction": False, "steer_tick": 0}

        # count the number of ticks
        global TICK
        TICK = 0
    elif state["type"] == "TICK":
        level3(state)
        TICK += 1

### SOCKET FUNCTIONS ###
def on_message(ws, message):
    main(message)

def on_error(ws, error):
    print(f"!!! ERROR !!!: {error}")


def on_close(ws, close_status_code, close_msg):
    print("### CLOSED ###")


def on_open(ws):
    print("### OPEN ###")
    # start level when first connect to socket
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
