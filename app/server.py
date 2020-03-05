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

    board_Y = data.get("board").get("height")
    board_X = data.get("board").get("width")

    print("BOARD SIZE")
    print(board_X, board_Y)

    response = {"color": "#00e1ff", "headType": "fang", "tailType": "curled"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

"""
def areWeGoingtoKillOurself(move, body):
    
    goodMove = True

    if move == "up":
        if body:
            return False


    elif move == "down":
        if (body.y-- == body.y):
            return False

    elif (move == "left"): 
        if (body.x-- == body.x): 
            return False

    elif (move == "right"):
        if (body.x++ == body.y):
            return False 

    return goodMove
"""

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
    #move = random.choice(directions)
    move = "up"
    
    goodMove = True

    # Are we going to kill ourself? 
    if move == "up":
        print("HEAD N NECK COMMIN IN HAWT: ")
        print(body.y)
        print(neck.y) 
        if body.y+1 == neck.y or body.y+1 == board_Y:
            goodMove = False



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
