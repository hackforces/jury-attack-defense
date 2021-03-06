from pytz import utc
import time
import os

# APScheduler import
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import *

# custom classes & modules
from modules.db import Database
from modules.zond import Zond
from modules.utils import *
from etc.config import *
spath = os.path.dirname(os.path.realpath(__file__))

# Listener for success attack
def success_attack(event):
    # print(event.retval)
    if len(event.retval) == 7:
        DB.saveAttack(event.retval)

if __name__ == '__main__':
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
    scheduler.remove_all_jobs()
    scheduler.add_listener(success_attack, EVENT_JOB_EXECUTED)
    # scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    DB = Database(connString)
    # DB = Database('pq://ctf:14881488@localhost:5432/ctf')
    teams = DB.getTeams(GAME['teams'])
    services = DB.getServices(GAME['services'])
    # loadExpolits(services)
    # scheduler.add_job(
    #     Zond.attack,
    #     args=(spath, 'check', '127.0.0.1', 'Test 1', 'test_flag'), # command for Zond
    #     max_instances=3, # how many instances (threads) open for this job
    #     trigger='interval', # job trigger type
    #     seconds=4, # repeat interval
    #     misfire_grace_time=int(3), # maximum waiting time
    #     executor='default' # executor (thread, process, custom)
    # ) #, executor='processpool')
    # scheduler.add_job(
    #     Zond.attack,
    #     args=(spath, 'check', '127.0.0.1', 'Test 1', 'test_flag'), # command for Zond
    #     max_instances=3, # how many instances (threads) open for this job
    #     trigger='interval', # job trigger type
    #     seconds=4, # repeat interval
    #     misfire_grace_time=int(3), # maximum waiting time
    #     executor='default' # executor (thread, process, custom)
    # ) #, executor='processpool')
    # scheduler.add_job(DB.update(q), 'internval', seconds=2, executor='processpool')
    for team in teams:
        for service in services:
            # add "check" jobs
            scheduler.add_job(
                Zond.attack,
                args=(spath, 'check', team, service), # command for Zond
                name= strFmt(team['name'] + service['name']).
                max_instances= 2,#GAME['teams'], # how many instances (threads) open for this job
                trigger='interval', # job trigger type
                seconds=service['interval'], # repeat interval
                misfire_grace_time=int(GAME['roundtime'] / 2), # maximum waiting time
                executor='default' # executor (thread, process, custom)
            ) #, executor='processpool')
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # DB.close()
        scheduler.remove_all_jobs()
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()


# if __name__ == '__main__':
    # DB = Database('pq://ctf:14881488@localhost:5432/ctf')
    # print(DB.getTeams(3))
    # DB.close()
