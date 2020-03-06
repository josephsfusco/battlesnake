class body:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    print("hi")
    head = body(0, 5)

    print(head.x+1)
    print(head.y+1)

    return False

main()