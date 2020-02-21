from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

"""
NOTES:

Data tyoe:
0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}],
0 ==> refers to room number
(3,5) ==> x,y coordinates?
{'n': 1, 's': 5, 'e': 3, 'w': 7} ==> room id for each direction
==> None if there is no room

get_exits() returns [] of exits
current_room.id() returns an integer of room id (default to 0)
player.travel(direction) => Move to another room or show "cannot move"

BFS will probably be used for the shortest traverse (Queue needed)

DFS to try initially
1) Randomly pick a direction
2) Repeat that direction until it cannot be continued
3) Go opposite direction
4) Randomly picked again and continue
5) Repeat step 2 and 3 if get_exits() is None

BFS
1) Look for all possible exits
2) Randomly pick one to start and continue until all exits filled out
3) 
"""


def add_to_visited(room_id, visited):
    if room_id not in visited:
        # Create a new item for each id for modification
        visited[room_id] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}
    return visited


def get_opposite_direction(direction):
    if direction == "n":
        return "s"
    if direction == "s":
        return "n"
    if direction == "e":
        return "w"
    if direction == "w":
        return "e"


def possible_exits(room_id, player, visited):
    # get.exits() results in ['n','s', 'e','w']
    choices = player.current_room.get_exits()
    possible_choices = []
    # loop through tuple to get empty sets in visited
    #  {'n': '?', 's': '?', 'e': '?', 'w': '?'}
    for direction, target_room_id in visited[room_id].items():
        if direction in choices and target_room_id == '?':
            possible_choices.append(direction)
    return possible_choices


def traverse_all_rooms(player):
    # Initiate visited dict
    visited = {}
    # List to save path
    visited_path = []
    # Create a queue
    queue = Queue()
    # Add the current room id to queue)
    queue.enqueue(player.current_room.id)

    while queue.size() > 0:
        # Case: All room has been traversed
        if len(visited) == len(world.rooms):
            # Return visited 
            return visited
        
        # Pop out the last item in queue
        room_id = queue.dequeue()
        # Add the item into visited
        visited = add_to_visited(room_id, visited)
        
        
        if len(visited_path) > 0:
           
            # Previous room can be found as the last item of visited path
            # Data Type of visited_path[-1] --> [291, 's']
            prev_room_id = visited_path[-1][0]
           
            # Previous room direction in relation to current room
            # Thus opposite direction is needed
            prev_room_dir = get_opposite_direction(visited_path[-1][1])
            
            # Set the room id for the direction as indicated by previous room direction
            # visited --> room_id: {'n': ?, 's': ?, 'e': ?, 'w': ?}
            visited[room_id][prev_room_dir] = prev_room_id
        
        # Define exit options in each room
        # choices example ==> ['n', 's']
        choices = possible_exits(room_id, player, visited)
        
        # If there are possible exits
        if choices:
            # choices indicate direction
            choice = random.choice(choices)
            player.travel(choice)
            # Update room id of specific direction
            visited[room_id][choice] = player.current_room.id
            # Add the room id and direction to visited path
            visited_path.append([room_id, choice])
            
        # If there are no possible exits,
        # player needs to return to previous room
        else:
            # The only possible move is return
            choice = prev_room_dir
            # travel opposite way
            player.travel(choice)
            if visited_path:
                # remove last one since it is a duplicate of room
                visited_path.pop()
            else:
                # Add the return to the traversal path
                traversal_path.append(choice)
                # return visited for next traverse
                return visited
        
        # Add move to traverse path
        traversal_path.append(choice)
        # Add current room to queue to continue loop
        queue.enqueue(player.current_room.id)
        print(visited_path)


player = Player(world.starting_room)
traverse_all_rooms(player)



# def traverse_all_room(graph):
#     # Generate path to traverse all room
#     generated_path = []
#     # Keep track of latest room
#     back_track = []
#     # Visited room
#     visited = {}
#     # Unexplored rooms
#     unexplored = {}
#     # Loop will continue until all the rooms are visited
#     while len(visited) < len(room_graph):
#         # Starting case
#         if len(visited) == 0:
#             current_room = player.current_room.id
#             current_exits = player.current_room.get_exits()
#             visited[current_room] = current_exits
#             unexplored[current_room] = current_exits
#             # rand_num = random.randint(1, 4)
#             # if rand_num == 1 and "n" in current_exits:
#             #     player.travel("n")
#             # elif rand_num == 2 and "e" in current_exits:
#             #     player.travel("e")
#             # elif rand_num == 3 and "s" in current_exits:
#             #     player.travel("s")
#             # elif rand_num == 4 and "w" in current_exits:
#             #     player.travel("w")

#         if player.current_room.id not in visited:
#             current_room = player.current_room.id
#             current_exits = player.current_room.get_exits()
#             visited[player.current_room.id] = current_exits
#             unexplored[player.current_room.id] = current_exits

#         while len(unexplored[player.current_room.id]) < 1:
#             opposite_direction = back_track.pop()
#             generated_path.append(opposite_direction)
#             player.travel(opposite_direction)

#         move = unexplored[player.current_room.id].pop
#         generated_path.append(move)
#         back_track.append(get_opposite_direction(move))
#         player.travel(move)

#     print("---")

#     return generated_path


# traversal_path.extend(traverse_all_room(room_graph))

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
