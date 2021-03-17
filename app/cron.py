from app import app, db, crontab
from app.models import Rollcall, User
from datetime import date

@app.cli.command()
@crontab.job(minute="0", hour="17")
def mark_absent():
    users = User.query.all()
    user_ids = [user.id for user in users]
    date_obj = date.today()
    date_obj = date_obj.strftime("%d/%m/%y")
    print(user_ids, date_obj)
    present_users = Rollcall.query.filter_by(date=date_obj).all()
    # present_users = Rollcall.query.all()
    present_users_ids = [user.id for user in present_users]
    print(present_users_ids)
    absent_ids = list(set(user_ids)-set(present_users_ids))
    for absent_id in absent_ids:
        rollcall = Rollcall(id=absent_id, date=date_obj, time='-1')
        db.session.add(rollcall)
    db.session.commit()

# @crontab.job()
# def cron_test():
#     """Cron testing"""
#     print("test")
