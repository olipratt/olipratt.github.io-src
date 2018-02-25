Title: Rebuilding Makefile Targets Only When Dependency Content Changes
Date: 2018-02-25 12:27
Category: GNU Make
Tags: GNU Make, builds

#### TL;DR:

- GNU Make decides whether to rebuild a 'target' file based on the modification times of 'dependency' files of the target.

- In some cases those dependencies' modification times can change _without_ the contents of the files changing, thus forcing an unnecessary rebuild.

- If `make` was to decide whether to rebuild by looking at the hash of the contents of the dependency files instead, it would only rebuild when the contents changed.

- I wrote a utility for doing this as a simple makefile to include, and it is on Github here: [hashdeps](https://github.com/olipratt/hashdeps)

## Background

A common thing I do when working in a Git repo is switch branches to play about with something on a separate branch, then swap back to the main branch I was working on.

[Git does not store modification times](https://stackoverflow.com/questions/2179722/checking-out-old-file-with-original-create-modified-timestamps/2179825#2179825). When Git changes a file -- say in the above case to replace the copy in the original branch with the version from the new branch, then again to replace it with its original contents on the first branch -- it updates the modification time of the file to be the current time, i.e. the same as if I'd just written the file myself.

Now when you run a `make` command on this repo, make thinks all these files are newly modified, so all the targets that depend on them need rebuilding -- even if the file content is the same as the last time it built.

Wouldn't it be better if `make` instead could tell that the dependency files used to build a target hadn't actually changed, so didn't rebuild anything?

## Does this Already Exist?

From various searching online I couldn't find any standard solution to this problem. A fair few Stack Overflow answers amounted to 'use [Scons](http://scons.org/) instead', which seems to support looking at files hashes natively. But I like make and have used it extensively already, and don't want to add more dependencies to small projects -- a big advantage of GNU Make is that it's basically always available.

After a bit more searching, I did find a [12 year old article](https://www.cmcrossroads.com/article/rebuilding-when-files-checksum-changes) which outlines a hack to use file hashes, but in the opposite way to my main use case -- forcing a rebuild if the contents of a file change, but the modification time of the file is still older than the target.

From this though I thought I could probably take a stab at adapting this to my use case, and hopefully implement something sufficiently generic that this doesn't have to be solved again.

## Attempting an Implementation

I was ready to start giving this a try. Following the article above, creating a file containing the hash of a dependency and inserting it as a dependency in between the target and dependency -- i.e. replace the dependency chain `a <- b` with `a <- hashfile <- b` -- seems like a solid start.

### Testing

First though, I wanted to be sure I could test anything I made worked. My default would be to go for writing tests in Python, but given this was going to be just running `make` and looking at files, it felt overkill, so I looked around for shell-based test frameworks.

I found two main ones:

- [shunit2](https://github.com/kward/shunit2) - inactive for several years, but with a recent burst of activity.
- [bats](https://github.com/sstephenson/bats) - inactive for a few years now. Introduced me to [TAP](http://testanything.org/) which was something I'd never heard of before, but as far as I can tell it never took off.

The big swinger here for me was that `shunit2` is actually packaged up -- `apt-get install shunit2` 'just works' -- plus the interface matches the `junit` style of test writing I'm familiar with from Python's `unittest`, so I went with that.

So now we have a [first commit of a failing test](https://github.com/olipratt/hashdeps/commit/cb83540cce7304f4b660d23786af41910a9c8582) -- time to get to work!

### Better Understanding of Make

I was very keen to have a simple interface for this utility - in particular, I wanted to be able to add this to any existing makefile by tweaking it as little as possible (i.e. not rewriting all rules with some custom logic for each one), and, if it was going to mean having to change the internals of other makefiles,  then be able to seamlessly enable/disable it from doing anything easily.

I still couldn't quite see how this was going to work though, because my understanding was that make:

- first reads all the make files to build up the hierarchy of dependencies, then
- works out what things need rebuilding -- i.e. in the hierarchy `a <- b <- c`, touching `c` means make decides `a` and `b` need rebuilding, so queues up jobs to build each of those,
- finally starts running all the jobs, parallelising any if possible.

However, the second point above is wrong. After running several jobs with `--debug=a` passed to `make` to get lots of detailed logs out, I worked out that make actually builds a dependency of a target and _only then_ compares the timestamp of the dependency and target. So if you don't touch the dependency (i.e. in our case, check that the hash in the file matches so don't touch it), then make will look at the target, decide 'oh this is already newer so nothing to do here!' and move on.

With this I could build a working utility for my use case.

### Supporting More Use Cases

Now that I had my use-case working, it made sense to also add in support for the case from the old article above -- forcing regenerating the hash each time to handle the dependency having changed but still having an older modification time than the target. I added that behaviour, controlled by a configuration flag - `HASHDEPS_FORCE`.

That still left some undesirable behaviour -- in the case where the dependency isn't changed, but somehow the hash file is newer than the target, then we still rebuild the target. Since make is still in control of deciding what to build, and the hierarchy of dependencies is `a <- hashfile <- b`, a newer `hashfile` forces rebuilding of `a`.

Now using our knowledge of how make decides if it needs to rebuild a target, what if we push the modification time of the hash file _back in time_ so it's definitely older than the target? It turns out that does work -- so by setting the modification time of the hashfile back say 5 years if the hash it contains still matches the hash of the dependency, we can be confident that the target won't be rebuilt!

To best see how all cases are handled, [the table in this Unit Test file](https://github.com/olipratt/hashdeps/blob/master/tests/test_mod_time_combinations.sh) covers all the cases, and the tests below it check that they really are handled as described.

In particular notice that now the 'force' case rebuilds the target 'if-and-only-if' the dependency file has actually changed -- so it always does the right thing, at the cost of having to always recalculate the hash every build.

## Result

The output of all this is that there's now a makefile available that can be included in any other makefile-based build system to add this dependency hashing functionality.

Here it is: [hashdeps](https://github.com/olipratt/hashdeps)

[The API](https://github.com/olipratt/hashdeps#converting-a-target-to-use-hashed-dependencies) is as clean as I could make it -- you just wrap any dependency names in a make function call `hash_deps`, and wrap any uses of built in make variables referencing dependencies in `unhash_deps`. _(It does mean that you have to edit any targets you want to use this, but something like that would be necessary anyway unless it was going to apply to all targets blindly.)_ Also, just setting the make variable `HASHDEPS_DISABLE=y` disables any hashing function, so your makefiles behave exactly as if `hashdeps` wasn't even there.
