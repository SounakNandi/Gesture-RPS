import cv2
import random
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from PIL import Image, ImageDraw, ImageFont

class RPSGameLogic:
    def __init__(self):
        self.detector = HandDetector(maxHands=1, detectionCon=0.8)
        self.gestures = {
            "ROCK ✊": [(0, 0, 0, 0, 0), (1, 0, 0, 0, 0)],
            "PAPER ✋": [(1, 1, 1, 1, 1), (0, 1, 1, 1, 1), (1, 1, 1, 1, 0), (1, 1, 0, 0, 0)],
            "SCISSORS ✌️": [(0, 1, 1, 0, 0), (1, 1, 1, 0, 0), (0, 1, 1, 1, 0)]
        }
        self.choices = ["ROCK ✊", "PAPER ✋", "SCISSORS ✌️"]
        
        # Game State
        self.player_score = 0
        self.ai_score = 0
        self.current_round_result = ""
        self.player_move = None
        self.ai_move = None
        
        # Timing
        self.countdown_start = 0
        self.is_counting_down = False
        self.countdown_duration = 3

        self.hold_start_time = 0
        self.gesture_being_held = None
        self.trigger_duration = 2.0
        
    def get_gesture(self, hands):
        if not hands:
            return None
        hand = hands[0]
        fingers = tuple(self.detector.fingersUp(hand))
        for gesture, patterns in self.gestures.items():
            if fingers in patterns:
                return gesture
        return "UNKNOWN ❓"

    def start_round(self):
        self.countdown_start = time.time()
        self.is_counting_down = True
        self.current_round_result = "Prepare!"
        self.player_move = None
        self.ai_move = None

    def draw_text_pil(self, frame, text, position, color=(255, 255, 255)):
        try:
            # Convert OpenCV image (BGR) to PIL image (RGB)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            draw = ImageDraw.Draw(pil_img)
            
            try:
                # Segoe UI Emoji for Windows
                font = ImageFont.truetype("seguiemj.ttf", 36)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", 36)
                except:
                    font = ImageFont.load_default()
            
            # Shadow for readability
            draw.text((position[0]+2, position[1]+2), text, font=font, fill=(0,0,0))
            draw.text(position, text, font=font, fill=color)
            
            # Convert back to BGR for OpenCV
            return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"PIL Draw Error: {e}")
            return frame

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        hands, frame = self.detector.findHands(frame, draw=True, flipType=False)
        
        status_text = ""
        countdown_val = 0
        display_label = ""
        label_color = (255, 255, 255) # White
        
        if hands:
            hand = hands[0]
            fingers = tuple(self.detector.fingersUp(hand))
            bbox = hand['bbox']
            
            # Gesture detection
            current_detected = "NONE"
            if fingers == (1, 0, 0, 0, 1):
                current_detected = "RESETTING 🤙"
            elif fingers == (0, 1, 0, 0, 0):
                current_detected = "STARTING ☝️"
            else:
                for gesture, patterns in self.gestures.items():
                    if fingers in patterns:
                        current_detected = gesture
                        break
            
            display_label = current_detected

            # Hold logic for START/RESET
            if current_detected in ["STARTING ☝️", "RESETTING 🤙"] and not self.is_counting_down:
                # No reset needed if already 0-0
                if current_detected == "RESETTING 🤙" and self.player_score == 0 and self.ai_score == 0:
                    status_text = "SCORE IS ALREADY 0-0"
                    self.gesture_being_held = None
                    self.hold_start_time = 0
                else:
                    if self.gesture_being_held != current_detected:
                        self.gesture_being_held = current_detected
                        self.hold_start_time = time.time()
                    
                    elapsed = time.time() - self.hold_start_time
                    remaining = max(0, self.trigger_duration - elapsed)
                    
                    # Timer feedback to status bar
                    status_text = f"{current_detected} IN {remaining:.1f}s"
                    
                    label_color = (0, 255, 255) # Yellowish
                    
                    if elapsed >= self.trigger_duration:
                        if current_detected == "STARTING ☝️":
                            self.start_round()
                        else:
                            self.reset_game()
                        self.gesture_being_held = None
                        self.hold_start_time = 0
            else:
                self.gesture_being_held = None
                self.hold_start_time = 0

            # PIL label (supports emojis)
            text_y = bbox[1] + bbox[3] + 10
            if text_y > h - 50: text_y = bbox[1] - 50
            frame = self.draw_text_pil(frame, display_label, (bbox[0], text_y), label_color)

        # Game countdown
        if self.is_counting_down:
            elapsed = time.time() - self.countdown_start
            countdown_val = self.countdown_duration - int(elapsed)
            if countdown_val <= 0:
                self.is_counting_down = False
                self.ai_move = random.choice(self.choices)
                self.player_move = self.get_gesture(hands)
                self.evaluate_round()
            else:
                status_text = f"Show hand in {countdown_val}..."
        
        if not status_text and not self.is_counting_down:
            status_text = self.current_round_result if self.current_round_result else "Show ☝️ to Start | Show 🤙 to Reset"

        return frame, status_text, countdown_val

    def evaluate_round(self):
        if self.player_move == "UNKNOWN ❓" or self.player_move is None:
            self.current_round_result = "Invalid move! Try again."
            return

        p = self.player_move
        a = self.ai_move

        if p == a:
            self.current_round_result = f"TIE! BOTH CHOSE {p}"
        elif (p == "ROCK ✊" and a == "SCISSORS ✌️") or \
             (p == "PAPER ✋" and a == "ROCK ✊") or \
             (p == "SCISSORS ✌️" and a == "PAPER ✋"):
            self.player_score += 1
            self.current_round_result = f"YOU WIN! {p} BEATS {a}"
        else:
            self.ai_score += 1
            self.current_round_result = f"AI WINS! {a} BEATS {p}"

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.current_round_result = ""
        self.player_move = None
        self.ai_move = None
        self.is_counting_down = False
