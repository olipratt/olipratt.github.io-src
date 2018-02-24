Title: Rebuilding Makefile Targets Only When Dependency Content Changes
Date: 2018-02-25 10:27
Category: GNU Make
Tags: GNU Make, builds
Status: draft

#### TL;DR

- GNU Make decides whether to rebuild a 'target' file based on the modification times of 'dependency' files of the target.

- In some cases those dependencies' modification times can change _without_ the contents of the files changing, thus forcing an unnecessary rebuild.

- If `make` was to decide whether to rebuild by looking at the hash of the contents of the dependency files instead, it would only rebuild when the contents changed.

- I wrote a utility for doing this as a simple makefile to include, and it is on Github here: [hashdeps](https://github.com/olipratt/hashdeps)

## Background

