import subprocess
import time
program_path_1 = "guiv/guiv.py"
program_path_2 = "textv/textv.py"
sleep_time = 1.8
while True:
    process = subprocess.Popen(["python", program_path_1])
    time.sleep(sleep_time)
    if process.poll() is not None:
        print("Error detected. Starting another version of the program...")
        process = subprocess.Popen(["python", program_path_2])
        continue
    else:
        print("Program is running.")
        break
