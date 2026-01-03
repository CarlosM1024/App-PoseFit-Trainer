# 🏋️ App-PoseFit-Trainer
### *AI-Powered Fitness Pose Estimation & Biometric Analysis*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/Framework-MediaPipe-00C853.svg)](https://mediapipe.dev/)
[![OpenCV](https://img.shields.io/badge/Library-OpenCV-white.svg?logo=opencv&logoColor=white)](https://opencv.org/)

## 📝 Overview
**App-PoseFit-Trainer** is a Computer Vision solution designed to analyze and monitor human posture during physical training. By leveraging advanced Deep Learning models, the system detects 33 key body landmarks and calculates real-time biometric angles to help users improve their technique and prevent injuries.



### ✨ Key Features
- **🏋️ Real-time Pose Detection**: AI-powered analysis of exercise form using MediaPipe
- **📊 Form Correction**: Instant feedback on posture, alignment, and technique
- **🔢 Repetition Counter**: Automated counting for various exercises


## 📁 Project Structure

```text
App-PoseFit-Trainer/
├── app_PoseFit_Trainer/  # Core application logic
├── pose_projects/        # Experimental scripts and detection modules
│   └── PoseModule.py     # Main class for detection and angle calculation
├── assets/               # Sample videos and visual resources
├── LICENSE               # MIT License
└── README.md             # Project documentation
```

## 🚀 Getting Started

### Prerequisites
* **Python 3.9**
* **Webcam (for live analysis)**
  
### Installation
1. Clone the repository:

````bash
git clone [https://github.com/CarlosM1024/App-PoseFit-Trainer.git](https://github.com/CarlosM1024/App-PoseFit-Trainer.git)
cd App-PoseFit-Trainer
````

2. Create and activate a virtual environment:
````bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
````

3. Install dependencies:
````bash
pip install -r requirements.txt
````


## 🛠️ Usage

To execute App-PoseFit-Trainer:

````Bash
python app.py
````


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🤝 Contributing

If you'd like to contribute to this project, feel free to submit a pull request. Please make sure your code follows the existing style and includes appropriate comments.

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Commit your changes.
4.  Push to the branch.
5.  Submit a pull request.

## 👤 Author

**Carlos Antonio Martinez Miranda**

GitHub: [@CarlosM1024](https://github.com/CarlosM1024)
