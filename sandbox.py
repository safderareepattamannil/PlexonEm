import psutil


fpath = "C:\\Users\\bb\\Downloads\\Friday.Night.Lights.S05.1080p.AMZN.WEBRip.DD5.1.x264-NTb[rartv]"

def has_handle(fpath):
    for proc in psutil.process_iter():
        try:
            for item in proc.open_files():
                if fpath == item.path:
                    return True
        except Exception:
            pass

    return False

print(has_handle(fpath))