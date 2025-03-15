import random
from typing import List
import csv


class Card:
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f"{str(self.rank)} of {self.suit}"


class Deck:
    def __init__(self, suits, ranks) -> None:
        self.suits = suits
        self.ranks = ranks
        self.deck = []
        self.make_deck()

    def __str__(self) -> str:
        s = ""
        for card in self.deck:
            s += str(card) + "\n"
        return s

    def make_deck(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(rank, suit))
        return self


class Player:
    def __init__(self, firstName, lastName, age, country, chips) -> None:
        self.hand = []
        self.hand_value = 0
        self.has_ace = False
        self.blackjack, self.busted = 0, 0
        self.needs_card = True
        self.chips = 1000
        self.isOut = False
        #
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.country = country
        self.chips = chips

    def clear_hand(self):
        self.hand = []
        self.hand_value = 0
        self.has_ace = False
        self.blackjack, self.busted = 0, 0

    def is_out(self):
        if self.chips == 0 and self.isOut == False:
            print("Player has 0 chips. You're out of the game")
            self.isOut = True
        return self.isOut

    def get_bet2(self):
        while True:
            self.bet = int(input(f"You have {self.chips} chips. Choose your bet: "))
            if self.bet > self.chips:
                print("Bet too high")
                continue
            break
        return self

    def __str__(self):
        return f"Player is {self.firstName} {self.lastName}, aged {self.age}, from {self.country}, having {self.chips} chips."

    def show_hand(self, newline=True, hidden=False):
        hand = self.hand
        if hidden:
            # only showing the 2nd card of the dealer
            print("Hidden card")
            hand = [self.hand[1]]
        for card in hand:
            print(card)
        if not hidden:
            print(self.hand_value)

    def draw_card(self, deck):
        deck = deck.deck
        card = deck.pop(random.randint(0, len(deck) - 1))
        if card.rank == "Ace":
            self.has_ace = True
        self.hand.append(card)
        self.hand_value += values[card.rank]

    def draw_cards(self, deck):
        for i in range(2):
            self.draw_card(deck)

    def ask_for_card(self, deck):
        if not self.blackjack:
            while True:
                response = input("\nDo you want a card? Press 'y' or 'n': ")
                if response == "y":
                    self.draw_card(deck)
                    self.adjust_for_ace()
                    self.show_hand()
                    self.check_hand()
                    if self.blackjack or self.busted:
                        break
                elif response == 'n':
                    break
                else:
                    print('Provide a valid response!')

    def adjust_for_ace(self):
        if self.hand_value > 21 and self.has_ace:
            self.hand_value -= 10

    def check_hand(self):
        if self.hand_value == 21:
            self.blackjack = 1
        elif self.hand_value > 21:
            self.busted = 1
        return self

    def show_chips(self):
        print(f"Player has {self.chips} chips")


class Dealer(Player):
    def __init__(
        self, firstName=None, lastName=None, age=None, country=None, chips=None
    ):
        super().__init__(firstName, lastName, age, country, chips)

    def show_hand(self, hidden):
        return super().show_hand(hidden=hidden)

    def get_hand_value(self):
        return self.hand_value


# -----------------
def all_players_out(players: List[Player]):
    outStatuses = [player.is_out() for player in players]
    return all(outStatuses)

def compare_hands(player: Player, dealer: Dealer, initial_check=True):
    if player.blackjack and dealer.blackjack:
        print("It's a tie!")
    elif player.blackjack:
        print("Player has blackjack!")
        player.chips += player.bet
    elif dealer.blackjack:
        print("Dealer has blackjack!")
        player.chips -= player.bet
    elif player.busted:
        print("Player busted")
        player.chips -= player.bet
    elif dealer.busted:
        print("Dealer busted!")
        player.chips += player.bet
    elif player.hand_value > dealer.hand_value:
        print("Player wins")
        player.chips += player.bet
    elif player.hand_value == dealer.hand_value:
        print("Player ties")
    else:
        print("Player loses")
        player.chips -= player.bet
    return 0


suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
ranks = list(range(2, 11)) + ["Jack", "Queen", "King", "Ace"]
values = dict()
for rank in ranks:
    if type(rank) == int:
        values[rank] = rank
    elif rank == "Ace":
        values[rank] = 11
    else:
        values[rank] = 10


def read_players() -> List[Player]:
    with open("players.csv") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        players: List[Player] = []
        for row in spamreader:
            firstName = row["FirstName"]
            lastName = row["LastName"]
            age = int(row["Age"])
            country = row["Country"]
            chips = int(row["Chips"])
            player = Player(firstName, lastName, age, country, chips)
            players.append(player)
        return players


def print_players(players: List[Player]):
    for player in players:
        print(player)


def main():
    deck = Deck(suits, ranks)
    players = read_players()
    print_players(players)
    while True:
        print("\nStart of the game")
        for player, player_ind in zip(players, list(range(1, len(players) + 1))):
            print(f"\n\nPlayer {player_ind}")
            if not player.is_out():
                player.get_bet2()
                player.draw_cards(deck)
                player.show_hand()
                player.check_hand()
        
        if not all_players_out(players):
            dealer = Dealer()
            print(f"\n\nDealer")
            dealer.draw_cards(deck)
            dealer.show_hand(hidden=True)
            dealer.check_hand()

            for i, player in enumerate(players):
                if not player.is_out():
                    player_no = i + 1
                    print(f"\n\nPlayer {player_no}")
                    player.show_hand()
                    player.check_hand()
                    player.ask_for_card(deck)

            print(f"\n\nDealer")
            dealer.show_hand(hidden=False)
            while dealer.get_hand_value() < 17:
                print("\nDealer draws")
                dealer.draw_card(deck)
                dealer.show_hand(hidden=False)
                dealer.adjust_for_ace()
                dealer.check_hand()

            for ind, player in enumerate(players):
                if not player.is_out():
                    print(f"\nPlayer {ind+1}")
                    player.show_hand()
                    compare_hands(player, dealer)
                    player.show_chips()
            print("\nEnd of the game")

            response = input("\nDo you want to play another game? y or n: ")
            if response == "y":
                for player in players:
                    player.clear_hand()
                continue
            elif response == "n":
                break
        else:
            break


if __name__ == "__main__":
    main()
