# SQLmap And ML Integration in GUI
## Project Description:
A hybrid web security assessment tool designed to detect SQL Injection (SQLi) vulnerabilities using both AI-based machine learning analysis and the industry-standard SQLMap engine.

Built for cybersecurity professionals, penetration testers, and web app security teams, this tool combines the speed of machine learning classification with the depth of traditional penetration testing, all within an easy-to-use graphical interface (GUI).

## Features:

1. Machine Learning detection engine (default: Random Forest)
2. SQLmap integration for CLI-level testing
3. Fallback execution from ML to SQLmap if ML fails
4. Batch URL testing
5. Session cookie handling for authenticated targets
6. Logging of test results for analysis
</br>
This tool is intended for ethical security testing. Usage against targets without explicit permission is strictly prohibited.

## Project Structure:
project/
</br>├── GUI/
</br>│   ├── SQLiGUI.py             ```# Main GUI script```
</br>│   ├── ml_module_handler.py   ```# ML model loader/predictor```
</br>│   ├── dynamic_trainer.py     ```# Optional retraining script```
</br>│   └── modelfile/
</br>│       ├── best_random_forest_full.pkl
</br>│       └── tfidf_vectorizer.pkl
</br>├── sqlmap/                     ```# Cloned SQLMap repo (required)```
</br>│   └── sqlmap.py
</br>└── logs/                       ```# Auto-generated test logs```
## Prerequisites:
1. ✅ Python 3.11+
2. ✅ SQLmap (cloned into sqlmap/ folder)
3. ✅ Required Python packages:
```pip install -r requirements.txt```

### requirements.txt:
```scikit-learn, pandas, numpy, joblib, tkinter```

Trained model files (placed in modelfile/):
```best_random_forest_full.pkl```


1. Clone this repository (including SQLmap): git clone https://github.com/YourUsername/SQLMap-and-ML-Integration-GUI-Version.git
2. Download or clone SQLmap and place it inside the sqlmap/ folder:</br>
project/</br>
└── sqlmap/
</br> └── sqlmap.py
4. Verify that modelfile/ contains: **best_random_forest_full.pkl**

## How to Run:
1. Initiate the script using the bash file provided in the repository
2. or:</br>
a. cd GUI</br>
b. python SQLiGUI.py/py SQLiGUIpy

## How to Use:
### 1. Main Window
1. Operate with Machine Learning Feature: Launches ML Mode for single URL detection
2. Operate as Normal Engine: Launches SQLmap-only mode
3. Open Batch Mode: Supports batch URL testing
4. View Previous Result: Opens saved logs

### 2. ML Mode:
1. Input a target URL.
2. Select a trained model (default Random Forest provided).
3. Optional: Enable fallback to SQLmap if ML detection fails.
4. Click Operate with Machine Learning.
✅ Result:
1. Result shown in Result Window.
2. Saved automatically in /logs with timestamp.

### 3. SQLmap Mode
1. Input a target URL.
2. Choose optional SQLmap parameter (e.g. --dbs, --tables).
3. Optional: Input session cookie for authenticated scans.
4. Click Run SQLmap.
✅ Result:
1. Real SQLmap CLI output displayed in GUI.
2. Saved to /logs.

### 4. Batch Mode
1. Paste multiple URLs (one per line).
2. Optional: Input a shared session cookie for authenticated testing.
3. Click Run ML on Batch or Run SQLmap on Batch.
✅ Result:
1. Each URL tested in order.
2. Consolidated results saved in /logs.

## Logging
1. Logs saved as .txt files in /logs folder.
2. Contains detection results, including cookies if entered.
3. **Warning: Session cookies are stored in plaintext. Secure the logs folder!**

## Notes and Recommendations:
1. The tool uses SQLmap CLI as a subprocess; make sure sqlmap.py is present.
2. CAPTCHA, WAF, and multi-factor login may limit SQLmap effectiveness.
3. ML model provides fast first-line filtering; SQLmap gives deep validation.
4. For advanced use: retrain your ML model using dynamic_trainer.py with your own dataset.

Future improvements may include:
1. Encrypted log files
2. User authentication for the GUI
3. Real-time web app integration

## Dataset:
Dataset can be collected here in case users want to create their own ML: </br>
https://www.kaggle.com/code/iniestamoh/eda-sql-injection-dataset/notebook
