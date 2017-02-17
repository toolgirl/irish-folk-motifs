#Exploring Diddle Soup

Five years ago, when I started being interested in Irish Folk music I thought it sounded to me like diddle soup.
When I went all bright eye to the sessions and sat not really playing my flute because I could barely make noise on it, I would hear musicians discuss how they thought that this, or that other tune (its only called a song if someone is singing, if its just instruments its called a tune) was very interesting. I would sit there and silently think to myself: "I have no idea what they were talking about!", because frankly, to me they all sounded the same.

But, I was hooked to the idea of playing the flute. So I kept practicing and I kept going back to sessions. And I realized that I would walk away with three or four notes stuck in my head. They would cycle over and over just like a line of a pop-song does when I listen to the radio. In German that's called an "Ohrwurm" literally: Earworm. The earworms would get longer. I remember the day that a whole A part (most likely 8 bars of music) was stuck in my head while I was trying to sleep. It felt like a major milestone in my musical development.


All this is to explain the motivation for my project. I wanted to see if a Machine Learning algorithm, just like my brain, could start learning the patterns of Irish Folk Music.

As I am also a linguist and think about the world predominantly in terms of language, I wanted to use a data driven approach to finding the patterns that my brain were supplying me with. Ultimately I wanted to see if music is a language. I thought that using a language model to predict the patterns of Irish Folk Music would give me some insight.

It turns out that n-gram models work rather well for this purpose.

N-gram models essentially look at n-1 sized amount of history before a token to predict how perplexed the model is by a given token. The perplexity being the inverse of the log probability of a given token. Log probability is used avoid underflow errors.
One of the drawbacks of n-grams is that they have a tendency for overfitting, which meants they tend to perform poorly on new data unless the test data is very similar to the training data.
This I thought was an advantage in my case because part of my reason for choosing Irish Folk was its in group similarity, which is what makes it sound like diddle soup.

## The Data:

My data came from: [TheSession.org tunes](https://github.com/adactio/TheSession-data). [TheSession.org](https://thesession.org/) is a crowdsourced resource for mostly lay musicians who choose to enter tunes or versions of tunes for sharing.
This means there is not really any quality control on whether or not they were entered correctly.
In general my data was fairly clean in the sense that I had initially around 28K rows that after cleaning left me with around 26.5K rows.
Given the crowdsourced origin of my data I decided to drop NaNs and or tunes that were probably entered into the wrong field on the original website.

While the predominant amount of tunes are Irish on this website there are a significant amount of Scottish, Swedish, possibly Welsh and Mazurkas originally from Poland. I decided to deal with that by deleting anything that I specifically knew not to be Irish. These were: strathspeys, three-twos and mazurkas. I also deleted the obviously wrong entries.

This is an incomplete solution as there are plenty of Scottish reels and jigs. However, within the timeframe of the two weeks I had to complete my project I did not have time to do the research I would need to separate the Irish from the Scottish tunes. Additionally, I would argue that the differences between Scottish and Irish folk music, while important when executing the game that is playing folk music, are unimportant from a linguistic perspective. These being comparable to two very closely related languages that have significant lexical and grammatical overlap. An example in language terms would be Hawai'ian and Maori. For that reason I decided to go ahead with the assumption that jigs and reels are close enough.

I considered normalizing the data. I considered using [midi note numbers](http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm) to abstract away from the 

As my music was in .abc notation which is at its essence characters to represent the notes of the scale with a key indicator to put the characters in their musical context. That means if the tune is in Gmajor all the f's are sharp without needing to expressly state each sharp or flat.









## Approach

I built a character based ngram Model. I built an individual n-gram class that has an arbitrary sized n. On top of that I built an ensemble model that takes an arbitrary number of n-gram classes. When calculating the pseudo probability of the ensemble model, each contributing n-gram model gets to put in a weighted vote based on that models pseudo probability. I used grid searching to find a good set of weights to set as default. I found differences is weights based on the number of n-gram models I included but not for different subsets, like the tunes that were reels vs the tunes that were not or were jigs. (All of these can be found in the src folder.)
