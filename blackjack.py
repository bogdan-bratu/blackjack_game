import random
from typing import List

class Card():
    def __init__(self, rank, suit) -> None:
        self.rank = rank
        self.suit = suit
    
    def __str__(self) -> str:
        return f'{str(self.rank)} of {self.suit}'

class Deck():
    def __init__(self, suits, ranks) -> None:
        self.suits = suits
        self.ranks = ranks
        self.deck = []
        self.make_deck()

    def __str__(self) -> str:
        s = ''
        for card in self.deck:
            s += str(card) + '\n'
        return s

    def make_deck(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(rank, suit))
        return self
    
class Player():
    def __init__(self) -> None:
        self.hand = []
        self.hand_value = 0
        self.has_ace = False
        self.ended_game = False
        if isinstance(self, Player):
            self.chips = 1000

    def clear_hand(self):
        self.hand = []
        self.hand_value = 0
        self.has_ace = False
        self.ended_game = False

    def get_bet(self):
        if isinstance(self, Player):
            self.bet = int(input(f'You have {self.chips} chips. Choose your bet: '))
        else:
            self.bet = None

    def __str__(self, newline=True) -> str:
        s = ''
        for card in self.hand:
            if newline:
                s += '\n' + str(card)
            else:
                s += str(card)
        return s
    
    def draw_card(self, deck):
        deck = deck.deck
        card = deck.pop(random.randint(0, len(deck) - 1))
        if card.rank == 'Ace':
            self.has_ace = True
        self.hand.append(card)
        self.hand_value += values[card.rank]

    def show_hand(self, newline=True):
        print(self.__str__(newline))
        print(self.hand_value)

    # def show_hand_value(self):
    #     print(self.hand_value)

    def ask_for_card(self, deck):
        end = 0
        while not end:
            response = input("\nDo you want a card? Press 'y' or 'n': ")
            if response == 'y':
                self.draw_card(deck)
                self.show_hand()
                self.adjust_for_ace()
                self.show_hand_value()
                end = self.check_hand()
                if end:
                    self.set_ended_game()
            else:
                break
    
    def adjust_for_ace(self):
        if self.hand_value > 21 and self.has_ace:
            self.hand_value -= 10

    def check_hand(self):
        end = 0
        if self.hand_value == 21:
            print('Congratulations! Blackjack')
            end = 1
            if type(self) is Player:
                self.chips += self.bet
                print(f"Player has {self.chips} chips")
        elif self.hand_value > 21:
            print('Busted')
            end = 1
            if type(self) is Player:
                self.chips -= self.bet
                print(f"Player has {self.chips} chips left")
            #elif type(self) is Dealer:
            #    print(f'Dealer has busted! Player wins ')
        return end
    
    def compare_hands(self, dealer_hand_value):
        if self.hand_value > dealer_hand_value:
            print("Player wins")
            self.chips += self.bet
            print(f"Player has {self.chips} chips")
        elif self.hand_value == dealer_hand_value:
            print("Player ties")
            print(f"Player has {self.chips} chips left")
        else:
            print("Player loses")
            self.chips -= self.bet
            print(f"Player has {self.chips} chips left")

    def get_ended_game(self):
        return self.ended_game

    def set_ended_game(self):
        self.ended_game = True
        return self

class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()

    def show_hand(self, hidden=False):
        if hidden:
            print("\nHidden card", end="")
        return super().show_hand()
    
    def get_hand_value(self):
        return self.hand_value


suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
ranks = list(range(2, 11)) + ['Jack', 'Queen', 'King', 'Ace']
values = dict()
for rank in ranks:
    if type(rank) == int:
        values[rank] = rank
    elif rank == 'Ace':
        values[rank] = 11
    else:
        values[rank] = 10


def main():
    deck = Deck(suits, ranks)
    no_players = 1
    players: List[Player] = []
    player_bets = {}
    for _ in range(no_players):
        players.append(Player()) 

    while True:
        print('\nStart of the game')
        #list_of_ends = [False for player in players]
        for i, player in enumerate(players):
            player_no = i + 1
            print(f'\n\nPlayer {player_no}')
            player_bets[player_no] = player.get_bet()
            for _ in range(2):
                player.draw_card(deck)
            player.show_hand()

        return 0 
        for ind, player in enumerate(players):
            print(f'\n\nPlayer {ind+1}')
            player : Player = player
            player.get_bet()
            for _ in range(2):
                player.draw_card(deck)
            player.show_hand()
            #player.show_hand_value()
            end = player.check_hand()
            if end:
                player.set_ended_game()
            if player.get_ended_game():
                list_of_ends[ind] = True
        
        if not all(list_of_ends):
            dealer = Dealer()
            print(f'\n\nDealer')
            dealer.draw_card(deck)
            dealer.show_hand(hidden=True)
            dealer.draw_card(deck)
            end = dealer.check_hand()
            if end:
                dealer.set_ended_game()

            for ind, player in enumerate(players):
                player : Player = player
                if dealer.get_ended_game():
                    continue
                if not player.get_ended_game():
                    print(f'\n\nPlayer {ind+1}')
                    player.show_hand()
                    player.show_hand_value()
                    player.ask_for_card(deck)

            print(f'\n\nDealer')
            dealer.show_hand()
            dealer.show_hand_value()
            while dealer.get_hand_value() < 17:
                print('\nDealer draws')
                dealer.draw_card(deck)
                dealer.show_hand()
                dealer.adjust_for_ace()
                dealer.show_hand_value()
                end = dealer.check_hand()
                if end:
                    dealer.set_ended_game()

            for ind, player in enumerate(players):
                if dealer.get_ended_game() or player.get_ended_game():
                    continue
                print(f'\nPlayer {ind+1}')
                player.show_hand()
                player.show_hand_value()
                player.compare_hands(dealer.get_hand_value())
            print("\nEnd of the game")

        response = input('\nDo you want to play another game? y or n: ')
        if response == 'y':
            for player in players:
                player.clear_hand()
            continue
        elif response == 'n':
            break



if __name__ == '__main__':
    main()
