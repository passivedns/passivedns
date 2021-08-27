import datetime
import os
import sched
import time
import sys

from client import ApiClient
from processing import resolve_all

launch_hour = int(os.environ['LAUNCH_HOUR'])
launch_minute = int(os.environ['LAUNCH_MINUTE'])
days_frequency = int(os.environ['DAYS_FREQUENCY'])
scheduler = sched.scheduler(time.time, time.sleep)

host = os.environ['API_HOST']
username = os.environ['API_USERNAME']
password = os.environ['API_PASSWORD']
client = ApiClient(host, username, password)

thread_count = int(os.environ['THREAD_COUNT'])

retry_timeout = 5


def first_login():
    while True:
        try:
            client.login()
            return
        except Exception as e:
            print(f"cant connect to the API: {str(e)}")
            print(f"retrying in {retry_timeout} seconds...")
            time.sleep(retry_timeout)
            pass


def main():
    print('testing login...')
    first_login()
    print('login successful')

    
    if len(sys.argv) > 1 and sys.argv[1]== "--now":
        # excecute the job now
        print("executing the job now...")
        resolve_all(client, thread_count)

    else:
        print("launching the scheduler...")
        # scheduled

        while True:
            # get the next date of the job
            launch_date = datetime.datetime.now().date() + datetime.timedelta(days=days_frequency)

            # set the hour
            launch_time = datetime.time(launch_hour, launch_minute)

            # set timestamp
            launch_timestamp = datetime.datetime.combine(
                launch_date, launch_time
            )

            # schedule next
            scheduler.enterabs(launch_timestamp.timestamp(), 1, resolve_all, argument=(client, thread_count))

            print(f'{launch_timestamp} - waiting for run')
            scheduler.run()


if __name__ == "__main__":
    main()
