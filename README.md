#Exploring Diddle Soup

Five years ago, when I started being interested in Irish Folk music I thought it sounded to me like Diddle Soup.
When I went all bright eye to the sessions and sat not really playing my flute because I could barely make noise on it, I would hear musicians discuss how they thought that this, or that other tune (its only called a song if someone is singing, if its just instruments its called a tune) was very interesting. I would sit there and silently think to myself: "I have no idea what they were talking about!", because frankly, to me they all sounded the same.

But, I was hooked to the idea of playing the flute. So I kept practicing and I kept going back to sessions. And I realized that I would walk away with three or four notes stuck in my head. They would cycle over and over just like a line of a popsong does when I listen to the radio. In German that's called an "Ohrwurm" literally: Earworm. The earworms would get longer. I remember the day that a whole A part (most likely 8 bars of music) was stuck in my head while I was trying to sleep. It felt like a major milestone in my musical development.
All this is to explain the motivation for my project. I wanted to see if a Machine Learning Algorithm, just like my brain, could start learning the patterns of Irish Folk Music.

As I am also a linguist and think about the world predominantly in terms of language, I wanted to use a data driven approach to finding the patterns that my brain were supplying me with. Ultimately I wanted to see if music is a language. I thought that using a language model to predict the patterns of Irish Folk Music would give me some insight.

My data came from: [TheSession.org tunes](https://github.com/adactio/TheSession-data).

It turns out that n-gram models work rather well for this purpose.

N-gram models essentially look at n-1 sized amount of history before a token to predict how perplexed the model is by a given token. The perplexity being the inverse of the log probability of a given token. Log probability is used because of underflow errors.
The other problem with n-grams is that they tend overfit so they tend to perform poorly on new data unless the test data is very similar to the training data.
This is thought was an advantage in my case because part of my reason for choosing Irish Folk was its in group similarity, which I thought could either be an advantage or a disadvantage.

I built a character based ngram Model. I built an individual n-gram class that has an arbitrary sized n. On top of that I built an ensemble model that takes an arbitrary number of n-gram classes. When calculating the pseudo probability of the ensemble model, each contributing n-gram model gets to put in a weighted vote based on that models pseudo probability. I used grid searching to find a good set of weights to set as default. I found differences is weights based on the number of n-gram models I included but not for different subsets, like the tunes that were reels vs the tunes that were not or were jigs.
