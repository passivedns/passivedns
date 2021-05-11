# Environment reference

The list of the environment variable  used by the API

| variable        | set by    | used for                              |
|-----------------|-----------|---------------------------------------|
| ARANGO_USERNAME | user      | database connection                   |
| ARANGO_PASSWORD | user/auto | database connection                   |
| JWT_SECRET_KEY  | user/auto | JWT build                             |
| DEBUG           | user      | run in DEBUG mode (logs more verbose) |
| VERSION         | gitlab    | the last tag used in the code         |
| COMMIT_SHA      | gitlab    | the last commit                       |
| JOB_URL         | gitlab    | the url of the gitlab pipeline        |
| SMTP_PASSWORD   | user      | email connection                      |
