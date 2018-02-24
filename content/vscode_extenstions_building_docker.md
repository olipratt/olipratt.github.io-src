Title: Building VS Code Extensions in Docker Containers
Date: 2018-02-23 19:52
Category: Editors
Tags: VS Code, Docker
Image: /static/images/vscode_banner.png

#### TL;DR

- [VS Code](https://code.visualstudio.com/) is an editor that allows you to [write](https://code.visualstudio.com/docs/extensions/example-hello-world) and [share](https://marketplace.visualstudio.com/) custom extensions.

- These extensions require `Node.js` and `npm` installed, which you might not want to install locally - especially [given recent, scary issues](https://www.bleepingcomputer.com/news/linux/botched-npm-update-crashes-linux-systems-forces-users-to-reinstall/).

- Instead, using the `Dockerfile` and commands below, you can build extensions inside a Docker container and still test and run them inside the VS Code installation on the same machine without Node installed.

## Background

I've been using VS Code as my main editor for personal work for some time now, but only just got around to trying to create an extension.

I don't do any Node or Javascript development normally, so don't have Node/NPM installed, and [that's the first thing the docs tell you to do](https://code.visualstudio.com/docs/extensions/example-hello-world).
Keen not to install these on my system given the bloat I've heard they add and [recent issues](https://www.bleepingcomputer.com/news/linux/botched-npm-update-crashes-linux-systems-forces-users-to-reinstall/), I wanted to do try and do the necessary generation and building in a container.

Searching online for various combinations of relevant keywords only seemed to give me articles on writing extensions to work with Docker files/containers, and I had to poke about and get this working myself. I thought I'd write up how I did it in case it's useful for someone else.

## Getting Started

Obviously you'll need docker installed and set up.

Then the following `Dockerfile` will allow you to create a container with the VS Code extension generator ready and installed.

```Dockerfile
FROM node:latest

RUN npm install -g yo generator-code

USER node
WORKDIR /home/node/

ENTRYPOINT bash
```

Create a copy of that `Dockerfile` and build it - I called it `vscodeextenv`:

```shell
sudo docker build -t vscodeextenv .
```

Now I created a directory ready and named for my extension, and mounted that into the container.

```shell
mkdir example
sudo docker run -it \
     --mount source=$(pwd)/example,target=/home/node/example,type=bind \
     vscodeextenv
```

Now you should have an environment ready to build an extension.

___Gotcha:___ _I found out that [docker now recommends](https://docs.docker.com/storage/volumes/) you use `--mount` to mount directories inside a container rather than `-v`, but using that ended up with the mounted directory inside the container being owned by root until I added `type=bind` to the `mount` option._

## Building the Extension

Here you can just run the extension generator with `yo code` and follow the prompts. I named mine example, and just used dummy values for everything else. Like a good developer I also turned on all the linting :wink:.

Once it's generated, [the docs](https://code.visualstudio.com/docs/extensions/example-hello-world#_running-your-extension) say to start debugging the extension, but from what I can tell that first builds the extension, which won't work since we don't have all the dependencies installed. If I try, I get a few errors/stack traces in the debug console and this notification in the original VS Code instance

![Alt Text](/static/images/vscode_extension_debug_error.png)

The second instance that's supposed to have the extension loaded does open, but doesn't have it loaded in.

So we need to build it manually first.

This might be obvious if you're a proficient `node` developer, but after some poking through the generated files I found the command - in the container, run:

```shell
npm run compile
```

You'll now have an `out` directory, which is what VS Code needs.

___Gotcha:___ _For me the `compile` command failed with an error I think because I enabled the various linting and strict options when generating the project - this is fixed for now by commenting these lines out in `src/test/extension.test.ts`_

```ts
// import * as vscode from 'vscode';
// import * as myExtension from '../extension';
```

## Testing the extension in VS Code

_Now_ you should be able to, in VS Code, just open the `Debug` tab and press the `Play` button, and the new instance of VS Code with your app loaded should appear!

If you've just used the default app, then `Ctrl+Shift+P` in the new instance should allow you to find the `hello world` command, and running it should correctly show the notification.

The only downsides are that:

- the original VS Code instance still shows the error in the image above (I think because it still tries to build the extension and fails), though it runs fine regardless,

- you have to remember to manually build the extension in the container before running it in the VS Code debugger.
