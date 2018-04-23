# Udots Challenge - 2018

## Challenge 4 and 5 - Webapp and TCP Server

Create a Webapp that show a realtime graphic,
this graph should update every second from the data provided by a sum server.
The Sum Server is a small TCP services that listens on one socket (27877) for the incoming data (numbers 0...20),
and sum all the valid inputs within a second (1000ms) to generate a sum result,
then write to another socket (27878).

Connect the Webapp and the Sum Server,
every connected client should be shown in the WebApp like another line with the result of the sum,
if the socket is closed the line will take a red color and then after 5 seconds disappear.


### Explanation of solution

The solution was implemented with python3 using the thirdparty library tornado.
Tornado is an asynchronous network library that use non-blocking network I/O,
This allow tornado to scale to thousands of open connections.


### Architecture and deployment

The solution consist in three libraries and static files.
The library `server.py` contains the TCP Sum Server, `webapp.py` contains a Webapp Server,
`client.py` contains the TCP data clients and `static/` directory contains the statics files.

![Infraestructure](imgs/infraestructure.png)


#### Install

The solution use python3 and the thirdparty library tornado, install dependencies:

``` bash
$ pip install tornado
```


#### Deployment

Start the TCP Sum Server, The Webapp and the data clients
using differents terminals like this:

``` bash
$ python server.py
```

``` bash
$ python webapp.py
```

``` bash
$ python clients.py
```
