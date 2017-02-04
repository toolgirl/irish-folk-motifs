Plan:
  I found the vocabulary of Irish folk music.
  Now I constructed the densest possible excecise so that people can become irish musicians, fast.


Sat 1/14/2017
  I have a now the dataframe read in.
  I want to make it a class somehow but I'm a little lost on how.
  I have a variable that is holding the types and their number (pd.Series object)
  I am going to play the different cells and then I'm going to decide what they are and delete or do whatever with them.
  Where did the abc2midi happen with this little script?
  Ask Ben to help me with actually writing abc2midi so that I can test my data and decide how to deal with the 19 odd rows.
  Find a way to listen to a row of a dataframe.
  get the info from the API as well, because I want to learn how.

Thur 1/19
  - make a powerpoint.
  - show screenshots of app
  - make app for categorizing keys that shows sheet music and    has an input box that adds that to the given tune.


Sat 1/21
 - make sure to put dependencies in the README.
 - add sheet music capacity
 - clean out my data.


 Mon 1/23
 - Add in O'Neils? -Done
 - Figure out normalizing the data for key.
 - Midinumbers. REad in as midi and translate?
 - calculate the distances?
 - easier just to do it?

 Tues 1/24
  - Just calculate the numbers?
  - Think about numbers vs letters?
  - can I use tfidf if I have letters?
  - unigramms?
  Midinumbers:
  - go through and replace all 2  with the preceding letter
  - Matrix rows represent major keys
  - columns represent every possible abc note

Wed 1/25
 - I am going to figure out my frequencies for each value of the key of self.n_characters
- figure out perplexity tomorrow!


Fri 1/27
 - Whitespace
    - meaningful
      - because reels 4 and then Whitespace, jig 3 then Whitespace
      -
    - not meaningful
     - midi player doesn't care.
     - very inconsistent transcription

     might be modeling the transcriber not the tune type.

     Run it both ways so that I can figure out which model fares better.


Monday 1/30

 - My model can decide on the weights once its been trained.
 - Normalize by number of keys in the self.char_counter?


 Tuesday 1/31
 When I run a 10 gram ensemble model with the subset of just oneills 1001 tunes I get a set of weights that is:
 (0.0,
 0.20000000000000001,
 0.20000000000000001,
 0.20000000000000001,
 0.20000000000000001,
 0.0,
 0.0,
 0.0,
 0.0,
 0.19999999999999996)

 OUtput of running 10 models on 200 tunes.
 weights         score   n
2                                               (1,) -72980.523537   1
1                                         (0.2, 0.8) -61623.108102   2
9                                    (0.2, 0.0, 0.8) -52800.661925   3
0                               (0.2, 0.0, 0.4, 0.4) -50285.288484   4
5                          (0.2, 0.0, 0.4, 0.2, 0.2) -50122.999317   5
3                     (0.2, 0.0, 0.4, 0.2, 0.0, 0.2) -51544.931776   6
8                (0.2, 0.0, 0.4, 0.2, 0.0, 0.0, 0.2) -53150.030296   7
6           (0.2, 0.0, 0.2, 0.2, 0.2, 0.0, 0.0, 0.2) -54461.632224   8
7      (0.2, 0.0, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.2) -55316.117709   9
4  (0.2, 0.0, 0.2, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2)-56289.876612  10


First output with small data set and no Whitespace:
weights          score  n
2                  (1,) -312750.261835  1
3            (0.2, 0.8) -247041.209264  2
1       (0.2, 0.2, 0.6) -219634.046373  3
0  (0.2, 0.2, 0.2, 0.4) -213132.385580  4

Same dataset(small_reels) with Whitespace:
weights          score  n
2                  (1,) -347983.252884  1
3            (0.2, 0.8) -291016.357700  2
1       (0.2, 0.0, 0.8) -252893.256630  3
0  (0.2, 0.0, 0.4, 0.4) -242419.485299  4

2/2 Thursday:

Started a run for reels and no reels without Whitespace or punctuation


2/3 Friday.
Results of training my classifier on g and d tunes and predicting if d or g.
In [2]: %run run.py
Training model 0
Training model 1
Training model 2
Training model 3
Training model 4
Training model 5
Training model 0
Training model 1
Training model 2
Training model 3
Training model 4
Training model 5
Predicted  Dmajor  Gmajor  __all__
Actual
Dmajor       1699     106     1805
Gmajor         98    1786     1884
__all__      1797    1892     3689
population: 3689
P: 1884
N: 1805
PositiveTest: 1892
NegativeTest: 1797
TP: 1786
TN: 1699
FP: 106
FN: 98
TPR: 0.947983014862
TNR: 0.941274238227
PPV: 0.943974630021
NPV: 0.945464663328
FPR: 0.0587257617729
FDR: 0.0560253699789
FNR: 0.052016985138
ACC: 0.944700460829
F1_score: 0.945974576271
MCC: 0.889348268561
informedness: 0.889257253089
markedness: 0.889439293349
prevalence: 0.51070750881
LRP: 16.1425409606
LRN: 0.0552623061649
DOR: 292.107624182
FOR: 0.0545353366722


Results by traing binary classifier on reels and not reels and getting it to predict D and G.
Training model 0
Training model 1
Training model 2
Training model 3
Training model 4
Training model 5
Training model 0
Training model 1
Training model 2
Training model 3
Training model 4
Training model 5
Predicted  Dmajor  Gmajor  __all__
Actual
Dmajor        792    1013     1805
Gmajor        702    1182     1884
__all__      1494    2195     3689
population: 3689
P: 1884
N: 1805
PositiveTest: 2195
NegativeTest: 1494
TP: 1182
TN: 792
FP: 1013
FN: 702
TPR: 0.627388535032
TNR: 0.438781163435
PPV: 0.538496583144
NPV: 0.530120481928
FPR: 0.561218836565
FDR: 0.461503416856
FNR: 0.372611464968
ACC: 0.535104364326
F1_score: 0.579553812209
MCC: 0.0673822714476
informedness: 0.0661696984668
markedness: 0.0686170650712
prevalence: 0.51070750881
LRP: 1.11790355946
LRN: 0.849196583671
DOR: 1.31642493735
FOR: 0.469879518072

In [3]:
