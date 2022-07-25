import pygame
import sys

BOARD = {
    "type": "GAME_START",
    "level": {
        "id": 5,
        "board": {
            "width": 1886,
            "height": 1188,
            "obstructions": [
                {
                    "type": "HARBOUR_BORDER",
                    "area": [
                        {
                            "x": 135,
                            "y": 0
                        },
                        {
                            "x": 185,
                            "y": 215.7142857142857
                        }
                    ],
                    "id": 0
                },
                {
                    "type": "HARBOUR_BORDER",
                    "area": [
                        {
                            "x": 260,
                            "y": 0
                        },
                        {
                            "x": 310,
                            "y": 215.7142857142857
                        }
                    ],
                    "id": 1
                },
                {
                    "type": "BORDER_ROCK",
                    "area": [
                        {
                            "x": 0,
                            "y": 0
                        },
                        {
                            "x": 135,
                            "y": 51
                        }
                    ]
                },
                {
                    "type": "BORDER_ROCK",
                    "area": [
                        {
                            "x": 310,
                            "y": 0
                        },
                        {
                            "x": 1886,
                            "y": 51
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_1",
                    "area": [
                        {
                            "x": 278,
                            "y": 249
                        },
                        {
                            "x": 368,
                            "y": 345.66
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_2",
                    "area": [
                        {
                            "x": 44,
                            "y": 346
                        },
                        {
                            "x": 124,
                            "y": 399.28
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_3",
                    "area": [
                        {
                            "x": 319,
                            "y": 446
                        },
                        {
                            "x": 409,
                            "y": 516.02
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_2",
                    "area": [
                        {
                            "x": 339,
                            "y": 615
                        },
                        {
                            "x": 439,
                            "y": 681.6
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_1",
                    "area": [
                        {
                            "x": 303,
                            "y": 752
                        },
                        {
                            "x": 393,
                            "y": 848.66
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_2",
                    "area": [
                        {
                            "x": 75,
                            "y": 946
                        },
                        {
                            "x": 165,
                            "y": 1005.94
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_3",
                    "area": [
                        {
                            "x": 253,
                            "y": 1046
                        },
                        {
                            "x": 333,
                            "y": 1108.24
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_2",
                    "area": [
                        {
                            "x": 809,
                            "y": 475
                        },
                        {
                            "x": 899,
                            "y": 534.94
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_3",
                    "area": [
                        {
                            "x": 1180,
                            "y": 273
                        },
                        {
                            "x": 1260,
                            "y": 335.24
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_1",
                    "area": [
                        {
                            "x": 1518,
                            "y": 553
                        },
                        {
                            "x": 1608,
                            "y": 649.66
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_2",
                    "area": [
                        {
                            "x": 1260,
                            "y": 793
                        },
                        {
                            "x": 1330,
                            "y": 839.62
                        }
                    ]
                },
                {
                    "type": "ROCKS_SMALL_1",
                    "area": [
                        {
                            "x": 774,
                            "y": 886
                        },
                        {
                            "x": 864,
                            "y": 982.66
                        }
                    ]
                }
            ],
            "harbour": [
                {
                    "x": 185,
                    "y": 0
                },
                {
                    "x": 260,
                    "y": 107.85714285714285
                }
            ]
        },
        "mechanics": {
            "borderCollision": True,
            "sequentialDocking": True
        },
        "ships": [
            False,
            False,
            False,
            False,
            False,
            False
        ]
    }
}

def get_points(obj, has_area=True):
    if has_area:
        obj = obj["area"]
    # top left
    s_x1, s_y1 = obj[0]["x"], obj[0]["y"]
    # bottom right
    s_x2, s_y2 = obj[1]["x"], obj[1]["y"]
    return s_x1, s_y1, s_x2, s_y2


screen = pygame.display.set_mode((1886, 1188))
rects = []

pygame.font.init()
font1 = pygame.font.Font('freesansbold.ttf', 20)
font = pygame.font.Font('freesansbold.ttf', 15)
texts = []

# Red Obstructions
count = 0
for ob in BOARD["level"]["board"]["obstructions"]:
    s_x1, s_y1, s_x2, s_y2 = get_points(ob)
    rect_obj = pygame.Rect(s_x1, s_y1, s_x2-s_x1, s_y2-s_y1)
    pygame.draw.rect(screen, pygame.Color('red'), rect_obj)
    typ = ob["type"]
    t = font.render(f"{count} {typ}", False, (0,0,0))
    texts.append((t, rect_obj))
    count += 1

# Green Harbour
s_x1, s_y1, s_x2, s_y2 = get_points(BOARD["level"]["board"]["harbour"], False)
rect_obj = pygame.Rect(s_x1, s_y1, s_x2-s_x1, s_y2-s_y1)
pygame.draw.rect(screen, pygame.Color('green'), rect_obj)

waypoints = [(220,200), (220, 560), (386, 557), (601, 557), (604, 195), (1738, 195), (604, 1054), (1059, 1054)]
port_waypoint = (601, 557)
for way in waypoints:
    pygame.draw.circle(screen, (255,255,255), way, 20)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
                break
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)

    for text, textRect in texts:
        screen.blit(text, textRect)
    
    # screen.fill((255, 255, 255))
    pygame.display.update()

def should_turn_p5(x, y):
    waypoints = [(220,200), (220, 560), (386, 557), (601, 557), (593, 187), (1717, 187), (1717, 1046), (607, 1046)]
    SIZE = 10
    for waypoint in waypoints:
        if (x == waypoint[0] + SIZE or x == waypoint[0] - SIZE) and (y == waypoint[1] + SIZE or y == waypoint[1] - SIZE):
            return True
        return False

def enter_port_p5(x, y):
    port_waypoint = (601, 557)
    if x == port_waypoint[0] and y == port_waypoint[1]:
        return True
    return False

def level5(state):
    for ship in state["ships"]:
        # we've already changed the position during the previous tick so don't change it again or the ship will spin
        if abs(TICK - SHIPS[ship["id"]]["steer_tick"]) < TICK_THRESHOLD and not SHIPS[ship["id"]]["override_steer_tick"]:
            print("tick wait")
            continue

        s_x1, s_y1, s_x2, s_y2 = get_points(ship)
        ship_mid_x, ship_mid_y = get_center(s_x1, s_y1, s_x2, s_y2)


# logic
"""
for boat in boats:
    if should_turn(boat[x], boat[y], waypoints):
        send turn signal
    elif boat is next to enter and enter_port(boat[x], boat[y], port_waypoint):
        turn 3 times
"""
