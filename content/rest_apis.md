Title: REST APIs Notes and References
Date: 2017-02-12 17:37
Modified: 2017-02-25 20:45
Category: REST
Tags: REST

After working to create a [REST API]({filename}/rest_swagger_producer.md) and [client]({filename}/rest_swagger_consumer.md) recently, here are some notes and resources I found useful. I'll keep adding to this as I find new info.

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

* RESTful API Design Guides

    * [Google's](https://cloud.google.com/apis/design/)

    * [Microsoft's](https://github.com/Microsoft/api-guidelines/blob/master/Guidelines.md)

    * [Zalando's](https://zalando.github.io/restful-api-guidelines/)

* [Talk on the discoverability side of REST](https://vimeo.com/20781278)

Have you got any other good general rules, notes, or references to add?
