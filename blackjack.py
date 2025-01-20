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
        self.blackjack = 0
        self.busted = 0
        self.needs_card = True
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

    def __str__(self, card) -> str:
        return card.__str__()
    
    def show_hand(self, newline=True, hidden=False):
        hand = self.hand
        #print('here_player', hidden)
        if hidden:
            #only showing the 2nd card of the dealer
            print('Hidden card')
            hand = [self.hand[1]]
        for card in hand:
            print(self.__str__(card))
        if not hidden:
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
        if not self.blackjack:
            while True:
                response = input("\nDo you want a card? Press 'y' or 'n': ")
                if response == 'y':
                    self.draw_card(deck)
                    self.show_hand()
                    self.adjust_for_ace()
                    self.check_hand()
                    if self.blackjack or self.busted:
                        break
                else:
                    break
    
    def adjust_for_ace(self):
        if self.hand_value > 21 and self.has_ace:
            self.hand_value -= 10

    def check_hand(self):
        #end = 0 
        if self.hand_value == 21:
            #print('Congratulations! Blackjack')
            self.blackjack = 1
            #self.needs_card = False
        elif self.hand_value > 21:
            #print('Busted')
            self.busted = 1
            #self.needs_card = False
        return self

    def show_chips(self):
        print(f'Player has {self.chips}')


class Dealer(Player):
    def show_hand(self, hidden):
        return super().show_hand(hidden=hidden)
    
    def get_hand_value(self):
        return self.hand_value
    

def compare_hands(player : Player, dealer : Dealer, initial_check=True):
    # end = 0
    # if initial_check:
    #     if player.blackjack or player.busted:
    #         #print('Plyer has blackjack!')
    #         #player.chips += player.bet
    #         end = 1
    #     elif player.busted:
    #         #print('Player busted')
    #         #player.chips -= player.bet
    #         end = 1
    # else:
    if player.blackjack and dealer.blackjack:
        print('It\'s a tie!')
    elif player.blackjack:
        print('Player has blackjack!')
        player.chips += player.bet
    elif dealer.blackjack:
        print('Dealer has blackjack!')
        player.chips -= player.bet
    elif player.busted:
        print('Player busted')
        player.chips -= player.bet
    elif dealer.busted:
        print('Dealer busted!')
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
            player.check_hand()
        
        dealer = Dealer()
        print(f'\n\nDealer')
        dealer.draw_cards(deck)
        dealer.show_hand(hidden=True)
        dealer.check_hand()
        
        for i, player in enumerate(players):
            player_no = i + 1
            print(f'\n\nPlayer {player_no}')
            player.show_hand()
            player.check_hand()
            
            player.ask_for_card(deck)

            print(f'\n\nDealer')
            dealer.show_hand(hidden=False)
            while dealer.get_hand_value() < 17:
                print('\nDealer draws')
                dealer.draw_card(deck)
                dealer.show_hand(hidden=False)
                dealer.adjust_for_ace()
                dealer.check_hand()

            for ind, player in enumerate(players):
                print(f'\nPlayer {ind+1}')
                player.show_hand()
                compare_hands(player, dealer)
                player.show_chips()
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
