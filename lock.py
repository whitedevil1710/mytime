import subprocess
from datetime import datetime

def check_screen():
    out = subprocess.run(['gnome-screensaver-command', '-q'], stdout=subprocess.PIPE, text=True)
    status = out.stdout.strip().split()
    current = datetime.now()
    time= current.strftime("%H:%M")
    if status[-1]== "inactive":
        return False
    else:
        return True
    
print(check_screen())