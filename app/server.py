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
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    global board_Y
    global board_X

    board_Y = data.get("board").get("height")-1
    board_X = data.get("board").get("width")-1

    print("BOARD SIZE")
    print(f"Board_X: {board_X} \nBoard_Y: {board_Y} \n")

    response = {"color": "#00e1ff", "headType": "fang", "tailType": "curled"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )

def areWeGoingToKillOurself(move, snekBody, snekLength):

  #print(f"HEAD! \n H.Y: {head.y} - H.X {head.x} \n")
  #print(f"NECK! \n N.Y: {neck.y} - H.X {neck.x} \n")
  #print(f"Move: {move} \n head: {head} \n neck: {neck} \n ")
  goodMove = True
  #is moving up a good move?
  if move == "up":
    #print(f"boardy: {board_Y}")
    #print(f"UP! \n H.Y: {head.y} - N.Y {neck.y} \n")
    if snekBody[0].get("y") == 0:

      goodMove = False

    if goodMove: 
      for i in range (1, snekLength):
        #print(f"head: {snekBody[0].get('y')}")
        #print(f"{i} - snek body {snekBody[i].get('y')}" )

        tempNode = {"x": snekBody[0].get("x") ,"y": snekBody[0].get("y")-1}
        #print(f"tempNode: {tempNode}")
        if (tempNode == snekBody[i]):
          goodMove = False

    #is moving down a good move?
  elif move == "down":
    #print(f"boardy: {board_Y}")
    #print(f"DOWN! \n H.Y: {head.y} - N.Y {neck.y} \n")
    if snekBody[0].get("y") == board_Y:
      goodMove = False

    if goodMove: 
      for i in range (1, snekLength):
        #print(f"head: {snekBody[0].get('y')}")
        #print(f"{i} - snek body {snekBody[i].get('y')}" )

        tempNode = {"x": snekBody[0].get("x"), "y": snekBody[0].get("y")+1}
        #print(f"tempNode: {tempNode}")
        if (tempNode == snekBody[i]):
          goodMove = False
  
  #is moving left a good idea?
  elif move == "left":
    #print(f"boardx: {board_X}")
    #print(f"LEFT! \n H.X: {head.x} - N.X {neck.x} \n"  )

    if snekBody[0].get("x") == 0:
      goodMove = False

    if goodMove: 
      for i in range (1, snekLength):
        #print(f"head: {snekBody[0].get('x')}")
        #print(f"{i} - snek body {snekBody[i].get('x')}" )
       
        tempNode = {"x": snekBody[0].get("x")-1 ,"y": snekBody[0].get("y")}
        #print(f"tempNode: {tempNode}")
        if (tempNode == snekBody[i]):
          goodMove = False


  #is moving right a good idea?
  elif move == "right":
    #print(f"boardx: {board_X}")
    #print(f"RIGHT! \n H.X: {head.x} - N.X {neck.x} \n")
    if snekBody[0].get("x") == board_X:
      goodMove = False

    if goodMove: 
      for i in range (1, snekLength):
        #print(f"head: {snekBody[0].get('x')}")
        #print(f"{i} - snek body {snekBody[i].get('x')}" )

        tempNode = {"x": snekBody[0].get("x")+1 ,"y": snekBody[0].get("y")}
        #print(f"tempNode: {tempNode}")
        if (tempNode == snekBody[i]):
          goodMove = False


  print(f"AM I GONNA STAY ALIVE? {goodMove}")
  return(goodMove)

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
    else:
      return None



@bottle.post("/move")
def move():

    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """

    data = bottle.request.json
    print("MOVE:", json.dumps(data))

    snekBody = data.get("you").get("body")
    snekLength = len(snekBody)
    schooloFish = data.get("board").get("food")

    #print(f"body {snekBody}")
    #print(f"length {snekLength}")
    
    # Choose a random direction to move in
    directions = ["up", "down", "left", "right"]

    goodMove = False
    move = None

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

        #pop direction
        print(f"directions {directions}")
        directions.remove(move)
        goodMove = areWeGoingToKillOurself(move, snekBody, snekLength)
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
