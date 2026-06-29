from apscheduler.schedulers.background import BackgroundScheduler
from notifiication import check_birthdays, check_anniversary

scheduler = BackgroundScheduler()

# scheduler.add_job(
#     check_birthdays,
#     "interval",
#     minutes=1
# )
# scheduler.add_job(
#     check_anniversary,
#     "interval",
#     minutes=1
# )

scheduler.add_job(
    check_birthdays,
    "cron",
    hour=9,
    minute=0
)

scheduler.add_job(
    check_anniversary,
    "cron",
    hour=9,
    minute=0
)

def start_scheduler():
    scheduler.start()