import simpleguitk as simplegui
# Mini-project #6 - Blackjack

# import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_hand = []
dealer_hand = []
playerPos = (50, 400)
dealerPos = (50, 200)
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
            # create Hand object
        self.my_hand = []
        

    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for i in range(len(self.my_hand)):
            ans = ans + " " + str(self.my_hand[i])
        return ans

    def add_card(self, card):
        # add a card object to a hand
        return self.my_hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.hand_value = 0
        self.has_ace = False
        for r in self.my_hand:
            self.card_value = VALUES[r.get_rank()]
            self.hand_value += self.card_value
            if r.get_rank() == "A":
                self.has_ace = True
        if not self.has_ace:
            return self.hand_value
        else:
            if self.hand_value + 10 > 21:
                return self.hand_value
            else:
                return self.hand_value + 10
                
       
    def draw(self, canvas, pos):
            # draw a hand on the canvas, use the draw method for cards
        
        for card in self.my_hand:
            card.draw(canvas, pos)
            pos = pos[0]+100, pos[1]
            
        
# define deck class 
class Deck:
    def __init__(self):
            # create a Deck object
        self.my_deck = []
        for suit in SUITS:
            for rank in RANKS:
                new_card = Card(suit, rank)
                self.my_deck.append(new_card)

    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.my_deck)

    def deal_card(self):
            # deal a card object from the deck
        return self.my_deck.pop(-1)
    
    def __str__(self):
            # return a string representing the deck
        ans = "Deck contains"
        for card in range(len(self.my_deck)):
            ans = ans + " " + str(self.my_deck[card])
        return ans        



#define event handlers for buttons
def deal():
    global outcome, in_play, new_deck, player_hand, dealer_hand, score
    
    # your code goes here
    new_deck = Deck()
    new_deck.shuffle()
    if in_play:
        score -= 1
    in_play = True
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range(2):
        dealer_hand.add_card(new_deck.deal_card())
        player_hand.add_card(new_deck.deal_card())
    outcome = "Hit or Stand?"
    return player_hand, dealer_hand
    
def hit():
    global new_deck, player_hand, outcome, score, in_play
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(new_deck.deal_card())
        if player_hand.get_value() > 21:
            in_play = False
            outcome = "Player " + str(player_hand.get_value()) + ". You have busted. Deal again?"
            score -= 1
       
def stand():
    global in_play, player_hand, dealer_hand, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(new_deck.deal_card())
        in_play = False
        if dealer_hand.get_value() > 21 or dealer_hand.get_value() < player_hand.get_value():
            outcome = "Player " + str(player_hand.get_value()) + ". Dealer " + str(dealer_hand.get_value()) + ". You win! Deal again?"
            score += 1
        else:
            outcome = "Player " + str(player_hand.get_value()) + ". Dealer " + str(dealer_hand.get_value()) + ". You lost! Deal again?"
            score -= 1
    
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global playerPos, dealerPos
    # test to make sure that card.draw works, replace with your code below
    player_hand.draw(canvas, playerPos)
    dealer_hand.draw(canvas, dealerPos)
    canvas.draw_text("Dealer", (50,175), 50, "Black")
    canvas.draw_text("Player", (50,375), 50, "Black")
    canvas.draw_text("Blackjack", (50,75), 75, "Grey")
    canvas.draw_text("Score: " + str(score), (450, 75), 30, "Black")
    canvas.draw_text(outcome, (200, 375), 22, "Red")
    if in_play:
         if in_play==True:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [86, 248], CARD_BACK_SIZE)


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


