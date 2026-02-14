# 🖐️ Gesture-RPS

Rock Paper Scissors game using Object Detection (Hand Tracking) with OpenCV and MediaPipe.

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

- `app.py`: Main application script with UI and core logic.
- `assets/`: Directory containing game resources and assets.
- `requirements.txt`: Project dependencies.

## Credits

Made with ❤️ by some cool guy [SOUNAK NANDI](https://github.com/SounakNandi)
