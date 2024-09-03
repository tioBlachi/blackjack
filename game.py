import random

suits = ['♣️', '♦️', '❤️', '♠️']
cards = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']

class Blackjack:
    def __init__(self, playerHandVal=0, dealerHandVal=0):
        self.deck = [[card, suit] for card in cards for suit in suits]
        self.playerHandVal = playerHandVal
        self.dealerHandVal = dealerHandVal
        self.dealerHand = None
        self.playerWins = 0
        self.dealerWins = 0
        self.ties = 0
        self.bank = 100
        self.totalGames = 1
        self.playerTurn = True
        self.dealerTurn = False
        self.running = True
        self.dealerBlackjack = False

    def card_value(self, card):
        if card[0] in ["J", "Q", "K"]:
            return 10
        elif card[0] == "A" and self.playerHandVal <= 10:
            return 11
        elif card[0] == "A" and self.playerHandVal > 11:
            return 1
        elif card[0] == "A" and self.dealerHandVal <= 10:
            return 11
        elif card[0] == "A" and self.dealerHandVal > 11:
            return 1
        else:
            return int(card[0])

    def initGame(self):
        random.shuffle(self.deck)
        return self.deck

    def drawPlayerHand(self):
        first = self.deck.pop()
        value1 = self.card_value(first)
        second = self.deck.pop()
        value2 = self.card_value(second)
        self.playerHandVal += value1 + value2

        print("\nYou have been dealt:")
        print(f"{first[0]}{first[1]} and {second[0]}{second[1]}")
        print(f"Hand Total: {self.playerHandVal}\n")
        self.check_blackjack()

        return first, second

    def drawDealerHand(self):
        first = self.deck.pop()
        second = self.deck.pop()
        self.dealerHand = (first, second)
        self.dealerHandVal += self.card_value(first) + self.card_value(second)
        if self.dealerHandVal == 21:
            self.dealerBlackjack = True

    def hitPlayer(self):
        drawn_card = self.deck.pop()
        self.playerHandVal += self.card_value(drawn_card)
        print(f"You drew a {drawn_card[0]}{drawn_card[1]}")
        print(f"Hand total: {self.playerHandVal}\n")

    def hitDealer(self):
        while self.dealerHandVal < 17:
            drawn_card = self.deck.pop()
            self.dealerHandVal += self.card_value(drawn_card)
            print(f"Dealer Drew a {drawn_card[0]}{drawn_card[1]}")
            print(f"Dealer Hand Total: {self.dealerHandVal}\n")
        if 21 > self.dealerHandVal >= 17:
            print("Dealer must stand!")

    def check_blackjack(self):
        if self.playerHandVal == 21:
            self.playerWins += 1
            print("Blackjack! You win!\n")
            self.reset()
            return True


    def check_winner(self):
        if self.playerTurn:
            if self.playerHandVal > 21:
                self.dealerWins += 1
                print("BUST! You lose!\n")
                self.reset()

        if not self.playerTurn:
            if self.playerHandVal > self.dealerHandVal:
                print("You beat the dealer! You win!\n")
                self.playerWins += 1
                self.reset()

            elif self.dealerHandVal == self.playerHandVal:
                print("PUSH! It's a tie!\n")
                self.ties += 1
                self.reset()

            elif self.dealerHandVal > 21 >= self.playerHandVal:
                self.playerWins += 1
                print("Dealer BUSTS! You win!\n")
                self.reset()

            elif self.playerHandVal < self.dealerHandVal <= 21:
                self.dealerWins += 1
                print("Dealer wins! You lose!\n")
                self.reset()

            elif self.playerHandVal > 21:
                self.dealerWins += 1
                print("BUST! You lose!\n")
                self.reset()

    def showStats(self):
        if self.running:
            print("           STATS           ")
            print("___________________________")

            if self.dealerWins == 0 and self.playerWins == 0:
                print("0.00% Player Wins")
                print(f"Ties: {self.ties}")
                print(f"Total Games: {self.totalGames - 1}")
                print(f"Your current hand total: {self.playerHandVal}\n")
            elif self.dealerWins == 0 and self.playerWins > 0 and self.totalGames == self.playerWins:
                print(f"{self.playerWins / self.totalGames * 100:.2f}% Player Wins")
                print(f"Losses: {self.dealerWins}")
                print(f"Ties: {self.ties}")
                print(f"Total Games: {self.totalGames - 1}")
                print(f"Your current hand total: {self.playerHandVal}\n")
            else:
                print(f"Player Wins: {self.playerWins}")
                print(f"Losses: {self.dealerWins}")
                print(f"Ties: {self.ties}")
                print(f"Total Games: {self.totalGames - 1}")
                print(f"{self.playerWins / (self.totalGames - 1) * 100:.2f}% Player Wins")
                print(f"Your current hand total: {self.playerHandVal}\n")
        else:
            print("           STATS           ")
            print("___________________________")
            if self.dealerWins and self.playerWins == 0:
                print("0.00% Player Wins")
                print(f"Ties: {self.ties}")
                print(f"Total Games: {self.totalGames - 1}")
            else:
                #self.dealerWins == 0 and self.playerWins > 0 and self.totalGames == self.playerWins:
                print(f"{self.playerWins / self.totalGames * 100:.2f}% Player Wins")
                print(f"Ties: {self.ties}")
                print(f"Total Games: {self.totalGames - 1}")

    def reset(self):
        while True:
            choice = input("Play again? (Y/N)").lower()
            if choice == 'y':
                self.playerHandVal = 0
                self.dealerHandVal = 0
                self.deck = [[card, suit] for card in cards for suit in suits]
                self.deck = self.initGame()
                self.playerTurn = True
                self.dealerTurn = False
                self.dealerHand = None
                self.dealerBlackjack = False
                self.totalGames += 1
                print("********* BLACKJACK ***********")
                print(f"           GAME #{self.totalGames}             ")
                self.drawPlayerHand()
                self.drawDealerHand()
                break
            elif choice == 'n':
                self.running = False
                self.playerTurn = False
                self.dealerTurn = False
                print("Thank you for playing!")
                self.showStats()
                break
            else:
                print("Invalid input! Please enter either 'y' or 'n'.\n")

    def check_dealer_blackjack(self):
        if self.dealerBlackjack:
            self.dealerWins += 1
            print("Dealer has Blackjack! You lose!\n")
            self.reset()

    def getPlayerTurn(self):
        return self.playerTurn

    def getDealerTurn(self):
        return self.dealerTurn

    def getRunning(self):
        return self.running

    def getDealerHand(self):
        return self.dealerHand

    def getDealerHandVal(self):
        return self.dealerHandVal

    def getDealerBlackjack(self):
        return self.dealerBlackjack

    def setRunning(self, running):
        self.running = running

    def setPlayerTurn(self, playerTurn):
        self.playerTurn = playerTurn

    def setDealerTurn(self, dealerTurn):
        self.dealerTurn = dealerTurn


