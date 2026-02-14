# Rock_Paper_Scissors_Object_Detection

Rock Paper Scissors game using Object Detection (Hand Tracking) with OpenCV and MediaPipe.

## Features

- Real-time gesture recognition (Rock, Paper, Scissors).
- Modern GUI using PyQt6.
- Interactive status bars and score tracking.
- Touchless controls (Start/Reset via gestures).

## Installation

```bash
git clone https://github.com/SounakNandi/Gesture-RPS.git
cd Gesture-RPS
pip install -r requirements.txt
```

## Running the Game

```bash
python app.py
```

## How it Works

The system uses the `HandTrackingModule` from `cvzone` to detect the number of fingers up and maps them to gestures:

- **Rock**: 0 fingers
- **Paper**: 5 fingers
- **Scissors**: 2 fingers (Index and Middle)

## Project Structure

- `app.py`: Modern PyQt6 UI version.
- `logic.py`: Core game engine and gesture processing.
- `requirements.txt`: Project dependencies.

---

Developed by [SOUNAK NANDI](https://github.com/SounakNandi)
