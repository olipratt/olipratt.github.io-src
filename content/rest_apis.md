Title: REST APIs Notes and References
Date: 2017-02-12 17:37
Category: REST
Tags: REST

After working to create a [REST API]({filename}/rest_swagger_producer.md) and [client]({filename}/rest_swagger_consumer.md) recently, here are some notes and resources I found useful.

#### General notes

* Resource collection names should always be plural.

* Depending on who (client vs server) names resources, creation switches between `PUT`/`POST`:
    * client names resources:
        * `PUT /kittens/<my_kittens_name>` - creates a resource there
    * server names resources:
        * `POST /things` - Creates a new `thing` at `/things/<autogened_id>`, with that ID returned in the response to the post


#### Some useful references

* [General REST API best practices](http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api)

* [Explanations of the REST verbs](http://www.restapitutorial.com/lessons/httpmethods.html)
