# PASSIVE DNS SCHEDULER

This scheduler runs resolution update, at a specified frequency.

## Environment reference

The scheduler MUST be run with the following variable in order to be run.

| variable       | description                                             | example value       |
|----------------|---------------------------------------------------------|---------------------|
| LAUNCH_HOUR    | Hour of the launch time                                 | 12                  |
| LAUNCH_MINUTE  | Minute of the launch time                               | 30                  |
| DAYS_FREQUENCY | Frequency of the task (day unit)                        | 1                   |
| API_HOST       | Host where the passive DNS API is hosted                | https://api.host.fr |
| API_USERNAME   | Identity to use when interacting with the API           | user                |
| API_PASSWORD   | Password to use when interacting with the API           | password            |
| THREAD_COUNT   | Count of worker interacting simultaneously with the API | 5                   |
