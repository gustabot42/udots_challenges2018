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

In order to achieve the amount of concurrent connections, the operative system was customized
and a non-blocking server was used. Thse server was fork in order to user both cores.
Multiple process running need an intermediator for communication,
the intermediator must be fast and support concurrency too or it will be a bottleneck.


### Architecture and deployment

The solution was implemented with python3.6 using the thirdparty library tornado and aioredis.
It take advantage of the multiproces capability of tornado to spam multiple process
and use a redis database for communication between the process.

Customize the OS variables like this:

``` bash
$ cat /etc/security/limits.d/20-nofile.conf

*	soft	nofile	999999
*	hard	nofile	999999
```

The app run with docker compose, like this:

``` bash
$ docker-compose --project-name udot7_redis -f docker-compose.yml up
```


### Test

A request spammer was developed in order to test server answers, run like this:

```
$ python requests.py
The server answered to ´1008´ requests
```
