Title: Python REST API With SwaggerUI
Date: 2016-10-29 11:45
Category: REST
Tags: Python, REST, Swagger, Flask-RESTPlus, microservice


What with REST APIs and the [swagger](http://swagger.io/) framework for documenting and integrating them being the in-thing lately, to start getting to grips with them I wanted to see how easy it would be to create a simple one in Python with minimal code from me. Turns out it was very simple.

As practice project I picked writing a really simple datastore.

## Choosing a Package

After looking around for something that provides a SwaggerUI ([demo here](http://petstore.swagger.io/) to see what this looks like) and schema, I found [Flask-RESTPlus](https://flask-restplus.readthedocs.io/en/stable/index.html) which does this [really easily out of the box](https://flask-restplus.readthedocs.io/en/stable/swagger.html#swagger-ui). It also builds on top of [Flask](http://flask.pocoo.org/) which I've heard good things about and wanted to try for a while - having only used [cherrypy](http://cherrypy.org/) before myself.

Another thing I wanted was to be able to easily test the API, and it seemed  `Flask` is really [easy to test](http://flask.pocoo.org/docs/0.11/testing/), and so by extension so is `Flask-RESTPlus` as it just plugs in on top. So this combo sounded like a good choice to get going.

I also needed some way to store the data and so looked for a really simple key-value store. A quick search gave [TinyDB](http://tinydb.readthedocs.io/en/latest/getting-started.html) - small, easy to set up, and stores Python `dict`s directly ([easily converted to](https://docs.python.org/3.5/library/json.html#json.loads) from the JSON used in the API).

## Getting Started

Getting something up and running was very straightforward - I followed the tutorial [here](http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/) and wrote tests as I went.

That was followed by lots of tweaking/playing with the contents of the SwaggerUI page and working out how to create data models to enforce on the API, but the bulk of the work to get going was trivial.

## Impressions

The SwaggerUI page is **really** great for exploring and documenting APIs. Often it's hard to grasp how to integrate with some new code from reading it, but here you can actually play with the interface, press buttons to see what happens, and provide input and follow it through different API calls - really nice to use. Definitely like it and plan to use it more.

With a bit of reading of the `Flask-RESTPlus` docs you can edit all the fields and documentation in the Swagger UI page so you can make it as easy to use as possible - looks like it's fully featured in that respect and was a good choice.

## Gotchas

It wasn't entirely plain sailing though - here are the main problems I hit that it's worth being aware of!

* You have to use a non-empty prefix for your API to start at ([`prefix` parameter here](https://flask-restplus.readthedocs.io/en/stable/api.html#flask_restplus.Api)). I [raised an issue about it](https://github.com/noirbizarre/flask-restplus/issues/210) but it didn't garner much attention. It's pretty minor though - I suspect any real system would not have the API exposed on `/` directly.

* It doesn't seem like the swagger schema is exposed anywhere over HTTP by `Flask-RESTPlus` by default. However, it's really easy to do so, just return `api.__schema__` as the response to a `GET` request and it's there. I ended up doing that in a separate `schema` namespace so it gets it's own top-level section in the SwaggerUI.

* If you use the `@api.expect` decorator to state what model the incoming data must match, `Flask-RESTPlus` won't force incoming data to conform unless you set the `validate=True` parameter on it - seems like the wrong default to me...

## End Result

And here's the result - [microstore](https://github.com/olipratt/microstore) - a trivial datastore with a rest API and documented and interactive via SwaggerUI. I kept all the code [in one file](https://github.com/olipratt/microstore/blob/master/microstore.py) to make it as simple a reference as possible.

I'd say it was a success, and was a fun weekend!
