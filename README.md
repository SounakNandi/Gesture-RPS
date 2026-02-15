# 🖐️ Gesture-RPS

Classic **Rock Paper Scissors** game powered by AI Hand Gesture Recognition.

## 🌟 Key Features

- **UI**: A modern, dark-themed interface built with PyQt6.
- **Real-time Hand Tracking**: Advanced hand-gesture detection using MediaPipe.
- **Intelligent AI**: Competitive computer moves to challenge the player.
- **On-Screen Feedback**: Real-time visual cues for detected gestures and countdowns.

### 🏁 Game Controls (Gesture-Based)

| Action          | Gesture            | Description                                             |
| :-------------- | :----------------- | :------------------------------------------------------ |
| **Start Round** | ☝️ (Index Finger)  | Hold for **2 seconds** to begin the countdown.          |
| **Reset Game**  | 🤙 (Thumb & Pinky) | Hold for **2 seconds** to clear scores (only if > 0-0). |

## 🚀 Getting Started

### 📦 Prerequisites

- Python 3.10+
- A working Webcam

### 🛠️ Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/SounakNandi/Gesture-RPS.git
    cd Gesture-RPS
    ```

2.  **Create a virtual environment (recomended)**:

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 🏃 Launch the app

```bash
python app.py
```

## 📂 Project Structure

- `app.py`: The main entry point for the modern PyQt6 application.
- `logic.py`: The core engine handling gesture detection and game rules.
- `requirements.txt`: List of necessary Python packages.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Made with ❤️ by some cool guy [SOUNAK NANDI](https://github.com/SounakNandi)
