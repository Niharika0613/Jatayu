from celery.schedules import crontab

beat_schedule = {
    "daily-trek-reminders": {
        "task": "app.jobs.tasks.send_daily_reminders",
        "schedule": crontab(hour=8, minute=0),  # Every day at 8 AM IST
    },
    "monthly-admin-report": {
        "task": "app.jobs.tasks.send_monthly_admin_report",
        "schedule": crontab(hour=9, minute=0, day_of_month=1),  # 1st of every month
    },
}
