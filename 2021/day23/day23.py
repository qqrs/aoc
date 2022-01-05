from pprint import pprint
from collections import namedtuple, Counter
import re
import math
import statistics
import functools
import itertools
from queue import PriorityQueue

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

State = namedtuple('State', ['cost', 'board'])
Board = namedtuple('Board', ['hall', 'rooms'])
class Move(dict): pass

# @dataclass(frozen=True)
    # class burrow:
    # __slots__ = ('room', 'num_home')
    # room: tuple
    # num_home: int

# class Hall(tuple): pass
# class Rooms(tuple): pass
# class Room(tuple): pass


BOARD_REGEX = (
"""#############
#\.\.\.\.\.\.\.\.\.\.\.#
###([ABCD])#([ABCD])#([ABCD])#([ABCD])###
  #([ABCD])#([ABCD])#([ABCD])#([ABCD])#
  #########""")

BOARD_EXTRA = (
"""#D#C#B#A#
#D#B#A#C#""")


ROOM_SIZE = None


def parse_board(txt, add_extra):
    m = list(re.findall(BOARD_REGEX, txt)[0])

    if add_extra:
        extra = [
            v
            for line in BOARD_EXTRA.splitlines()
            for v in line.strip('#').split('#')]
        m = m[:4] + extra + m[4:]

    rooms = [[], [], [], []]
    for i, v in enumerate(m):
        rooms[i % len(rooms)].append(v)

    global ROOM_SIZE
    ROOM_SIZE = len(rooms[0])

    # TODO: handle room with all amphs already home

    board = Board(tuple([None] * 7),
                  tuple([tuple(room) for room in rooms]))
    return(board)


def is_room_full(room):
    assert(isinstance(room, int))
    return room >= ROOM_SIZE


def is_room_cleared(room, n):
    assert(isinstance(room, tuple))
    target = room_target(n)
    return all(v == target for v in room)


def all_rooms_complete(rooms):
    return all(isinstance(room, int) and room == ROOM_SIZE for room in rooms)


def room_target(n):
    return chr(ord('A') + n)


def room_for_amph(amph):
    return ord(amph) - ord('A')


def exit_room(room, n):
    assert(room)
    cost = 1 + ROOM_SIZE - len(room)
    rem_room = room[1:]
    if is_room_cleared(rem_room, n):
        rem_room = len(rem_room)
    return (room[0], rem_room, cost)


def enter_room(room, amph):
    assert(isinstance(room, int))
    assert(room < ROOM_SIZE)
    cost = ROOM_SIZE - room
    return (room + 1, cost)


def exit_hall(hall, n):
    assert(hall[n] is not None)
    return(hall[n], hall[:n] + (None,) + hall[n+1:])


def enter_hall(hall, n, amph):
    assert(hall[n] is None)
    return(hall[:n] + (amph,) + hall[n+1:])


def check_hallway_path(hall, x, y):
    if x > y:
        x, y = y, x
    hall_idxs = [get_hall_idx_for_x(i) for i in range(x+1, y)]
    hall_idxs = [v for v in hall_idxs if v is not None]
    return all(hall[idx] is None for idx in hall_idxs)


def get_hall_idx_for_x(x):
    return [0, 1, None, 2, None, 3, None, 4, None, 5, 6][x]


def get_hall_x(hall_idx):
    return [0, 1, 3, 5, 7, 9, 10][hall_idx]


def get_room_x(room_idx):
    return [2, 4, 6, 8][room_idx]


def energy_per_step(amph):
    return 10 ** (ord(amph) - ord('A'))


def apply_move(state, src_room=None, src_hall=None, dest_room=None, dest_hall=None):
    assert((src_hall is not None) != (src_room is not None))
    assert((dest_hall is not None) != (dest_room is not None))

    hall, rooms = state.board
    enter_dist, exit_dist = (0, 0)

    new_hall = hall
    new_rooms = list(rooms)

    if src_room is not None:
        (amph, exited_room, exit_dist) = exit_room(rooms[src_room], src_room)
        new_rooms[src_room] = exited_room
        src_x = get_room_x(src_room)
    elif src_hall is not None:
        (amph, new_hall) = exit_hall(hall, src_hall)
        src_x = get_hall_x(src_hall)

    if dest_room is not None:
        (entered_room, enter_dist) = enter_room(rooms[dest_room], amph)
        new_rooms[dest_room] = entered_room
        dest_x = get_room_x(dest_room)
    elif dest_hall is not None:
        new_hall = enter_hall(new_hall, dest_hall, amph)
        dest_x = get_hall_x(dest_hall)

    new_rooms = tuple(new_rooms)

    dist = (exit_dist + abs(dest_x - src_x) + enter_dist)
    energy_mult = energy_per_step(amph)
    cost = state.cost + dist * energy_mult

    is_done = all_rooms_complete(new_rooms)
    return (State(cost, Board(new_hall, new_rooms)), is_done)


# def get_moves():
#   for each amph in hall:
#       if target room is cleared
#           and path to target room isn't blocked:
#               -> we can move to target room
#
#   for each room:
#       if room isn't empty and room isn't cleared:
#           pop closest amph to exit
#           calc door address
#           for each hall spot to left of door:
#               if spot isn't occupied:
#                 -> we can move to this hall spot
#           for each hall spot to right of door:
#               if spot isn't occupied:
#                 -> we can move to this hall spot
#
#   return cost and state for each possible move
def get_moves(board):
    moves = []

    # see if amphs in rooms can move
    for i, room in enumerate(board.rooms):
        # check if they've all left
        if isinstance(room, int):
            continue

        # try hallway to left
        for j in range(1 + i, -1, -1):
            if board.hall[j]:
                break
            moves.append(Move(src_room=i, dest_hall=j))

        # try hallway to right
        for j in range(2 + i, len(board.hall)):
            if board.hall[j]:
                break
            moves.append(Move(src_room=i, dest_hall=j))

    # see if amphs in hall can move
    hall = board.hall
    for i in range(len(hall)):
        if hall[i] is None:
            continue

        # try destination room
        j = room_for_amph(hall[i])
        room = board.rooms[j]
        if not isinstance(room, int):
            continue

        is_hallway_clear = check_hallway_path(hall, get_hall_x(i), get_room_x(j))
        if (is_hallway_clear and not is_room_full(room)):
            moves.append(Move(src_hall=i, dest_room=j))

    return moves
        

def pt1():
    # f = open('example.txt')
    f = open('input.txt')

    # board = parse_board(f.read(), add_extra=False)
    board = parse_board(f.read(), add_extra=True)

    state = State(0, board)
    print(state)
    # import ipdb; ipdb.set_trace()

    seen = {board: 0}
    hops = {}
    winners = []

    pq = PriorityQueue()
    pq.put(PrioritizedItem(0, state))

    pprint(state)

    i = 0
    while not pq.empty():
        state = pq.get().item
        i += 1
        if i % 50000 == 0:
            print((pq.qsize(), state))
        moves = get_moves(state.board)
        # pprint(moves)
        for move in moves:
            mstate, is_done = apply_move(state, **move)
            if mstate.cost >= seen.get(mstate.board, math.inf):
                # already seen it at lower cost
                continue
            if is_done:
                hops[mstate] = state
                winners.append(mstate)
                # print('got one: cost={} {} -> {}'.format(mstate.cost, state, mstate))
                continue
            else:
                seen[mstate.board] = mstate.cost
                hops[mstate] = state
                pq.put(PrioritizedItem(mstate.cost, mstate))

    pprint(winners)
    print(min(w.cost for w in winners))

    best_cost = min(w.cost for w in winners)

    for w in winners:
        if w.cost != best_cost:
            continue
        print('')
        n = w
        while n:
            print(n)
            n = hops.get(n)
    # import ipdb; ipdb.set_trace()


def interactive():
    f = open('example.txt')
    # f = open('input.txt')

    board = parse_board(f.read(), add_extra=False)
    # board = parse_board(f.read(), add_extra=True)

    state = State(0, board)
    print(state)

    while True:
        print('')
        print(state)
        moves = get_moves(state.board)

        for i, move in enumerate(moves):
            mstate, is_done = apply_move(state, **move)
            print('{:2d} {} {}'.format(i, move, mstate))

        choice = int(input('choose move: '))
        move = moves[choice]
        mstate, is_done = apply_move(state, **move)
        state = mstate

        if is_done:
            print('got one: cost={}'.format(mstate.cost))
            break


if __name__ == '__main__':
    pt1()
    # interactive()

