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

    def __str__(self, card, newline, hidden) -> str:
        s = ''
        if hidden:
            s= '\nHidden card'
        elif newline:
            s += '\n' + card.__str__()
        else:
            s = card.__str__()
        return s
    
    def show_hand(self, newline=True, hidden=False):
        for card in self.hand:
            print(self.__str__(card, newline, hidden))
        print(self.hand_value)
    
    def draw_card(self, deck):
        deck = deck.deck
        card = deck.pop(random.randint(0, len(deck) - 1))
        if card.rank == 'Ace':
            self.has_ace = True
        self.hand.append(card)
        self.hand_value += values[card.rank]

    def draw_cards(self, deck):
        for i in range(2):
            self.draw_card(deck)

    def ask_for_card(self, deck):
        end = 0
        while not end:
            response = input("\nDo you want a card? Press 'y' or 'n': ")
            if response == 'y':
                self.draw_card(deck)
                self.show_hand()
                self.adjust_for_ace()
                end = self.check_hand()
                if end:
                    self.set_ended_game()
            else:
                break
    
    def adjust_for_ace(self):
        if self.hand_value > 21 and self.has_ace:
            self.hand_value -= 10

    def check_hand(self):
        blackjack, busted = 0, 0
        if self.hand_value == 21:
            print('Congratulations! Blackjack')
            blackjack = 1
        elif self.hand_value > 21:
            print('Busted')
            busted = 1
        return blackjack, busted
    
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
    
    def player_won(self):
        print('Congratulations! You won!')
        self.chips += self.bet


class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()

    def draw_card(self, deck):
        return super().draw_card(deck)
    
    def draw_cards(self, deck):
        return super().draw_cards(deck)

    def show_hand(self, hidden=False):
        return super().show_hand(hidden=True)
    
    def get_hand_value(self):
        return self.hand_value
    
    def check_hand(self):
        return super().check_hand()


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
        for i, player in enumerate(players):
            player_no = i + 1
            print(f'\n\nPlayer {player_no}')
            player_bets[player_no] = player.get_bet()
            player.draw_cards(deck)
            player.show_hand()
            player_blackjack, player_busted = player.check_hand()
        #return 0
        dealer = Dealer()
        print(f'\n\nDealer')
        dealer.draw_cards(deck)
        dealer.show_hand()
        dealer_blacjack, dealer_busted = dealer.check_hand()
        
        return 0
        if dealer_busted:
            player.player_won()
        elif dealer_blacjack:
            pass

        for ind, player in enumerate(players):
            if not player.get_ended_game():
                print(f'\n\nPlayer {ind+1}')
                player.show_hand()
                player.ask_for_card(deck)

        print(f'\n\nDealer')
        dealer.show_hand()
        while dealer.get_hand_value() < 17:
            print('\nDealer draws')
            dealer.draw_card(deck)
            dealer.show_hand()
            dealer.adjust_for_ace()
            end = dealer.check_hand()
            if end:
                dealer.set_ended_game()

        for ind, player in enumerate(players):
            if dealer.get_ended_game() or player.get_ended_game():
                continue
            print(f'\nPlayer {ind+1}')
            player.show_hand()
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
