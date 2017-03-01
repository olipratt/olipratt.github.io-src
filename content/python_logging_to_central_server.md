Title: Python Microservice Logging
Date: 2017-02-25 14:39
Category: Logging
Tags: Python, logging, syslog, microservice

After looking into [microservices]({filename}/rest_swagger_producer.md) [recently]({filename}/rest_swagger_consumer.md), I was running multiple terminals and switching between them to look at logs as they are written to screen. This was a little awkward so I thought it was worth looking for the right way to log to a central location from multiple microservices. Ideally I wanted do this just using the Python logging library, and without adding more dependencies to every service.

This meant a lot of reading around to reach a rather boring and obvious solution. I documented my whistle-stop tour around the world of logging, but jump to the end to just see the [solution](#real-solution) I went with.

## Picking a format

#### Open Standards

Straight off - there's no obvious standardised server package for receiving logs over the network from the Python logging module. I initially thought this whole thing would just take a 5 minute search - maybe this should have been a clue.

So I started looking around for other open logging formats and log stores. Turns out there's quite a few of these.  [GELF](http://docs.graylog.org/en/2.2/pages/gelf.html) seemed like maybe a good option. It's open, JSON structured format, integrates with many log stores, and has a [Python logging module handler](https://github.com/severb/graypy).

[The GELF server](http://docs.graylog.org/en/2.2/pages/installation.html) is pretty massive though - delivered as a whole VM, ideally I just wanted a simple listener script I could run. I did find a [single simple server implementation](http://idlethreat.com/blog/graylog/gelf-listener-in-python/), but that was it. I got it all running easily enough, and though I could have tidied it up and used it, I felt I was off the beaten path and had added a new dependency to every service for logging so kept digging for a bit.

#### Too Cumbersome - Back to Simple HTTP

Going back to the logging module, it looked like basic [HTTPHandler](https://docs.python.org/3/library/logging.handlers.html#httphandler) would do, and meant no dependencies. However, I found [warnings that it was slow](http://ericshtiv.blogspot.co.uk/2012/12/python-fast-http-logging-handler.html), but then a [solution](http://plumberjack.blogspot.co.uk/2010/09/improved-queuehandler-queuelistener.html) to that using the logging module's [queuehandler](https://docs.python.org/3.6/library/logging.handlers.html#queuehandler).

I got that working, but the POST body from the HTTPHandler was not JSON but just a [URL encoded string](http://stackoverflow.com/a/14551320). I could easily decode this in a Flask server, but then it was still a lot of code to copy paste and I might as well just shove in a JSON body instead. So I reworked that into a REST log handler - which I still have lying around:

```python3
def configure_remote_logging(url, client_name, level=logging.INFO):
    """Set up remote logging to the specified url.

    This sets up a queue which logs are placed onto, and then they are sent on
    a background thread so they don't slow down the code making the logs.
    """
    # The handler which will send logs remotely - definition and an instance.
    class RESTHandler(logging.Handler):
        """Handler which sends logs to a REST log server."""

        def __init__(self, url, client_name):
            super(RESTHandler, self).__init__()
            self.url = url
            self.client_name = client_name

        def format(self, log_record):
            formatted = log_record.__dict__
            formatted["processName"] = self.client_name
            return formatted

        def emit(self, log_record):
            import requests
            requests.post(self.url, json=self.format(log_record))

    rest_handler = RESTHandler(url, client_name)
    rest_handler.setLevel(level)

    # Create queue handlers so that logs are processed in a background thread.
    # Set up an unbounded size queue and assume logs are processed faster than
    # they are made.
    logging_queue = queue.Queue()
    queue_handler = logging.handlers.QueueHandler(logging_queue)
    queue_listener = logging.handlers.QueueListener(logging_queue,
                                                    rest_handler)

    # Add the remote logging handler and start the background queue running.
    root = logging.getLogger()
    root.addHandler(queue_handler)
    queue_listener.start()

    # Should call this on exit to ensure all final logs are flushed.
    # queue_listener.stop()
```

Then receiving the log is simple on the Flask server side - just:

```python3
class LogsCollection(Resource):
    def post(self):
        """Receives a log."""
        log.handle(logging.makeLogRecord(request.get_json()))
        return None, 201
```

But now:

- I should really be calling the commented out `stop` method on the queue when the app exits, otherwise logs can end up not being flushed - which means some kind of global state to store a reference to that queue and a hook to call it.
- The overhead of a HTTP POST for every log seems high - especially at the debug level.
- I've still got a huge block of code to copy/paste into every service, or otherwise write a package and add another dependency.
- I've added a dependency on `requests` in there.

Sigh.

#### No, No - Let's Use a Standard

Clearly that's the wrong approach - throw it away and start over. Really we should be going with a standard so we can integrate with other things, and that ended up with me looking into syslog since

- it seemed frequently [recommended](http://www.structlog.org/en/stable/logging-best-practices.html#syslog-again),
- well used and supported by every client/server,
- has a built in [Python logging handler](https://docs.python.org/3/library/logging.handlers.html#sysloghandler),
- I [found a tiny Python listener for it](https://gist.github.com/marcelom/4218010),
- and [it's so standardised it has an RFC](https://tools.ietf.org/html/rfc5424)!

This *had* to be the right answer, so I wrote some client code for that:

```python
def configure_logging(client_name, host=None, level=logging.INFO):
    """Set up logging to stderr and optionally a remote syslog server."""
    handlers = []

    if host is not None:
        syslog_fmt = ('1 %(asctime)s.%(msecs)03dZ {} {} - - - '
                      '%(message)s').format(socket.getfqdn(), client_name)
        syslog_date = '%Y-%m-%dT%H:%M:%S'
        syslog_formatter = logging.Formatter(syslog_fmt, datefmt=syslog_date)
        # Force UTC time so we can just stick `Z` at the end of the timestamp.
        syslog_formatter.converter = time.gmtime

        syslog_handler = logging.handlers.SysLogHandler(address=(host, 514))
        syslog_handler.setFormatter(syslog_formatter)
        handlers.append(syslog_handler)

    stderr_fmt = '%(asctime)-23s:%(levelname)-8s:%(message)s'
    stderr_formatter = logging.Formatter(stderr_fmt)
    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(stderr_formatter)
    handlers.append(stderr_handler)

    root = logging.getLogger()
    root.setLevel(level)
    for handler in handlers:
        root.addHandler(handler)
```

*Aside: I had to build the formatter to match the RFC standard syslog format because I couldn't easily find one elsewhere - might come in handy.*

So this now works fine, it's a reasonable chunk of code, but it's mostly just boilerplate stuff setting up the built in logging module, and the only custom part is setting up the right formatter. All done?


## Real Solution

So after all that, I think I'm done and move on to something else - containerising these apps was up next for me - ...and that's when I stumble across the *right* answer. It's right [here](https://12factor.net/logs) in these [guidelines to writing services](https://12factor.net/):

***Just write your logs to stdout.***

That's it! Then whatever is running your app pipes them out and handles them appropriately. Anything else you do is just another system someone has to worry about integrating into their setup. [Docker by default assumes an app will send logs to stdout](https://docs.docker.com/engine/reference/commandline/logs/#/extended-description) and handles them as configured. I saw this in action when I started using Docker - I'll write that up soon.

---

So that was an interesting bit of investigation, and I learnt some stuff, but damn if it doesn't feel like a waste of time.

How do you handle logging from your Python apps?
