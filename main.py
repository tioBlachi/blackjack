from game import Blackjack

if __name__ == '__main__':
    print("********* BLACKJACK ***********")
    print("           GAME #1             ")
    game = Blackjack()
    game.initGame()
    game.drawPlayerHand()
    game.drawDealerHand()

    while game.getRunning():

        while game.getPlayerTurn():
            choice = input("What would you like to do?\n1. Hit\n2. Stand\n3. Stats\n4. Quit\n")
            if choice == "1":
                game.hitPlayer()
                game.check_winner()
            elif choice == "2":
                game.setPlayerTurn(False)
            elif choice == "3":
                game.showStats()
            elif choice == "4":
                print("Thanks for playing!")
                game.setRunning(False)
                break

            if game.getRunning() and not game.getPlayerTurn():
                game.setDealerTurn(True)
                print(f"Dealer has {game.getDealerHand()[0][0]}{game.getDealerHand()[0][1]} and {game.getDealerHand()[1][0]}{game.getDealerHand()[1][1]}")
                print(f"Dealer Hand Total: {game.getDealerHandVal()}")
                game.check_dealer_blackjack()
            while game.getDealerTurn():
                game.hitDealer()
                game.check_winner()
