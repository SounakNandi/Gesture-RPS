import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import random
import pymsgbox

run = True
game_started = False
time_started = False
check_now = False
player_choice = None
max_time = 4
game_list = ['rock','paper','scissors']
ai_score = 0
player_score = 0

webcam = cv2.VideoCapture(0)
webcam.set(3, 640)#width
webcam.set(4, 480)#height

detector = HandDetector(maxHands=1)

bg_img = cv2.imread('Pictures\\Rock_Paper_Scissors_bg.png')
rock = cv2.imread('Pictures\\hand_rock.png')
paper = cv2.imread('Pictures\\hand_paper.png')
scissors = cv2.imread('Pictures\\hand_scissors.png')
three = cv2.imread('Pictures\\3.png')
two = cv2.imread('Pictures\\2.png')
one = cv2.imread('Pictures\\1.png')
zero = cv2.imread('Pictures\\0.png')
shoot = cv2.imread('Pictures\\shoot !!.png')

def draw_screen():
    global img_scaled

    success, img = webcam.read()
    img_scaled = cv2.resize(img,(0,0),None,0.8125,0.8125)
    img_scaled = img_scaled[:,90:430]

    hand_detection()

    if current_time == 3:
        bg_img[240:390, 425:575] = three
    elif current_time == 2:
        bg_img[240:390, 425:575] = two
    elif current_time == 1:
        bg_img[240:390, 425:575] = one
    elif current_time == 0:
        bg_img[240:390, 425:575] = shoot
    
    bg_img[155:545, 605:945] = img_scaled

    cv2.imshow('BG',bg_img)  

def time_counter():
    global current_time,start_time,time_started,max_time,check_now

    current_time = max_time
    if game_started:
        current_time = int(max_time-(time.time()-start_time))

        if current_time < 0:
            start_time = time.time()
            check_now = True

def key_press_event():
        global game_started,run,time_started,start_time

        key = cv2.waitKey(1)
        if key == ord(' '):
            game_started = True
            time_started = True
            start_time = time.time()

        if key == ord('q'):
            cv2.destroyAllWindows()
            run = False

def hand_detection():
    global img_scaled,game_started,player_choice,check_now

    hands, img = detector.findHands(img_scaled)

    if game_started:
        if check_now:
            if hands:
                hand = hands[0]
                fingers_up = detector.fingersUp(hand)

                if fingers_up == [0,1,1,0,0]:
                    player_choice = 'scissors'
                elif fingers_up == [0,0,0,0,0]:
                    player_choice = 'rock'
                elif fingers_up == [1,1,1,1,1]:
                    player_choice = 'paper'
                else :
                    player_choice = None

                win_condition()
                check_now = False    

def win_condition():
    global ai_choice,player_choice,player_score,ai_score,bg_img,check_now

    if check_now :
        ai_choice = random.choice(game_list)
        print(ai_choice,player_choice)

        if ai_choice == 'rock':
            bg_img[275:425,150:300] = rock
        if ai_choice == 'paper':
            bg_img[275:425,150:300] = paper
        if ai_choice == 'scissors':
            bg_img[275:425,150:300] = scissors

        if player_choice == 'paper':
            if ai_choice == 'rock':
                player_score += 1
            elif ai_choice == 'scissors':
                ai_score += 1

        elif player_choice == 'rock':
            if ai_choice == 'scissors':
                player_score += 1
            elif ai_choice == 'paper':
                ai_score += 1

        elif player_choice == 'scissors':
            if ai_choice == 'paper':
                player_score += 1
            elif ai_choice == 'rock':
                ai_score += 1
        print(ai_score,player_score)
                
def score_counter():
    global zero_scaled

    zero_scaled = cv2.resize(zero,(0,0),None,0.6,0.6)
    one_scaled = cv2.resize(one,(0,0),None,0.6,0.6)
    two_scaled = cv2.resize(two,(0,0),None,0.6,0.6)
    three_scaled = cv2.resize(three,(0,0),None,0.6,0.6)
    
    if ai_score == 0:
        bg_img[60:150,305:395] = zero_scaled
    elif ai_score == 1:
        bg_img[60:150,305:395] = one_scaled
    elif ai_score == 2:
        bg_img[60:150,305:395] = two_scaled
    elif ai_score == 3:
        bg_img[60:150,305:395] = three_scaled

    if player_score == 0:
        bg_img[60:150,605:695] = zero_scaled
    elif player_score == 1:
        bg_img[60:150,605:695] = one_scaled
    elif player_score == 2:
        bg_img[60:150,605:695] = two_scaled
    elif player_score == 3:
        bg_img[60:150,605:695] = three_scaled

def end_screen():
    global run,ai_score,player_score

    if ai_score == 3 :
        end = pymsgbox.alert("AI Won","Game Over")
        if end == 'OK':
            cv2.destroyAllWindows()
            run = False
    elif player_score == 3:
        end = pymsgbox.alert("You Won","Game Over")
        if end == 'OK':
            cv2.destroyAllWindows()
            run = False
        
def main():
    while run:
        time_counter()
        draw_screen()
        score_counter()
        key_press_event()
        end_screen()

if __name__ == '__main__':
    main()
