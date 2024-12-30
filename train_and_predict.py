filename = "../../data/lichess_elite_2020-08.pgn"  
import os
# برای بررسی وجود فایل و خواندن محتوا  
if os.path.isfile(filename):  
    with open(filename, 'r') as file:  
        content = file.read()  # یا هرگونه پردازش دیگر که می‌خواهید انجام دهید  
else:  
    print(f"The file {filename} does not exist.")