Title: The C++ Short String Optimisation
Date: 2016-11-19 12:28
Category: Performance
Tags: C++, optimisation, performance

While learning and reading up on C++11 recently, I came across the Short String Optimisation.

I'd at some point been told (or somehow got it into my head), that C `union`s are generally dangerous and are something you should steer well clear of, so I'd never really known what they were about. However, from learning about the SSO it's clear they can make for some very efficient memory use as long as you are careful. (If you're familiar with `union`s this whole thing will probably be underwhelming!).

I'll attempt an explanation here in my own words so I can make sure I understand the topic.

## Deriving the SSO

### Baby Steps

Let's try and implement a C++ `string` class, and be as memory and processor efficient as we can. Assuming a 64-bit system, we'll need at least:

- A `char *string` pointer to the string - the string itself will have to be on the heap somewhere as it can be arbitrarily large,
- A `uint64_t length` - again allowing for arbitrary largeness.

That's pretty good so far, only 16 bytes used and we can manage arbitrarily large strings.

### Minimising Reallocation

Now imagine we're working with a string, and appending `char`s to it to build some bigger string, one-by-one. That means each time one is appended, we have to `realloc` our string, which may well mean a `malloc` of new memory, a `memcpy` of the whole string, and a `free` of the old string. That's far from ideal, so lets add one more field:

- A `uint64_t allocated_length` - this will separately store the size of any allocated memory, meaning we can, for example, double the amount of memory allocated when we run out, to achieve [amortised constant time cost](https://en.wikipedia.org/wiki/Dynamic_array#Geometric_expansion_and_amortized_cost).

Cool, we're up to 24 bytes now and can handle large strings pretty optimally.

### Wasn't This About Short Strings?

What about small strings though? If I create only a little string `Hello world!`, I have to allocate some memory on the heap to hold it. Going further, say I create an array of several two character strings, every single one has to separately allocate and later free memory. That's not great, so lets try and improve it.

We could add a small array to our string class that we use for small strings - say something like:

- A `char short_string[16]` - any 16 byte or shorter string gets put in here.

But then, every string class instance gets 16 bytes bigger, whether it needs it or not, and the space is completely useless for long strings (unless we split them across this array and any allocated memory, but then the string's not contiguous in memory and that's going to make it useless to any number of standard functions that expect that).

So let's not do that - but notice if we did, when the array was in use the `char *string` and `uint64_t allocated_length` would be useless, and they would be wasted instead...

Here's where the `union` steps in - lets define our string class[^1] as:

```cpp
class string
{
  uint64_t length;  // The real string length.
  union  // One of...
  {
    struct  // ...a string on the heap and the memory size if needed...
    {
      char *string;
      uint64_t allocated_length;
    } long_string;
    char short_string[sizeof(long_string)];  // ...or a small array.
  };
};
```

That's a common 8 byte length of the actual string, and then an either-or of:

- pointer-to-string and allocated length
- `char` array of the same size as the above takes up - 16 bytes here.

Now if our string is 16 characters or shorter, we can pack it directly into the memory of the string class itself, and if it's longer, we treat the union as a pointer and length and store the string there instead!

### But Wait, There's More

In the case above that we're using the short string buffer, the largest length we need to store is going to be 15 (assuming the string is stored null-terminated), so the `uint64_t` is overkill. Let's try turning the whole thing into one big `union`, using only a single byte to store the length in the short case:

```cpp
class string
{
  union
  {
    struct
    {
      uint64_t length;
      char *string;
      uint64_t allocated_length;
    } long_string;
    struct
    {
      uint8_t length;
      char buffer[sizeof(long_string) - 1];
    } short_string;
  };
};
```

Great, now our short string can be 23 bytes long, but there's one problem - how do we know which type to treat the `union` as when using this class?

To solve this, we can take advantage of the fact that in the short case we need only about 5 bits to store the length, and  *surely* no-one will mind if we limit them to a paltry `2^63`[^2] byte string, so lets steal the high bit[^3] from the length to act as a flag for whether we're treating the union one way or the other.

### Squeezing Out the Last Drops

There's one final thing we can tweak to do better. As it stands, swapping back and forth from a 23 byte to a 24 byte string means allocating a string and copying into it one way, and then copying back and freeing it the other. Instead once we allocate a string and set the bit flag, we can just never unset it - so when a string shrinks to 23 bytes or less, we just continue using the allocated space.


And that's how we can use just 24 bytes of space to point to arbitrarily long strings *and* still store 23 byte strings without having to allocate any extra memory!


[^1]: I'm not claiming that any real implementations look exactly like any of the ones in this post - but it gives an illustrative idea. [Here's a real implementation, with some good explanatory diagrams](https://github.com/elliotgoodrich/SSO-23).

[^2]: Even modern 64 bit CPUs can't actually address the full 64 bit space - the current limit is about [46 bits](http://www.howtogeek.com/175443/what-is-the-maximum-amount-of-ram-you-could-theoretically-put-in-a-64-bit-computer/) - so this isn't even a real limitation as it stands. (A limit that HP's search-engine-unagreeably-named "The Machine" is coming up against!)

[^3]: Yes, I'm ignoring endianness for the purposes of this post.
