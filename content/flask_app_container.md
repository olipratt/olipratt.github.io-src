Title: Docker Container for a simple Flask App
Date: 2017-03-01 21:36
Category: Containers
Tags: Python, Flask, Container, Docker, microservice


Continuing the recent microservices trend, I tried to containerise a previous project, a small REST datastore - [microstore]({filename}/rest_swagger_producer.md).

I'm not going to go into detail on what containers are (not least because I don't think I could!) - but briefly they are a way to package up an app and it's dependencies so they can be run in their own mini-environment. The best intro is just to follow the tutorial [here](https://docs.docker.com/engine/getstarted/).

## Creating the Container

I installed [Docker on CentOS](https://docs.docker.com/engine/installation/linux/centos/). It warns you not to just `yum install`, so instead I followed the *Install from a package* instructions - but note that you now have to always run docker commands with `sudo`.

Containerising an app was simple - basically [just follow this tutorial](https://runnable.com/docker/python/dockerize-your-flask-application).

[Here's](https://github.com/olipratt/microstore/blob/master/Dockerfile) the `Dockerfile` I created following that - now in the microstore repo.

Note I had to set the app to listen on `0.0.0.0` because we are going to forward ports to outside the container, so need to listen on a public address inside the container.

So if you have docker installed, just:

* get a clone of the microstore repo,
* build the container image with: `sudo docker build -t microstore:latest .`
* then run it with: `sudo docker run -p 5000:5000 microstore`

The `-p 5000:5000` binds port 5000 of the container to port 5000 on the host.
So now you can just go to `http://127.0.0.1:5000/` in your web browser and you should see the SwaggerUI running!

Some notes on running containers:

- If there's a problem building/running the app, you can just run the same commands again after fixing the problem.
- Add the `-d` option to run the container in the background.
- Note `sudo docker ps` shows what containerised apps are running.

## Shipping an Image

You can now create the final container ready to ship with `sudo docker save microstore > microstore.tar`. This one was about 300MB when I created it.

Later/elsewhere you can reload it with `sudo docker load < microstore.tar`.

## Composing Multiple Containers

Now I'd got one running, I wanted to see how you'd ship several microservices given they would need to contact each other over IP somehow. Turns out that's simple too using `docker-compose`.

Again, not going into detail on this as it's all online.

* There's a good tutorial [here](https://docs.docker.com/compose/gettingstarted/).
* You may need to specify a [startup order](https://docs.docker.com/compose/startup-order/) so that a service is created before another tries to connect to it.
* Networking between services is also simple - basically [access the name of a service in the compose file as a hostname](https://docs.docker.com/compose/networking/).

I set up my little card deck service with a [Dockerfile](https://github.com/olipratt/microcarddeck/blob/master/Dockerfile) and [compose file](https://github.com/olipratt/microcarddeck/blob/master/docker-compose.yml) to run it and the microstore together. If you built the microstore container above, then by just running `sudo docker-compose up` in the card deck repo it will build the second image and then run them both together - magic!

*One note - I was confused that `sudo docker-compose up` didn't rebuild the image after fixing a bug in the `Dockerfile` but, as per [here](https://github.com/docker/compose/issues/1487), you need to run `sudo docker-compose build` to force it to rebuild - `up` won't ever rebuild.*

## Tidying up

Docker seems to leave images that you create as you iterate lying around, and you have to do a bit of manual cleanup at the end. As noted in [here](https://docs.docker.com/compose/gettingstarted/) you can clear up composed containers with `sudo docker-compose down`. You can then [prune](https://docs.docker.com/engine/reference/commandline/image_prune/) and [remove unused images](https://docs.docker.com/engine/reference/commandline/rm/#/remove-all-stopped-containers).

---

That was really simple and Docker seems like a great way for running at least simple apps in a controlled environment. What's been your experience with Docker, if any?
