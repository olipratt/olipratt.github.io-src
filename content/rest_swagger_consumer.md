Title: Python REST API Client Adhering to a Swagger Schema
Date: 2017-02-11 19:13
Category: REST
Tags: Python, REST, Swagger, pyswagger, microservice


After [building a REST API]({filename}/rest_swagger_producer.md) I left it alone for a while before coming back to try and get a client working properly.

Similar goals here to back then - find a good library to use going forwards that does the heavy lifting and make a simple example project. I chose a simple microservice that provides an API for decks of playing cards - like a casino dealer type of thing - which would be a client of the datastore I created in the link above.

## Choosing a Client Package

The standard seems to be to [generate code](https://github.com/swagger-api/swagger-codegen) to meet a schema, but I'd rather load it dynamically into an app if possible.

After a bit of looking I found [Bravado](http://bravado.readthedocs.io/en/latest/) which looked promising. However, it was a pain to install - it relies on the twisted package and that doesn't seem to install on Windows through pip successfully, so after some failed attempts to get it to work I gave up. I figure it's not worth using if it's going to be a pain for others to install - shame :(.

Next up was [pyswagger](http://pyswagger.readthedocs.io/en/latest/) - it seems to provide all the functionality and be well maintained (commits in the past few days when I wrote this). The API doesn't look as polished to me when compared to `bravado` above, but it worked fine in practice.

On the testing point - `pyswagger` uses  `requests` for HTTP requests, so we can easily test using the [responses](https://github.com/getsentry/responses) library to provide mock responses to them.


## The First Test

This was painful to get working, but as always trivial to fix in the end.

I needed to load in the schema, and then intercept the requests over the network for each API call. Intercepting the API calls was trivial with `responses`, but loading in the schema turned out to be less so.

There were two approaches I could see:

* `pyswagger` lets you load in a schema from file, so just pass it a file name
* intercept the request for the schema over the network

However, both failed when I tried:

* if I loaded in the schema from file, `pyswagger` would then try and make API requests using the `file` scheme, which causes it to fall over as that's not a [supported scheme](https://github.com/mission-liao/pyswagger/blob/cff50d0b49da984666e1a350cff3e7bdf71d0b13/pyswagger/contrib/client/requests.py#L11) for that part it seems.
* the request for the schema over the network uses [`urllib.urlopen` rather than `requests`](https://github.com/mission-liao/pyswagger/blob/cff50d0b49da984666e1a350cff3e7bdf71d0b13/pyswagger/getter.py#L136) so I couldn't easily intercept it with `responses` and would have to do more mocking of the deep internals of `pyswagger`, which seemed wrong.

Lots of trial-and-error and reading of the `pyswagger` source later I found the solution in the [tests of the client in `pyswagger` itself](https://github.com/mission-liao/pyswagger/blob/cff50d0b49da984666e1a350cff3e7bdf71d0b13/pyswagger/tests/contrib/client/test_requests.py#L28). They were doing exactly what I was trying in the first bullet above - loading in the schema from file then intercepting API requests - so why were their API requests working? It turns out their schema had two entries not added by `Flask-RESTPlus` - [`host`](https://github.com/mission-liao/pyswagger/blob/cff50d0b49da984666e1a350cff3e7bdf71d0b13/pyswagger/tests/data/v2_0/wordnik/swagger.json#L16) and [`schemes`](https://github.com/mission-liao/pyswagger/blob/cff50d0b49da984666e1a350cff3e7bdf71d0b13/pyswagger/tests/data/v2_0/wordnik/swagger.json#L40).

So I just needed this in top level of my schema saved in a file for the tests:

```json
{
  "host": "127.0.0.1:5000",
   "schemes":[
      "http"
   ],
   ...
}
```

With that, `pyswagger` can load schema from file for tests, and then send API requests over HTTP to that address, and we can use `responses` to catch those and respond to them.

Phew!

## Overall

Once I had wasted far too long trying to get a test working, everything else was straightforward, basically just following the [tutorials linked in the `pyswagger` readme](https://github.com/mission-liao/pyswagger#tutorial).

When you have loaded in the schema to `pyswagger`, you just reference API calls by name in the schema, which `Flask-RESTPlus` auto-generates from the class names you give to resources, and you can rename if you want - details of both of those bits of logic [here](https://flask-restplus.readthedocs.io/en/stable/swagger.html#documenting-the-methods). `pyswagger` makes sure you pass in all the right arguments in the right format, so if you have models in the schema you pretty much have to use the API correctly or any attempts will be rejected, which is great for catching bugs early.

## Result

Here's the project - [microcarddeck](https://github.com/olipratt/microcarddeck). I didn't end up implementing much function because I didn't need to - I got to exercise the `pyswagger` package and get a feel for how to use it, and got a good simple bit of reference code to crib from in the future.
