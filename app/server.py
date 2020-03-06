import json
import os
import random

import bottle
from bottle import HTTPResponse

"""
establishing two global variables to track the size of the board
"""
board_X = 0
board_Y = 0

class bodyy:
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

    data = bottle.request.json
    print("START:", json.dumps(data))

    global board_Y
    global board_X

    board_Y = data.get("board").get("height")-1
    board_X = data.get("board").get("width")-1

    print("BOARD SIZE")

    response = {"color": "#00e1ff", "headType": "fang", "tailType": "curled"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

#function to test whether a move is a good idea or if the snake is going to either run into a walll or it's own body
def areWeGoingToKillOurself(move, snekBody, snekLength,snakePit):

  goodMove = True
  #is moving up a good move?
  if move == "up":
    if snekBody[0].get("y") == 0:
      goodMove = False

    if goodMove:
      for i in range (1, snekLength):
        tempNode = {"x": snekBody[0].get("x") ,"y": snekBody[0].get("y")-1}
        if (tempNode == snekBody[i]):
          goodMove = False

    if goodMove:
      for i in range(0,len(snakePit)):
        for j in range(0,len(snakePit[i].get("body"))):
          print(f"******* J is {j} *******")
          myNode = {"x": snekBody[0].get("x") ,"y": snekBody[0].get("y")-1}
          badNode = snakePit[i].get("body")[j]
          if (tempNode == badNode):
            goodMove = False
            break

  #is moving down a good move?
  elif move == "down":
    if snekBody[0].get("y") == board_Y:
      goodMove = False

    if goodMove:
      for i in range (1, snekLength):
        tempNode = {"x": snekBody[0].get("x"), "y": snekBody[0].get("y")+1}
        if (tempNode == snekBody[i]):
          goodMove = False

    if goodMove:
      for i in range(0,len(snakePit)):
        for j in range(0,len(snakePit[i].get("body"))):
          myNode = {"x": snekBody[0].get("x") ,"y": snekBody[0].get("y")+1}
          badNode = snakePit[i].get("body")[j]
          if (tempNode == badNode):
            goodMove = False
            break

  #is moving left a good idea?
  elif move == "left":
    if snekBody[0].get("x") == 0:
      goodMove = False

    if goodMove:
      for i in range (1, snekLength):
        tempNode = {"x": snekBody[0].get("x")-1 ,"y": snekBody[0].get("y")}
        if (tempNode == snekBody[i]):
          goodMove = False

    if goodMove:
      for i in range(0,len(snakePit)):
        for j in range(0,len(snakePit[i].get("body"))):
          myNode = {"x": snekBody[0].get("x")-1 ,"y": snekBody[0].get("y")}
          badNode = snakePit[i].get("body")[j]
          if (tempNode == badNode):
            goodMove = False
            break

  #is moving right a good idea?
  elif move == "right":
    if snekBody[0].get("x") == board_X:
      goodMove = False

    if goodMove:
      for i in range (1, snekLength):
        tempNode = {"x": snekBody[0].get("x")+1 ,"y": snekBody[0].get("y")}
        if (tempNode == snekBody[i]):
          goodMove = False

    if goodMove:
      for i in range(0,len(snakePit)):
        for j in range(0,len(snakePit[i].get("body"))):
          print(f"******* J is {j} *******")
          myNode = {"x": snekBody[0].get("x")-1 ,"y": snekBody[0].get("y")}
          badNode = snakePit[i].get("body")[j]
          if (tempNode == badNode):
            goodMove = False
            break
  return(goodMove)

#function to see if there is a snack within an imidiate move of the snake head, if there is, return that move direction
def gimmeGoldFish(snekBody, schooloFish):
  schoolSize = len(schooloFish)
  for i in range(0, schoolSize):
    #check up
    if schooloFish[i] == {"x": snekBody[0].get("x") ,"y": snekBody[0].get("y")-1}:
      return "up"
    #check down
    elif schooloFish[i] == {"x": snekBody[0].get("x") ,"y": snekBody[0].get("y")+1}:
      return "down"
    #check left
    elif schooloFish[i] == {"x": snekBody[0].get("x")-1 ,"y": snekBody[0].get("y")}:
      return "left"
    #check right
    elif schooloFish[i] == {"x": snekBody[0].get("x")+1 ,"y": snekBody[0].get("y")}:
      return "right"
    #if no food near by return "none"
    else:
      return None


@bottle.post("/move")
def move():

    data = bottle.request.json
    print("MOVE:", json.dumps(data))
    #set snake body and length variables, load positions of goldfish, and other snakes
    snekBody = data.get("you").get("body")
    snekLength = len(snekBody)
    schooloFish = data.get("board").get("food")
    snakePit = data.get("board").get("snakes")

    # directions to choose from
    directions = ["up", "down", "left", "right"]

    goodMove = False
    move = None

		#check snacks around and if it returns a move, send that move through
    move = gimmeGoldFish(snekBody, schooloFish)
    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>snaklyfe<<<<<<<<<<<<<<<<: {move}")
    if move == None:
      for i in range (0, 4):
        print(f">>>>>>>>  {i}  <<<<<<<<")
        move = random.choice(directions)
        print(f"WHATS MY MOVE: {move} \n ")

        if len(directions) == 1:
          print(f"LAST CHANCE - directions {directions}")
          break
        print(f"directions {directions}")
        #remove move used from directions list
        directions.remove(move)
        goodMove = areWeGoingToKillOurself(move, snekBody, snekLength,snakePit)
        if goodMove:
          print("good move! break!")
          break


    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "Meattballs coming through!"

    print(f"HTTPResponse move Response: {move}")

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
