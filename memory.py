# implementation of card game - Memory
import simpleguitk as simplegui
# import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards_deck, card, exposed, state, counter
    
    state=0
    card = 0
    lst0 = range(8)
    lst1 = range(8)
    cards_deck = lst0 + lst1  
    random.shuffle(cards_deck)
    exposed = [False, False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    counter=0
    label.set_text("Turns = " + str(counter))
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global card_index, exposed, first_card, second_card, counter, state
    card_index = pos[0] // 50
    
    if state == 0:
        exposed[card_index]=True
        counter+=1
        label.set_text("Turns = " + str(counter))
        first_card = card_index
        state = 1
    elif state == 1:
        exposed[card_index]=True
        second_card = card_index
        state = 2
        
    else:
        if cards_deck[first_card] != cards_deck[second_card]:
            exposed[first_card]=exposed[second_card]=False
        state = 0
    
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards_deck, exposed
    for card_index in range(len(exposed)):
        card_pos = 50 * card_index
        if exposed[card_index]==True:
            canvas.draw_text(str(cards_deck[card_index]), (card_pos+5,75) , 70, "White")
        else:
            canvas.draw_polygon([[card_pos,0], [card_pos,100], [50+card_pos,100], [card_pos+50,0]], 1, "Black", "Green")
     
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


