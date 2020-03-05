import json
import os
import random

import bottle
from bottle import HTTPResponse

"""
adding a test comment
"""
board_X = 0
board_Y = 0

class body:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    board_Y = data.get("board").get("height")-1
    board_X = data.get("board").get("width")-1

    print("BOARD SIZE")
    print(board_X, board_Y)

    response = {"color": "#00e1ff", "headType": "fang", "tailType": "curled"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

def areWeGoingToKillOurself(move, head, neck):
  goodMove = True
  #is moving up a good move?
  if move == "up":
    print("HEAD N NECK COMMIN IN HAWT: ")
    print(head.y)
    print(neck.y)
    if head.y-1 == neck.y or head.y-1 == -1:
      goodMove = False
    #is moving down a good move?
  elif move == "down":
    print("HEAD N NECK COMMIN IN HAWT: ")
    print(head.y)
    print(neck.y)
    if head.y+1 == neck.y or head.y+1 == board_Y:
      goodMove = False
  #is moving left a good idea?
  if move == "left":
    print("HEAD N NECK COMMIN IN HAWT: ")
    print(head.x)
    print(neck.x)
    if head.x-1 == neck.x or head.x-1 == -1:
      goodMove = False
  #is moving right a good idea?
  if move == "right":
    print("HEAD N NECK COMMIN IN HAWT: ")
    print(head.x)
    print(neck.x)
    if head.x+1 == neck.x or head.x+1 == board_X:
      goodMove = False

  print("HOW MY MOVE LOOKIN'?")
  print(goodMove)
  return(goodMove)

@bottle.post("/move")
def move():

    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    print("MOVE:", json.dumps(data))


    # get head coordinates & creaate head
    x = data.get("you").get("body")[0].get("x")
    y = data.get("you").get("body")[0].get("y")
    head = body(x,y)

    x = data.get("you").get("body")[1].get("x")
    y = data.get("you").get("body")[1].get("y")
    neck = body(x,y)




    # Choose a random direction to move in
    directions = ["up", "down", "left", "right"]
    move = random.choice(directions)
    print("WHATS MY MOVE")
    print(move)
    print(type(directions))
    directions = directions.remove(move)
    goodMove = areWeGoingToKillOurself(move, head, neck)

    while not goodMove or len(directions)>0:
      move = random.choice(directions)
      directions = directions.remove(move)
      goodMove = areWeGoingToKillOurself(move, head, neck)


    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "Meattballs coming through!"

    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
