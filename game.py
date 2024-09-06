import time
import random

class Game:
    def __init__(self):
        self.deck = None
        self.playerHand = []
        self.dealerHand = []
        self.playerScore = 0
        self.dealerScore = 0
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.gamesPlayed = 1
        self.running = True

    def run(self):
        self.deal()
        time.sleep(.75)
        while self.running:
            print()
            time.sleep(.75)
            try:
                choice = input("What would you like to do?\n1. Hit\n2. Stand\n3. See Stats\n4. Quit")
                match choice:
                    case "1":
                        self.hitPlayer()
                    case "2":
                        self.hitDealer()
                    case "3":
                        self.show_stats()
                    case "4":
                        self.running = False
                        time.sleep(.75)
                        print()
                        print("Thank you for playing!")
                        print()
                        time.sleep(.75)
                        self.show_stats()
                    case _:
                        print("Invalid input. Please enter 1, 2, 3 or 4")
            except Exception as e:
                print(f"An error occured: {e}")

    def deal(self):
        print("Welcome to Blackjack!")
        time.sleep(.75)
        print(f"Game {self.gamesPlayed}")
        print("Dealing...")
        time.sleep(1)
        suits = ["❤️", "♣️", "♦️", "♠️"]
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, "A", "J", "Q", "K"]
        # create new deck and shuffle it
        self.deck = [[rank, suit] for rank in ranks for suit in suits]
        random.shuffle(self.deck)

        # deal 2 cards to the player and dealer
        self.playerHand.append(self.deck.pop(0))
        self.dealerHand.append(self.deck.pop(0))
        self.playerHand.append(self.deck.pop(0))
        self.dealerHand.append(self.deck.pop(0))

        time.sleep(.75)
        print(f"Your hand: {self.playerHand[0][0]}{self.playerHand[0][1]} and {self.playerHand[1][0]}{self.playerHand[1][1]}")
        print(f"Dealer shows: {self.dealerHand[1][0]}{self.dealerHand[1][1]}")

        self.update_scores()

        if self.playerScore == 21:
            time.sleep(.75)
            print()
            print("You have Blackjack!")

    def card_val(self, card):
        rank = card[0]
        if rank in ["J", "Q", "K"]:
            return 10
        elif rank == "A":
            return 11
        else:
            return rank

    def hand_value(self, hand):
        score = 0
        aces = 0
        for card in hand:
            value = self.card_val(card)
            score += value
            if card[0] == "A":
                aces += 1

        while score > 21 and aces > 0:
            score -= 10
            aces -= 1

        return score

    def hitPlayer(self):
        print()
        card = self.deck.pop(0)
        time.sleep(.75)
        print(f"You were dealt: {card[0]}{card[1]}")
        self.playerHand.append(card)
        self.update_scores()
        self.check_bust()

    def hitDealer(self):
        print()
        time.sleep(.75)
        print(f"Dealer has {self.dealerHand[1][0]}{self.dealerHand[1][1]} and {self.dealerHand[0][0]}{self.dealerHand[0][1]}")
        time.sleep(.75)
        self.check_blackjack()
        print(f"Dealer score: {self.dealerScore}")
        print()
        #if len(self.dealerHand) == 2:
        #    self.check_winner()

        while self.dealerScore < 17:
            card = self.deck.pop(0)
            time.sleep(.75)
            print(f"Dealer drew: {card[0]}{card[1]}")
            self.dealerHand.append(card)
            self.update_scores()
            if 17 <= self.dealerScore <= 21:
                time.sleep(.75)
                print()
                print("Dealer must stand")

        self.check_winner()

    def check_bust(self):
        if self.playerScore > 21:
            print()
            print("You busted! You lose!")
            self.loses += 1
            self.reset()
            return True
        else:
            return False

    def update_scores(self):
        self.playerScore = self.hand_value(self.playerHand)
        self.dealerScore = self.hand_value(self.dealerHand)

        match len(self.dealerHand), len(self.playerHand):
            case 2, 2:
                time.sleep(.75)
                print()
                print(f"Your score: {self.playerScore} \nDealer: {self.card_val(self.dealerHand[1])}")

            case (dealer_len, player_len) if player_len > 2 and dealer_len == 2:
                time.sleep(.75)
                print(f"Your score: {self.playerScore} \nDealer: {self.card_val(self.dealerHand[1])}")
                print()
            case (dealer_len, _) if dealer_len >= 3:
                time.sleep(.75)
                print(f"Your score: {self.playerScore} \nDealer: {self.dealerScore}")
                print()

    def check_winner(self):
        if self.playerScore == 21 or self.dealerScore == 21 and len(self.dealerHand) == len(self.playerHand) == 2:
            self.check_blackjack()
        # checking other winning/losing conditions
        if self.playerScore > self.dealerScore and not self.check_bust():
            print("You beat the dealer! You win!")
            self.wins += 1
            self.reset()
        elif self.dealerScore > self.playerScore and 17 <= self.dealerScore <= 21:
            print("Dealer beats your hand! You lose!")
            self.loses += 1
            self.reset()
        elif self.playerScore == self.dealerScore and 17 <= self.dealerScore <= 21:
            print("You and the Dealer have the same score! It's a Push!")
            self.draws += 1
            self.reset()
        else:
            print("Dealer busts! You win!")
            self.wins += 1
            self.reset()

    def check_blackjack(self):
        player_blackjack = False
        dealer_blackjack = False

        if self.card_val(self.playerHand[0]) + self.card_val(self.playerHand[1]) == 21:
            player_blackjack = True
        if self.card_val(self.dealerHand[0]) + self.card_val(self.dealerHand[1]) == 21:
            dealer_blackjack = True

        if player_blackjack and dealer_blackjack:
            print("Dealer also has Blackjack! It's a Push!")
            self.draws += 1
            self.reset()
        elif player_blackjack and not dealer_blackjack:
            print("Dealer cannot beat your Blackjack! You win!")
            self.wins += 1
            self.reset()
        elif dealer_blackjack and not player_blackjack:
            print("Dealer has Blackjack! You lose!")
            self.loses += 1
            self.reset()

    def show_stats(self):
        match self.running:
            case True:
                print()
                print("          STATS          ")
                print(f"Games Played: {self.gamesPlayed - 1}")
                print(f"Games Won: {self.wins}")
                print(f"Draws: {self.draws}")
                print(f"Loses: {self.loses}")
                print(f"Winning Percentage: {self.wins/self.gamesPlayed*100:.2f}%")
                print(f"Your current score: {self.playerScore}")
            case False:
                print("          STATS          ")
                print(f"Games Played: {self.gamesPlayed - 1}")
                print(f"Games Won: {self.wins}")
                print(f"Draws: {self.draws}")
                print(f"Loses: {self.loses}")
                print(f"Winning Percentage: {self.wins / self.gamesPlayed * 100:.2f}%")

    def reset(self):
        while True:
            try:
                print()
                choice = input("Would you like to play again? (1: Yes, 2: No)")
                match choice:
                    case "1":
                        print()
                        self.dealerScore = 0
                        self.playerScore = 0
                        self.playerHand = []
                        self.dealerHand = []
                        self.gamesPlayed += 1
                        self.run()
                        break
                    case "2":
                        self.running = False
                        print()
                        print("Thank you for playing!")
                        print()
                        self.gamesPlayed += 1
                        self.show_stats()
                        break
                    case _:
                        print("Invalid input! Please enter 1 or 2.")
                        print()
            except Exception as e:
                print(f"An error has occurred: {e}")
