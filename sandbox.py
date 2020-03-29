import os
import sys
import psutil

p = os.getcwd() + "\\log.txt"
print(p)

def has_handle(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True
        except Exception:
            pass

    return False


print(has_handle(p))