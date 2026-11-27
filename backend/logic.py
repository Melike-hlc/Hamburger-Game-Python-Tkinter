import random

DT = 0.1
START_LIVES = 3
ORDER_TIME = 45
RAW_LIMIT = 5
BURN_LIMIT = 10
FRIES_FILL_SECONDS = 8
DRINK_FILL_SECONDS = 6
ITEM_POINTS = 10
ORDER_BONUS = 20

score = 0
lives = START_LIVES
game_over = False
game_time = 0.0

player_name = "Player"

plate_items = []
orders = []
stoves = []
slots = {}
event_log = []

orders_completed = 0
orders_failed = 0
items_ok = 0
items_wrong = 0
burnt_patties = 0


def generate_order():
    order = ["bottom_bun", "patty"]

    if random.choice([True, False]):
        order.append("cheese")

    if random.choice([True, False]):
        order.append("lettuce")

    order.append("top_bun")

    if random.choice([True, False]):
        order.append("fries")

    if random.choice([True, False]):
        order.append("drink")

    return order


def create_order():
    order = {
        "remaining": generate_order(),
        "time_left": ORDER_TIME,
        "total_time": ORDER_TIME
    }

    return order


def replace_order(menu_index):
    orders[menu_index] = create_order()


def init_orders():
    orders.clear()

    for i in range(3):
        orders.append(create_order())



def log_event(event_type, detail):

    valid_events = [
        "game_start",
        "item_ok",
        "item_wrong",
        "order_complete",
        "order_timeout",
        "burnt_patty",
        "game_over"
    ]

    if event_type not in valid_events:
        return

    event = {
        "t": round(game_time, 1),
        "event_type": event_type,
        "detail": detail,
        "score_after": score,
        "lives_after": lives
    }

    event_log.append(event)



def set_player_name(name):
    global player_name

    name = str(name).strip()

    name = name.replace(",", "")
    name = name.replace("\n", "")
    name = name.replace("\r", "")

    name = name[:20].strip()

    if not name:
        name = "Player"

    player_name = name


def is_plate_item(item):
    allowed_items = [
        "bottom_bun",
        "top_bun",
        "lettuce",
        "cheese",
        "patty",
        "fries",
        "drink"
    ]

    return item in allowed_items

def add_to_plate(item):
    if game_over:
        return False

    if not is_plate_item(item):
        return False

    plate_items.append(item)
    return True

def clear_plate():
    plate_items.clear()


def init_stoves():
    stoves.clear()

    for i in range(4):
        stoves.append({
            "occupied": False,
            "cook_time": 0
        })


def get_patty_state(cook_time):
    if cook_time < RAW_LIMIT:
        return "raw_patty"
    elif cook_time < BURN_LIMIT:
        return "patty"
    else:
        return "burnt_patty"


def put_on_stove(stove_index):
    if game_over:
        return False

    if stoves[stove_index]["occupied"]:
        return False

    stoves[stove_index]["occupied"] = True
    stoves[stove_index]["cook_time"] = 0

    return True

def take_from_stove(stove_index):
    global burnt_patties

    stove = stoves[stove_index]

    if not stove["occupied"]:
        return None

    patty_state = get_patty_state(stove["cook_time"])

    stove["occupied"] = False
    stove["cook_time"] = 0

    if patty_state == "burnt_patty":
        burnt_patties += 1
        log_event("burnt_patty", str(stove_index))

    return patty_state

def init_slots():
    global slots

    slots = {
        "fries": {"ready": True, "fill": 100},
        "drink1": {"ready": True, "fill": 100},
        "drink2": {"ready": True, "fill": 100}
    }


def take_from_slot(slot_name):
    if game_over:
        return None

    slot = slots[slot_name]

    if not slot["ready"]:
        return None

    slot["ready"] = False
    slot["fill"] = 0

    if slot_name == "fries":
        return "fries"
    else:
        return "drink"


def add_score(points):
    global score
    score += points

def lose_life():
    global lives, game_over

    if game_over:
        return

    lives -= 1

    if lives <= 0:
        lives = 0
        game_over = True
        log_event("game_over", "")

def try_remove_from_order(item, menu_index):
    remaining = orders[menu_index]["remaining"]
    if item in remaining:
        remaining.remove(item)
        return True
    return False

def check_order_complete(menu_index):
    global orders_completed

    if len(orders[menu_index]["remaining"]) == 0:
        add_score(ORDER_BONUS)
        orders_completed += 1
        log_event("order_complete", str(menu_index))
        replace_order(menu_index)

def deliver_item(item, menu_index):
    global items_ok, items_wrong
    if game_over:
        return False
    if try_remove_from_order(item, menu_index):
        add_score(ITEM_POINTS)
        items_ok += 1
        log_event("item_ok", item)
        check_order_complete(menu_index)
        return True
    else:
        items_wrong += 1
        log_event("item_wrong", item)
        lose_life()
        return False

def deliver_plate(menu_index):
    global items_ok, items_wrong
    if game_over or len(plate_items) == 0:
        return
    wrong_count = 0
    for item in plate_items:
        if try_remove_from_order(item, menu_index):
            add_score(ITEM_POINTS)
            items_ok += 1
            log_event("item_ok", item)
        else:
            items_wrong += 1
            wrong_count += 1
            log_event("item_wrong", item)
    if wrong_count > 0:
        lose_life()
    check_order_complete(menu_index)
    clear_plate()

def update_orders(dt):
    global orders_failed
    for i in range(len(orders)):
        orders[i]["time_left"] -= dt
        if orders[i]["time_left"] <= 0:
            orders_failed += 1
            log_event("order_timeout", i)
            lose_life()
            replace_order(i)

def update_stoves(dt):
    for stove in stoves:
        if stove["occupied"]:
            stove["cook_time"] += dt

def update_slots(dt):
    for name, slot in slots.items():
        if not slot["ready"]:
            if name == "fries":
                fill_seconds = FRIES_FILL_SECONDS
            else:
                fill_seconds = DRINK_FILL_SECONDS
            slot["fill"] += (100 / fill_seconds) * dt
            if slot["fill"] >= 100:
                slot["fill"] = 100
                slot["ready"] = True

def update_game(dt):
    global game_time

    if game_over:
        return

    game_time += dt

    update_orders(dt)
    update_stoves(dt)
    update_slots(dt)

def restart_game():
    global score, lives, game_over, game_time
    global plate_items, event_log
    global orders_completed, orders_failed
    global items_ok, items_wrong, burnt_patties

    score = 0
    lives = START_LIVES
    game_over = False
    game_time = 0.0

    plate_items = []
    event_log = []

    orders_completed = 0
    orders_failed = 0
    items_ok = 0
    items_wrong = 0
    burnt_patties = 0

    init_orders()
    init_stoves()
    init_slots()

    log_event("game_start", player_name)

def get_session_summary():
    return {
        "player": player_name,
        "score": score,
        "duration_sec": round(game_time, 1),
        "orders_completed": orders_completed,
        "orders_failed": orders_failed,
        "items_ok": items_ok,
        "items_wrong": items_wrong,
        "burnt_patties": burnt_patties,
        "events": [event.copy() for event in event_log]
    }

