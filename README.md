#Exploring Diddle Soup

Five years ago, when I started being interested in Irish Folk music I thought it sounded to me like diddle soup.
When I went all bright eye to the sessions and sat not really playing my flute because I could barely make noise on it, I would hear musicians discuss how they thought that this, or that other tune (its only called a song if someone is singing, if its just instruments its called a tune) was very interesting. I would sit there and silently think to myself: "I have no idea what they were talking about!", because frankly, to me they all sounded the same.

But, I was hooked to the idea of playing the flute. So I kept practicing and I kept going back to sessions. And I realized that I would walk away with three or four notes stuck in my head. They would cycle over and over just like a line of a pop-song does when I listen to the radio. In German that's called an "Ohrwurm" literally: Earworm. The earworms would get longer. I remember the day that a whole A part (most likely 8 bars of music) was stuck in my head while I was trying to sleep. It felt like a major milestone in my musical development.


All this is to explain the motivation for my project. I wanted to see if a Machine Learning algorithm, just like my brain, could start learning the patterns of Irish Folk Music.

As I am also a linguist and think about the world predominantly in terms of language, I wanted to use a data driven approach to finding the patterns that my brain were supplying me with. Ultimately I wanted to see if music is a language or has many of the features of a Language. I thought that using a language model to predict the patterns of Irish Folk Music would give me some insight.

It turns out that n-gram models work rather well for this purpose.

N-gram models essentially look at n-1 sized amount of history before a token to predict how perplexed the model is by a given token. The perplexity being the inverse of the log probability of a given token. Log probability is used avoid underflow errors.
One of the drawbacks of n-grams is that they have a tendency for overfitting, which meants they tend to perform poorly on new data unless the test data is very similar to the training data.
This I thought was an advantage in my case because part of my reason for choosing Irish Folk was its in group similarity, which is what makes it sound like diddle soup.

## The Data:

My data came from: [TheSession.org tunes](https://github.com/adactio/TheSession-data) on github. [TheSession.org](https://thesession.org/) is a crowdsourced resource for mostly lay musicians who choose to enter tunes or versions of tunes for sharing.
This means there is not really any quality control on whether or not they were entered correctly.
In general my data was fairly clean in the sense that I had initially around 28K rows that after cleaning left me with around 26.5K rows.
Given the crowdsourced origin of my data I decided to drop NaNs and or tunes that were probably entered into the wrong field on the original website.

While the predominant amount of tunes are Irish on this website there are a significant amount of Scottish, Swedish, possibly Welsh and Mazurkas originally from Poland. I decided to deal with that by deleting anything that I specifically knew not to be Irish. These were: strathspeys, three-twos and mazurkas. I also deleted the obviously wrong entries.

This is an incomplete solution as there are plenty of Scottish reels and jigs. However, within the timeframe of the two weeks I had to complete my project I did not have time to do the research I would need to separate the Irish from the Scottish tunes. Additionally, I would argue that the differences between Scottish and Irish folk music, while important when executing the game that is playing folk music, are unimportant from a linguistic perspective. These being comparable to two very closely related languages that have significant lexical and grammatical overlap. An example in language terms would be Hawai'ian and Maori. For that reason I decided to go ahead with the assumption that [jigs](https://en.wikipedia.org/wiki/Jig) and [reels](https://en.wikipedia.org/wiki/Reel_(dance) are close enough.

I considered normalizing the data. I considered using [midi note numbers](http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm) to abstract away from the key bound notes. Though again the time constraint and the inconsistency of the data gave me pause. I decide instead to go ahead with the data as is. I can argue for normalizing and saying that it would be interesting to see how things behave if I remove the key differences. I also think that it is useful to take key information into account since one could argue that the key of a tune gives rise to the patterns in it.

.abc notation which is at its essence a string of characters representing the notes of the scale with a way of showing which octave is meant. There is a key indicator to put the characters in their musical context. That means if the tune is in Gmajor all the f's are sharp without needing to expressly state each sharp or flat.

The data I ended up using to train any of my models was the column of the data frame that contained the string that was the part of the [.abc notation](http://abcnotation.com/) that is the actual melody.

This was useful because it meant my classifier never saw the mode column. Its possible to argue that the key is implied in the characters and that's true and as far as I can see acceptable since that is what it is looking for.

## Approach

I decided to use n-grams. I made this choice because even though n-grams have a tendency to overfit and not work very well if the test data is very different from the training data. In the case of my data this is actually exactly the case. Since the similarity of my data was precisely what interested me about it.

N-grams work with the idea of looking at a token and the n-1 sized piece of history before the token that I'm interested in. In written language a token can be a word or a character. The exception being a unigram which doesn't have any history. In English it is common on a character level to use unigrams, bigrams and trigrams, and combining them to let them weigh in on the likely hood or the perplexity which is the inverse of the likelyhood of a give token following a given set of history.

As this was not English I didn't know how much history I needed to include so I built a model that could take any size n.

Since my data came as string I decided to build a character based ngram model. I built an individual [n-gram class](https://github.com/toolgirl/irish-folk-motifs/blob/master/src/n_gram.py) that takes an arbitrary sized n. On top of that I built an [ensemble model](https://github.com/toolgirl/irish-folk-motifs/blob/master/src/ensemble.py) that also takes an arbitrary number of n-gram classes. When calculating the pseudo probability of the ensemble model, each contributing n-gram model gets to put in a weighted vote based on that models pseudo probability.

The training of the model involves counting the tokens and their history and calculating the frequency of a token given that particular set of history.
That means the frequencies can be very small. In either model the frequencies get multiplied to determine the probability. This can cause underflow errors since these are all very small. To avoid those I added the frequencies in log space. Hence I have a pseudo probability. Since the perplexity is the inverse of the probability and needs to take the numbers back out of logspace I decided to continue on with the pseudo probability as the vote cast by a given model is relative anyway and simply a higher pseudo probability is a good enough measure.

I used grid searching to find a good set of weights to set as default.
I had a lot of trouble finding a set of weights that didn't just give the model with the most history a weight of 1. This makes sense in some way since obviously the most history would give a model a better capacity to predict a given token. I'm fairly certain it is something to do with not normalizing the frequencies so that a frequency of a longer piece of history would have a bigger frequency since it would not show up as often and therefore it ends up being closer to 1 than one of the smaller models that may have more different inciendences of a particular piece of history.

In the end when going rather high and including up to 15-gram I found the ensemble model not giving any weights to the models with n < 6.
That is why I decided on that as the default setting.

I did find differences in weights based on the number of n-gram models I included but I didn't find any differences when training the model on different sets of tunes. In the sense that I trained the models on tunes that were reels and tunes that were jigs and there were no differences in the number of models to include.
I had hoped there were, as that would allow me to possibly train a classifier for the kind of dance.

## Classifier

I also built a [classifier](https://github.com/toolgirl/irish-folk-motifs/blob/master/src/classifier.py) that as of now has been trained on tunes in G and D and can classify previously unseen tunes in D and G.
This was in part to test if my models really worked. Since was a somewhat unsupervised problem and I didn't really know if my models were indeed coming up with ways to find the patterns in Irish folk music.
The other reason for a classifier was that the website I got my data from is populated by volunteers and not everyone has the background in harmony to correctly identify a tune. I thought that it would be useful to add a model to the website that makes a key suggestions when someone enters a tune into it.
The classifier consists of two ensemble models trained on different datasets.
So far in was trained on a roughly equal number of tunes in G and D and then given a set of new tunes in D and G to classify.
The results were encouraging with an F1-score of 0.95. One part that was interesting to me was that the models never saw the key of a given tune because that was a separate column of my data frame and I did not include that in the training (or testing) data.
However, just in case I was fooling myself, given such a high F1-score I decided to train the models on tunes in mixed keys and try then give them the same set of test tunes in D and G to classify and now the F1-score was 0.57.


## Generator
My approach also gave rise to a generator class as part of the ensemble model.
I generated a string of characters based randomly selecting from my set of models based on the weights of the models. Then it randomly selects from the possible tokens given the chunk of history that model can see.
An example of the music I generated can be found [here](https://soundcloud.com/zia-rauwolf/full-generated-tune?in=zia-rauwolf/sets/n-gram-generated-irish-tunes).
[Here](https://soundcloud.com/zia-rauwolf/presentation-tune?in=zia-rauwolf/sets/n-gram-generated-irish-tunes) are the last 13 seconds of the same tune.

I have found a number of interesting things about my generated music. It seems that the midi player struggles with playing something that has no bar lines. I'm guessing that is why there are these long notes when they are written. The generated tune chunk looking like this:

'4Bd4dFAGa2gGfBA2eBGAEFEGFGEF4AdGcdcdBdg2bfgdBgAefGe2dgfed2ABGz2GA2BcAG'

This is only an excerpt and this piece seems to be short enough not to confuse the midi player. However anything longer than ends up with these long notes.

I think this raises the other issue I see with the generated music. While the intervals are convincing to sound like Irish music and music in general, the lack of overall structure makes is sound like [muzak](https://en.wikipedia.org/wiki/Muzak).

Traditional dance music in general has structure and often repetition since the dancers need it to base their dances on.
I think the way I could replicate that which would be for future work is to add an n-gram model that looks at whole bars of music as the token. This I think would be the equivalent of the word based n-grams in spoken or written languages.


## Patterns

One of the things that most interested me about the project was to find out what were the most common patterns in Irish music.

What I found was surprising to me and yet not on second thought.

I decided to look at the token plus the history to get an idea of the patterns.

When looking at the twenty most frequent patterns in the larger windows, reasoning that the smaller patterns wouldn't be that useful since they wouldn't be big enough to give me much information, I found that with a few exceptions the predominant patterns were scales with the occasional arpeggio or turnaround in it. So the most common run of 6 notes in the key of G is: [https://github.com/toolgirl/irish-folk-motifs/blob/master/img/edcBAG.png]


## Conclusions




- Data exploration and integrity: Is my data usable? What does my data look like?
- Provide clean code along with your analysis in a separate .py file
This will be looked at and evaluated Feature Engineering and Model Building
- Conclusions
- Future Work


## Results


## Future Work
 - Key suggester
 - normalizing data and training
 - word based n-gram equivalent by using the bar as a word boundary
