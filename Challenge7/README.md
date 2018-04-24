# Udots Challenge - 2018

## Challenge 7 - DEVOPS

Create and deploy the following application, it must support up to 5.000 concurrent HTTP
requests, the application should be have the following specification:

```
/ => Response ( OK ) { status code : 200 } ( Always the server return OK)
/ check /{:m illis } => Response ( CHECKED|FAIL ) { status code : 201 } (*)
/ stats => Response ( Integer ) { status code : 200 } ( Amount of pending request to response)
```

(\*) If millis is between 1 and 20.000 this endpoint should do a sleep of the time of the millis
parameter and then answer CHECKED, if millis is another value return immediately FAIL.


### Explanation of solution

In order to achieve the amount of concurrent connections, a non-blocking server was used.
But one process will not use both cores, so to server was fork.
To process running need and intermediator to communicate information,
it must be fast or it will be a bottleneck (indeed, the concurrence sought was not achieved,
possibly because redis was not optimized)


### Architecture and deployment

The solution was implemented with python3 using the thirdparty library tornado.
It take advantage of the multiproces capability of tornado to spam multiple process
and use a redis database for communication between the process.

The app run with docker compose, like this:

```
$ docker-compose --project-name udot7_redis -f docker-compose.yml up
```


### Test

A request spammer was developed in order to test server answers, run like this:

```
$ python requests.py
The server answered to ´1008´ requests
```
