from game import Game


def main():
    game = Game()
    with open('console.txt', 'w') as file:
        file.write("")
    with open('tree-output.txt', 'w') as file:
        file.write("")
    game.start_game()


if __name__ == "__main__":
    main()
