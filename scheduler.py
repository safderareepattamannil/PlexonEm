import main
import schedule
import time

# Every two minutes run the main script
schedule.every(1).minutes.do(main.activate_plex_engine)

while True:
    schedule.run_pending()
    time.sleep(1)

