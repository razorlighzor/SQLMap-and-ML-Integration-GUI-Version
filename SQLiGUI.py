import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import os
import pandas as pd
import subprocess
from datetime import datetime
import ml_module_handler

selected_model_path = "modelfile/best_random_forest_full.pkl"
modelfile_path = "modelfile/"
batchfile_path = "batchURLs/"
logfile_path = "logs/"
# --- Helper Functions ---

def open_ml_mode():
    main_window.withdraw()
    ml_window.deiconify()

def open_sqlmap_mode():
    main_window.withdraw()
    sqlmap_window.deiconify()

def open_batch_mode():
    main_window.withdraw()
    batch_window.deiconify()

def open_batch_input_mode():
    main_window.withdraw()
    batch_window.deiconify()

def cancel_operation():
    result_window.withdraw()
    main_window.deiconify()

def exit_application():
    main_window.destroy()

def select_model_file():
    global selected_model_path
    model_file = filedialog.askopenfilename(title="Select ML Model File", 
                                            filetypes=[("Pickle Files", "*.pkl")],
                                            initialdir=modelfile_path)
    if model_file:
        selected_model_path = model_file
        messagebox.showinfo("Model Selected", f"Model selected:\n{model_file}")
        status_label.config(text=f"Selected Model: {os.path.basename(model_file)}")
        load_msg = ml_module_handler.load_model(model_file)
        print(load_msg)

def execute_ml():
    url = ml_url_entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a website URL")
        return

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Analyzing URL with ML: {url}\n")
    result_text.see(tk.END)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/sqli_detection_{timestamp}.txt"
    os.makedirs("logs", exist_ok=True)

    try:
        prediction = ml_module_handler.predict_sqli(url)
        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(f"URL: {url}\n")
            if prediction == 1:
                msg = "Potential SQL Injection Detected!\n"
                result_text.insert(tk.END, msg)
                log_file.write(msg)
            elif prediction == 0:
                msg = "No SQL Injection Detected by ML.\n"
                result_text.insert(tk.END, msg)
                log_file.write(msg)
                if fallback_to_sqlmap.get():
                    result_text.insert(tk.END, "Running SQLmap fallback...\n")
                    log_file.write("Running SQLmap fallback...\n")
                    run_sqlmap_command(["python", "sqlmap/sqlmap.py", "-u", url, "--batch"], url, "ML fallback", log_file)
                    return
            else:
                msg = f"ML Prediction Error: {prediction}\n"
                result_text.insert(tk.END, msg)
                log_file.write(msg)
    except Exception as e:
        result_text.insert(tk.END, f"Error: {e}\n")

    result_text.see(tk.END)
    result_text.config(state=tk.DISABLED)

    result_window.deiconify()

def execute_sqlmap():
    url = sqlmap_url_entry.get().strip()
    option = sqlmap_options.get().strip()
    cookie = cookie_entry.get().strip()

    if not url:
        messagebox.showwarning("Input Error", "Please enter a website URL")
        return

    command = ["python", "sqlmap/sqlmap.py", "-u", url]
    if option:
        command.append(option)
    command.append("--batch")

    run_sqlmap_command(command, url, option if option else "default", cookie=cookie)

def run_sqlmap_command(command, url, option_used, log_file=None, cookie=None):
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Running SQLmap on {url} [{option_used}]\n\n")

    if cookie:
        command.extend(["--cookie", cookie])

    start = time.time()
    try:
        process = subprocess.run(command, capture_output=True, text=True, timeout=300)
        output = process.stdout if process.stdout else process.stderr
    except Exception as e:
        output = f"Error running SQLmap: {str(e)}"
    end = time.time()

    duration = end - start
    result_text.insert(tk.END, output + f"\n[Time: {duration:.2f}s]\n")
    result_text.config(state=tk.DISABLED)
    result_window.deiconify()

    if log_file:
        log_file.write(output + f"\n[Time: {duration:.2f}s]\n")


def save_batch_file():
    
    urls = batch_text.get("1.0", tk.END).strip().split('\n')
    if not urls or urls == ['']:
        messagebox.showwarning("Input Error", "Please enter URLs in the text box.")
        return

    os.makedirs("batchURLs", exist_ok=True)
    base_name = "batch_urls_"
    extension = ".txt"

    # Find the next available number
    existing_files = os.listdir("batchURLs")
    numbers = [
        int(f.replace(base_name, "").replace(extension, ""))
        for f in existing_files
        if f.startswith(base_name) and f.endswith(extension) and f.replace(base_name, "").replace(extension, "").isdigit()
    ]
    next_number = max(numbers, default=0) + 1
    filename = f"{base_name}{next_number}{extension}"
    save_path = os.path.join("batchURLs", filename)

    # Write to file
    with open(save_path, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url.strip() + "\n")

    global selected_batch_path
    selected_batch_path = save_path
    messagebox.showinfo("Saved", f"Batch URLs saved to '{save_path}'")


def load_batch_file():
    global selected_batch_path  # Declare it global so it's accessible everywhere
    filepath = filedialog.askopenfilename(
        title="Open Batch URL File", 
        filetypes=[("Text Files", "*.txt")],
        initialdir=batchfile_path
    )
    
    if filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            urls = f.read()
        batch_text.delete("1.0", tk.END)
        batch_text.insert(tk.END, urls)

        selected_batch_path = filepath  # Only set if a file is selected
        messagebox.showinfo("Loaded", f"Loaded URLs from {os.path.basename(filepath)}")
    else:
        messagebox.showwarning("No File Selected", "No file was chosen. Please try again.")



def run_ml_batch():
    if not selected_batch_path or not os.path.exists(selected_batch_path):
        messagebox.showwarning("File Missing", "No batch URL file selected or found.")
        return

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    ml_logfile_path = f"logs/ml_batch_log_{timestamp}.txt"
    os.makedirs("logs", exist_ok=True)

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Running ML on batch URLs...\n")

    with open(selected_batch_path, "r") as f, open(ml_logfile_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"ML Batch Run - {time.ctime()}\n\n")
        for line in f:
            url = line.strip()
            if url:
                ml_module_handler.load_model("modelfile/best_random_forest_full.pkl")
                prediction = ml_module_handler.predict_sqli(url)
                status = "Injection" if prediction == 1 else "No Injection"
                result_line = f"{url} → {status}"
                result_text.insert(tk.END, result_line + "\n")
                log_file.write(result_line + "\n")

    result_text.config(state=tk.DISABLED)
    result_window.deiconify()
    messagebox.showinfo("Logged", f"ML batch results saved to '{ml_logfile_path}'.")

def run_sqlmap_batch():
    if not selected_batch_path or not os.path.exists(selected_batch_path):
        messagebox.showwarning("File Missing", "No batch URL file selected or found.")
        return

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    sqlmap_logfile_path = f"logs/sqlmap_batch_log_{timestamp}.txt"
    os.makedirs("logs", exist_ok=True)

    cookie = batch_cookie_entry.get().strip()

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, "Running SQLmap on batch URLs...\n")

    with open(selected_batch_path, "r") as f, open(sqlmap_logfile_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"SQLmap Batch Run - {time.ctime()}\n")
        if cookie:
            log_file.write(f"Using Cookie: {cookie}\n")
        log_file.write("\n")

        for line in f:
            url = line.strip()
            if url:
                result_text.insert(tk.END, f"\n--- {url} ---\n")
                log_file.write(f"\n--- {url} ---\n")

                command = ["python", "sqlmap/sqlmap.py", "-u", url, "--batch"]
                if cookie:
                    command.extend(["--cookie", cookie])

                start = time.time()
                try:
                    process = subprocess.run(command, capture_output=True, text=True, timeout=180)
                    output = process.stdout if process.stdout else process.stderr
                except Exception as e:
                    output = f"Error running SQLmap: {e}"
                end = time.time()

                duration = end - start
                result_text.insert(tk.END, output + f"\n[Time: {duration:.2f}s]\n")
                log_file.write(output + f"\n[Time: {duration:.2f}s]\n")

    result_text.config(state=tk.DISABLED)
    result_window.deiconify()
    messagebox.showinfo("Logged", f"SQLmap batch results saved to '{sqlmap_logfile_path}'.")


def view_previous_logs():
    log_file = filedialog.askopenfilename(title="Select Log File", 
                                          filetypes=[("Text Files", "*.txt")],
                                          initialdir=logfile_path)
    if log_file:
        with open(log_file, "r", encoding="utf-8") as file:
            log_content = file.read()
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, log_content)
        result_text.config(state=tk.DISABLED)
        main_window.withdraw()
        result_window.deiconify()

# --- Main Window ---
main_window = tk.Tk()
main_window.title("SQLMap GUI")
main_window.geometry("400x300")

tk.Label(main_window, text="WELCOME TO SQLMAP GUI VERSION", font=("Arial", 12)).pack(pady=20)
tk.Button(main_window, text="Operate with Machine Learning Feature", command=open_ml_mode).pack(pady=10)
tk.Button(main_window, text="Operate as Normal Engine", command=open_sqlmap_mode).pack(pady=10)
tk.Button(main_window, text="Open Batch Mode", command=open_batch_mode).pack(pady=10)
tk.Button(main_window, text="View Previous Result", command=view_previous_logs).pack(pady=10)
tk.Button(main_window, text="Exit Application", command=exit_application).pack(pady=10)

# --- ML Mode Window ---
ml_window = tk.Toplevel(main_window)
ml_window.title("SQLMap GUI - ML Mode")
ml_window.geometry("400x300")
ml_window.withdraw()
tk.Label(ml_window, text="Website URL:").pack()
ml_url_entry = tk.Entry(ml_window, width=50)
ml_url_entry.pack()
select_model_button = tk.Button(ml_window, text="Select Trained ML Model", command=select_model_file).pack(pady=5)
status_label = tk.Label(ml_window, text="Selected Model: None", fg="blue")
status_label.pack(pady=5)
if os.path.exists(selected_model_path):
    try:
        ml_module_handler.load_model(selected_model_path)
        status_label.config(text=f"Selected Model: {os.path.basename(selected_model_path)}")
    except Exception as e:
        status_label.config(text="Failed to load default model.")
else:
    status_label.config(text="Default model not found.")
fallback_to_sqlmap = tk.BooleanVar()
tk.Checkbutton(ml_window, text="Fallback to SQLmap if ML fails", variable=fallback_to_sqlmap).pack(pady=5)
tk.Button(ml_window, text="Operate with Machine Learning", command=execute_ml).pack(pady=10)
tk.Button(ml_window, text="Back to Main Menu", command=lambda: [ml_window.withdraw(), main_window.deiconify()]).pack(pady=5)

# --- SQLMap Mode Window ---
sqlmap_window = tk.Toplevel(main_window)
sqlmap_window.title("Normal Mode")
sqlmap_window.geometry("400x300")
sqlmap_window.withdraw()
tk.Label(sqlmap_window, text="Website URL:").pack()
sqlmap_url_entry = tk.Entry(sqlmap_window, width=50)
sqlmap_url_entry.pack()
tk.Label(sqlmap_window, text="Options:").pack()
sqlmap_options = ttk.Combobox(sqlmap_window, values=["--dbs", "--tables", "--columns", "--dump", "--os-shell", "--file-read", "--file-write",
    "--hostname", "--users", "--passwords", "--roles", "--privileges", "--current-user", "--current-db",
    "--is-dba", "--banner", "--technique=BEUSTQ"])
sqlmap_options.pack()
tk.Label(sqlmap_window, text="Session Cookie (Optional):").pack()
cookie_entry = tk.Entry(sqlmap_window, width=60)
cookie_entry.pack()
tk.Button(sqlmap_window, text="Run SQLmap", command=execute_sqlmap).pack(pady=10)
tk.Button(sqlmap_window, text="Back to Main Menu", command=lambda: [sqlmap_window.withdraw(), main_window.deiconify()]).pack(pady=5)

# --- Batch Input Window ---
batch_window = tk.Toplevel(main_window)
batch_window.title("Batch URL Input")
batch_window.geometry("500x500")
batch_window.withdraw()
tk.Label(batch_window, text="Enter URLs (one per line):").pack()
batch_text = tk.Text(batch_window, height=10, width=60)
batch_text.pack(pady=10)
tk.Button(batch_window, text="Load Existing Batch File", command=load_batch_file).pack(pady=5)
tk.Label(batch_window, text="Session Cookie (Optional):").pack()
batch_cookie_entry = tk.Entry(batch_window, width=60)
batch_cookie_entry.pack()
tk.Button(batch_window, text="Save Batch File", command=save_batch_file).pack(pady=5)
tk.Button(batch_window, text="Run ML on Batch", command=run_ml_batch).pack(pady=10)
tk.Button(batch_window, text="Run SQLmap on Batch", command=run_sqlmap_batch).pack(pady=10)
tk.Button(batch_window, text="Back to Main Menu", command=lambda: [batch_window.withdraw(), main_window.deiconify()]).pack(pady=5)

# --- Result Window ---
result_window = tk.Toplevel(main_window)
result_window.title("Results")
result_window.geometry("700x700")
result_window.withdraw()
tk.Label(result_window, text="Result Window", font=("Arial", 10)).pack(pady=10)
result_text = tk.Text(result_window, height=25, width=150)
result_text.pack(pady=10)
result_text.config(state=tk.DISABLED)
tk.Button(result_window, text="Back to Main Menu", command=cancel_operation).pack(pady=5)

main_window.mainloop()
