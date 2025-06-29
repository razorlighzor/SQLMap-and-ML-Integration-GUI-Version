Project Description:
A hybrid web security assessment tool designed to detect SQL Injection (SQLi) vulnerabilities using both AI-based machine learning analysis and the industry-standard SQLMap engine.

Built for cybersecurity professionals, penetration testers, and web app security teams, this tool combines the speed of machine learning classification with the depth of traditional penetration testing, all within an easy-to-use graphical interface (GUI).

Features:

Machine Learning detection engine (default: Random Forest)
SQLmap integration for CLI-level testing
Fallback execution from ML to SQLmap if ML fails
Batch URL testing
Session cookie handling for authenticated targets
Logging of test results for analysis

This tool is intended for ethical security testing. Usage against targets without explicit permission is strictly prohibited.

Project Structure:
project/
├── GUI/
│   ├── SQLiGUI.py             # Main GUI script
│   ├── ml_module_handler.py   # ML model loader/predictor
│   ├── dynamic_trainer.py     # Optional retraining script
│   └── modelfile/
│       ├── best_random_forest_full.pkl
│       └── tfidf_vectorizer.pkl
├── sqlmap/                     # Cloned SQLMap repo (required)
│   └── sqlmap.py
└── logs/                       # Auto-generated test logs

Prerequisites:
✅ Python 3.11+
✅ SQLmap (cloned into sqlmap/ folder)
✅ Required Python packages:
pip install -r requirements.txt

scikit-learn
pandas
numpy
joblib
tkinter

Trained model files (placed in modelfile/):
best_random_forest_full.pkl


1. Clone this repository (including SQLmap): git clone https://github.com/YourUsername/SQLMap-and-ML-Integration-GUI-Version.git
2. Download or clone SQLmap and place it inside the sqlmap/ folder:
project/
└── sqlmap/
    └── sqlmap.py
3. Verify that modelfile/ contains: best_random_forest_full.pkl

How to Run:
1. Initiate the script using the bash file provided in the repository
2. or:
a. cd GUI
b. python SQLiGUI.py/py SQLiGUIpy

How to Use:
1. Main Window
> Operate with Machine Learning Feature: Launches ML Mode for single URL detection
> Operate as Normal Engine: Launches SQLmap-only mode
> Open Batch Mode: Supports batch URL testing
> View Previous Result: Opens saved logs

2. ML Mode:
> Input a target URL.
> Select a trained model (default Random Forest provided).
> Optional: Enable fallback to SQLmap if ML detection fails.
> Click Operate with Machine Learning.
✅ Result:
> Result shown in Result Window.
> Saved automatically in /logs with timestamp.

3. SQLmap Mode
> Input a target URL.
> Choose optional SQLmap parameter (e.g. --dbs, --tables).
> Optional: Input session cookie for authenticated scans.
> Click Run SQLmap.
✅ Result:
> Real SQLmap CLI output displayed in GUI.
> Saved to /logs.

4. Batch Mode
> Paste multiple URLs (one per line).
> Optional: Input a shared session cookie for authenticated testing.
> Click Run ML on Batch or Run SQLmap on Batch.
✅ Result:
> Each URL tested in order.
> Consolidated results saved in /logs.

Logging
> Logs saved as .txt files in /logs folder.
> Contains detection results, including cookies if entered.
Warning: Session cookies are stored in plaintext. Secure the logs folder!

Notes and Recommendations:
> The tool uses SQLmap CLI as a subprocess; make sure sqlmap.py is present.
> CAPTCHA, WAF, and multi-factor login may limit SQLmap effectiveness.
> ML model provides fast first-line filtering; SQLmap gives deep validation.
> For advanced use: retrain your ML model using dynamic_trainer.py with your own dataset.

Future improvements may include:
> Encrypted log files
> User authentication for the GUI
> Real-time web app integration

