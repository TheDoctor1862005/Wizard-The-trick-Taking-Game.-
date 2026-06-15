from itertools import product 
from random import shuffle
import random

player_name = input("Please input your name ").lower().strip()

# Setup
Suits = ["\033[32mElves\033[0m", "\033[33mGiants\033[0m", "\033[31mDwarves\033[0m", "\033[36mHumans\033[0m"] 
Ranks = [1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 ] 
Special = ["The Wizard", "The Jester"]
Special_Ranks = [""]


#Card to Text
def card_to_text(card):
    rank, suit = card
    if rank == "":
        return suit
    else:
        return f"{rank} of {suit}"

def winner_to_text(card):
    rank, suit = card
    if rank == "":
        return suit
    else:
        return f"{rank} with {suit} points"

#Deck Creation
deck = list(product(Ranks, Suits)) 
for i in range(4):
    deck = deck + list(product(Special_Ranks, Special)) 

shuffle(deck) 


#Draw
remaining_cards = list(deck)
hand = []
def draw(number, hand):
    for i in range(0, number):
        card_drawn = random.choice(remaining_cards)
        remaining_cards.remove(card_drawn)
        hand.append(card_drawn)


#Figures out Suit
def suit_only(card):
    rank, suit = card
    return suit

#converts full hand to text
def hand_to_text(hand, player=False):
    cards_text = []
    number = str(1) 
    for card in hand:
        if player:
            cards_text.append(card_to_text(card) + " " + f"\033[34m{number}\033[0m")
        else:
            cards_text.append(card_to_text(card))
        number = int(number) + 1
        number = str(number)
    return ", ".join(cards_text)


#Start round
def start_round(round, hand, jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand):
    print(f"\nROUND {round}! BEGIN")
    if round == 1:
        print("\nYou have 5 opponents. Jimmy, Lily, Ian, Infant, and Clandriagresvangolls (Clan)")
    for person in [hand, jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand]:
        draw(round, person)


#Matchs cards in hands to card played
def match(hand, suit):
    matchs = []
    for card in hand:
        temp_type = card[1]
        if temp_type == suit:
            matchs.append(card)
    if matchs:
        matchs = max(matchs, key=lambda card: card[0]) 
        hand.remove(matchs)
    if not matchs:
        for card in hand:
            if card[1] == "The Wizard":
                matchs = card
                break
        for card in hand:
            if card[1] == "The Jester":
                matchs = card
                break
        if not matchs:
            matchs = min(hand, key=lambda card: card[0])
        hand.remove(matchs)
    return(matchs)

    


#Takes the Trick
def take_trick(round, hand, jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand, play_card, points):
    play_card = play_card - 1
    play_card = hand[play_card]
    suit = play_card[1]
    hand.remove(play_card)
    plays = []
    #Determines what opponents play.
    for person, held_cards in zip(players[1:], [jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand]):
        played = match(held_cards, suit)
        plays.append(played)
        print(f"\n{person} plays {card_to_text(played)}")
    wizards = 0
    jesters = 0
    alike = 0
    diffrent = 0
    same_suiters = []
    for name, play in zip(players[1:], plays):
        if play[1] == "The Wizard":
            wizards += 1
        elif play[1] == "The Jester":
            jesters += 1
        elif play[1] == play_card[1]:
            alike += 1
            same_suiters.append((name, play[0]))
        else:
            diffrent += 1

    plays.insert(0, play_card)
    winner = ""
    for name, card in zip(players, plays):
        if card[1] == "The Wizard":
            winner = name
            break
    if winner != "":
        if winner == "Player":
            print(f"\nYou Win!")
        else:
            print(f"\n{winner} Wins!")
    else:
        if same_suiters:
            winner = max(same_suiters, key=lambda same_suiters: same_suiters[0])[0]
        else:
            winner = "Player"
        if winner == "Player":
            print("\nYou Win!")
        else:
            print(f"\n{winner} Wins!")
    #adds points to winner
    for number, character in enumerate(players):
        if winner == character:
            points[number] += 1
    return(points)
        
            
    


    
    



#Plays the round
def play(round, hand, jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand, points):
    if round == 1:
        print("\nTo pick a card type the purple number corresponding to card you wish to play.")
    while True:
        while True:
            try:
                if len(hand) == 0:
                    break
                #Pick your card to play this trick
                while True:
                    try:
                        play_card = int(input(f"\nPick your card to play from {hand_to_text(hand, True)}: "))
                        if play_card == "":
                            print("\nPlease input a number")
                        else:
                            play_card = int(play_card)
                        break
                    except:
                        print("\nPlease input a number")
                    
            except:
                print("\nPlease input a number")
    
            if play_card > len(hand):
                print("\nTo high a number.")
            elif play_card < 1:
                print("\n Please select a actual number")
            else:
                points = take_trick(round, hand, jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand, play_card, points)

        if len(hand) == 0:
            break
    return points



#Actual Game code
round = 1
players = ['\033[0mPlayer\033[0m', '\033[36mJimmy\033[0m', '\033[95mLily\033[0m', '\033[38;5;208mIan\033[0m', '\033[94mInfant\033[0m', '\033[90mClandriagresvangoll\033[0m']
points = [0, 0, 0, 0, 0, 0]
while True:
    if round >= 11:
        break
    else:
        deck = list(product(Ranks, Suits)) 
        for i in range(4):
            deck = deck + list(product(Special_Ranks, Special)) 
        shuffle(deck) 
        remaining_cards = list(deck)
        hand = []
        jimmys_hand = []
        lilys_hand = []
        ians_hand = []
        infants_hand = []
        clandriagresvangolls_hand = []
        start_round(round, hand, jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand)
        for person, held_cards in zip(players[1:], [jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand]):
            print(f"{person} hand: {hand_to_text(held_cards)}")
        points = play(round, hand, jimmys_hand, lilys_hand, ians_hand, infants_hand, clandriagresvangolls_hand, points)
        round += 1

# Determins winner and prints everybodys points. 
for player, score in zip(players, points):
    if score >= 1:
        if player == '\033[0mPlayer\033[0m':
            print(f"\nYou got {score} {'point' if score == 1 else 'points'}")
        else:
            print(f"\n{player} got {score} {'point' if score == 1 else 'points'}")
    
winner = max(zip(points, players))[1]
if winner == '\033[0mPlayer\033[0m':
    print(f"\nCongrats {player_name} you win")
else:
    print(f"\nThe grand winner is {winner}")
