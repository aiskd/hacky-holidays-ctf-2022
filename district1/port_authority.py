from black import nullcontext
import websocket
import rel  # to stop websocket using keyboard
import json # to convert dictionaries to/from json

# Constants
#   for starting the correct level
LEVEL = 5
PREV_FLAG = "CTF{C4pt41N-4MErIc4}"

#   for the ship moving logic
NEAR_THRESHOLD = 50 # distance between ship and obstacle/other ship to trigger steer
TICK_THRESHOLD = 20 # number of ticks to wait before steering again

#   enum of directions for steering
DIRECTIONS = {"UP": {"next": "RIGHT"}, "RIGHT": {"next": "DOWN"}, "DOWN": {"next": "LEFT"}, "LEFT": {"next": "UP"}}

URL = "wss://8dc92437a5bdc6b5232ac541a4cec7c1.challenge.hackazon.org/ws"

def process_game_start(state):
    pass

### HELPER FUNCTIONS ###
def overlap(min1, max1, min2, max2):
    # print(min1, max1, min2, max2)
    return max(0, min(max1, max2) - max(min1, min2))

def is_near(val1, val2, ship_id):
    # print(f"{ship_id} Is near check: {val1}-{val2}   {abs(val1 - val2) < NEAR_THRESHOLD}")
    return abs(val1 - val2) < NEAR_THRESHOLD

def should_steer(dir, s_x1, s_y1, s_x2, s_y2, o_x1, o_y1, o_x2, o_y2, ship_id):
    return ((dir == "DOWN" and overlap(s_x1, s_x2, o_x1, o_x2) and s_y2 < o_y1 and is_near(s_y2, o_y1, ship_id))
            or (dir == "UP" and overlap(s_x1, s_x2, o_x1, o_x2) and s_y1 > o_y2 and is_near(s_y1, o_y2, ship_id))
            or (dir == "LEFT" and overlap(s_y1, s_y2, o_y1, o_y2) and s_x1 > o_x2 and is_near(s_x1, o_x2, ship_id))
            or (dir == "RIGHT" and overlap(s_y1, s_y2, o_y1, o_y2) and s_x2 < o_x1 and is_near(s_x2, o_x1, ship_id)))

def hit_border(dir, s_x1, s_y1, s_x2, s_y2, ship_id):
    return ((dir == "UP" and is_near(s_y1, 51, ship_id)) or (dir == "LEFT" and is_near(s_x1, 0, ship_id))
     or(dir == "DOWN" and is_near(s_y2, 1188, ship_id)) or (dir == "RIGHT" and is_near(s_x2, 1886, ship_id)))

def get_points(obj, has_area=True):
    if has_area:
        obj = obj["area"]
    # top left
    s_x1, s_y1 = obj[0]["x"], obj[0]["y"]
    # bottom right
    s_x2, s_y2 = obj[1]["x"], obj[1]["y"]
    return s_x1, s_y1, s_x2, s_y2

def get_center(s_x1, s_y1, s_x2, s_y2):
    return (s_x1 + (s_x2-s_x1)/2), (s_y1 + (s_y2-s_y1)/2)

### LOGIC FOR LEVELS ###
def level3(state):
    # Check if any ships are within {NEAR_THRESHOLD}pixels of colliding into something. If it is, then steer it
    # if state["ships"][CURRENT_SHIP]["isDocked"]:
    #     CURRENT_SHIP += 1
    # print(state)
    for ship in state["ships"]:
        # we've already changed the position during the previous tick so don't change it again or the ship will spin
        if abs(TICK - SHIPS[ship["id"]]["steer_tick"]) < TICK_THRESHOLD and not SHIPS[ship["id"]]["override_steer_tick"]:
            print("tick wait")
            continue

        s_x1, s_y1, s_x2, s_y2 = get_points(ship)
        ship_mid_x, ship_mid_y = get_center(s_x1, s_y1, s_x2, s_y2)
        width = min(s_x2-s_x1, s_y2-s_y1)
        height = max(abs(s_x2-s_x1), abs(s_y2-s_y1))
        # print(f"HeightL {height}")
        # print(f"Before: {s_x1, s_y1, s_x2, s_y2}")
        # if ship["direction"] in ["LEFT", "RIGHT"]:
        #     s_y1 = ship_mid_y - height/2
        #     s_y2 = ship_mid_y + height/2
        # if ship["direction"] in ["UP", "DOWN"]:
        #     s_x1 = ship_mid_x - height/2
        #     s_x2 = ship_mid_x + height/2
        # print(f"After: {s_x1, s_y1, s_x2, s_y2}")

        steer_ship = False # whether or not the ship needs to be steered

        # AVOIDING OBSTRUCTIONS AND OTHER SHIPS
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
        
        harb_x1, harb_y1, harb_x2, harb_y2 = get_points(BOARD["harbour"], False)
        harbour_x, harbour_y = get_center(harb_x1, harb_y1, harb_x2, harb_y2)
        turning_point_x = harbour_x
        turning_point_y = 700
        # Move current ship towards turning point
        # if not steer_ship and ship["id"] == CURRENT_SHIP:
        #     # direction
        #     delta_x = turning_point_x - ship_mid_x
        #     delta_y = turning_point_y - ship_mid_y

        #     move_x_dir = abs(delta_x) > abs(delta_y)
        #     if move_x_dir:
        #         # ship ---- turning point
        #         if delta_x > 0 and ship["direction"] != "RIGHT":
        #             steer_ship = True

        # Make other ships move in circles/away from turning point
        if ship["id"] != CURRENT_SHIP:
            pass

        # Check if ship is near the edge
        if hit_border(ship["direction"], s_x1, s_y1, s_x2, s_y2, ship["id"]):
            steer_ship = True

        if steer_ship:
            print("Steering ship " + str(ship["id"]) + " " + ship["direction"])
            ws.send(json.dumps({"type": "SHIP_STEER", "shipId": ship["id"]}))
            # SHIPS[ship["id"]]["direction"] = DIRECTIONS[ship["direction"]]["next"]
            SHIPS[ship["id"]]["steer_tick"] = TICK

def should_turn(x, y):
    waypoints = [
        (220,200), 
        (220, 560), (386, 557), (601, 557), (604, 195), (1738, 195), (1738, 1054), (604, 1054)]
    SIZE = 20
    for waypoint in waypoints:
        if overlap(x-SIZE, x+SIZE, waypoint[0] - SIZE, waypoint[0] + SIZE) and overlap(y-SIZE, y+SIZE, waypoint[1] - SIZE, waypoint[1] + SIZE):
            print("overlap")
            print(waypoint)
            print(x, y)
            return True
    return False

MIDDLE_X_MIN = 1050
MIDDLE_X_MAX = 1400
MIDDLE_Y_MIN = 440
MIDDLE_Y_MAX = 730

def find_middle(ships):
    for ship in ships:
        s_x1, s_y1, s_x2, s_y2 = get_points(ship)
        if overlap(s_x1, s_x2, MIDDLE_X_MIN, MIDDLE_X_MAX) and overlap(s_y1, s_y2, MIDDLE_Y_MIN, MIDDLE_Y_MAX):
            return ship["id"]

def middle_should_turn(x, y):
    middle_waypoints = [(1050, 440), (1400, 440), (1400, 730), (1050, 730)]
    SIZE = 25
    for waypoint in middle_waypoints:
        if overlap(x-SIZE, x+SIZE, waypoint[0] - SIZE, waypoint[0] + SIZE) and overlap(y-SIZE, y+SIZE, waypoint[1] - SIZE, waypoint[1] + SIZE):
            print("overlap")
            print(waypoint)
            print(x, y)
            return True
    return False

def enter_port(x, y):
    port_waypoint = (601, 557)
    if x == port_waypoint[0] and y == port_waypoint[1]:
        return True
    return False

def level5(state):

    # if first_run:
    global MIDDLE
    MIDDLE = find_middle(state["ships"])
    print(f"MIDDLE: {MIDDLE}")
    for ship in state["ships"]:
        # we've already changed the position during the previous tick so don't change it again or the ship will spin
        if abs(TICK - SHIPS[ship["id"]]["steer_tick"]) < TICK_THRESHOLD and not SHIPS[ship["id"]]["override_steer_tick"]:
            # print("tick wait")
            continue

        s_x1, s_y1, s_x2, s_y2 = get_points(ship)
        ship_mid_x, ship_mid_y = get_center(s_x1, s_y1, s_x2, s_y2)

        #  (ship["id"] == MIDDLE and middle_should_turn(ship_mid_x, ship_mid_y)) \
        if (ship["id"] != MIDDLE and should_turn(ship_mid_x, ship_mid_y)):

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

        global PORT_CENTER
        PORT_CENTER = (700 + 850) / 2

        # internally keep track of ship state
        global SHIPS
        SHIPS = {}
        for i in range(len(state["level"]["ships"])):
            SHIPS[i] = {"steer_tick": 0, "override_steer_tick": False}

        global CURRENT_SHIP
        CURRENT_SHIP = 0

        # count the number of ticks
        global TICK
        TICK = 0

    elif state["type"] == "TICK":
        level5(state)
        TICK += 1
    elif state["type"] == "LOSS":
        pass
        # ws.send(json.dumps({"type": "START_GAME", "level": LEVEL, "password": PREV_FLAG}))
    
    
    # screen.blit()

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
