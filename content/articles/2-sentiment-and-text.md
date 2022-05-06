---
Title: Sentiment and Text analysis
Date: 2022-01-02 16:15
Category: Template
---

For the reason that Tweets are a ready-made data source, we cannot ask the users their opinion on the conflict directly, so instead we have to automate the extraction of it using sentiment analysis. Basic sentiment analysis uses a sentiment lexicon, where each word is assigned a real-valued sentiment score that is either positive or negative. A Tweet can then be categorized as positive or negative based on the sum of these sentiments. However, this technique is known to work better for longer documents of text, whereas Tweets of course are rather short.

Instead we will be using rule-based sentiment analysis provided by [VADER](https://github.com/cjhutto/vaderSentiment) which provides a compound score for the sentiment. The compound score is the sum of the normalized sum of the positive, negative and neutral sentiment in a text. The value is normalized to be between -1 and +1.
This combined with knowledge of the topic of the Tweet, which is extracted using context annotations and hashtags. Context annotations are auto-generated keywords, which provide [contextual information about the Tweet based on semantic analysis.](https://developer.twitter.com/en/docs/twitter-api/annotations/overview)

However, this approach is imperfect because it can be ambiguous how to interpret a given sentiment score. Consider for example the following Tweet:

## Not an actual tweet
<center>"Oh my God Ukraine is completely destroyed, I'm so angry"</center>

The topic of this Tweet is “Ukraine” and it has a negative sentiment score, but that does not mean that the author is anti-Ukrainian. In order to disambiguate how the sentiment of Tweets should be interpreted, we do a couple of things: 

1) We assume that opinions on the conflict are binary, such that if you express support for Ukraine you express opposition towards the Russian invasion. 

2) A context window is used for each search word, such that the sentiment is only calculated for the five words on either side. This localizes the sentiment attributed to a topic, which allows a single tweet to express both negative sentiment towards e.g. Russia and positive sentiment towards Ukraine without these necessarily canceling each other out.

3) The sentiment analysis is restricted to only four topics: “Ukraine”,”Russia”,”Putin” and “Zelensky”. Initially we only focused on the two presidents, since it seems reasonable to assume words with negative or positive sentiment within the context window of their names will express either dissatisfaction or support respectively. However, this limited the dataset too much and we therefore also included the countries. 

With this approach, we assign each user a single value describing his or her “Ukrainian support” using the following formula:

![Ukraine Support Formula]({static}/images/uk-support.png)
<center>_The Variables in the sum represent the users sentiment score for those words._</center>

![Ukraine Support]({static}/images/ukraine-support.png)

Looking at the support for Ukraine over time, we see the support is always positive, but somewhat periodic in nature.
We speculated this, the periodicity, might be correlated to certain events in the war, however looking at the [timeline](https://en.wikipedia.org/wiki/Timeline_of_the_2022_Russian_invasion_of_Ukraine) for the war, this correlation was not obvious to us in its existence.

## A deeper look into the parameters for the Ukraine Support Score

![Nation Sentiment All]({static}/images/sentiment-nation-all.png)

This is an illustration of the individual sentiment scores for the words considered in the Ukraine Support. From this we see that Zelinskyy’s score doesn’t fluctuate much compared to the other scores and that most of the Ukraine support comes from negative sentiment towards Russia and Putin rather than positive sentiment towards Ukraine.
This could be due to many Tweets about Ukraine potentially being double negative, however taking a closer look into where the sentiment is coming from

![Ukraine Nation Sentiment]({static}/images/sentiment-nation-uk.png)

<center> Ukrainian users' sentiment contribution </center>

![Russia Nation Sentiment]({static}/images/sentiment-nation-ru.png)

<center> Russian users' sentiment contribution </center>

We see that, besides for Zelenskyy, Ukrainian users show some positive sentiment towards Ukraine, whereas Russian users are almost solely negative, save for the 17th of March.

Looking only at the Tweets tweeted in Ukrainian or Russian reveals an even more interesting pattern.

![Ukraine Language]({static}/images/sentiment-by-lang-uk.png)

![Russian Language]({static}/images/sentiment-by-lang-ru.png)

Ukrainian speech about Ukraine looks to be solely positive and that about Russia and Putin mostly negative. Russian speech about Ukraine is very negative and the words considered are in general negative. Thus, in our dataset at least, Ukrainians don’t speak negatively of their country in their mother tongue.

# Word Frequency

At this point it might be relevant to ask, how often are the words used to gauge the Ukraine Support actually used in the text data?

![Word Frequency Distribution]({static}/images/word_freq.png)

Ukraine, Russia and Putin can be found in the top 5 words, but Zelenskyy only shows up in the top ~40.
The explanation for can be found in the many aliases for Zelenskyy which include:

<center>"Volodymyr","Volodymyr Zelenskyy","Zelenskyy","volodymyr zelenskyy","volodymyr","zelenskyy","ZelenskyyUa","Volodymyr Zelensky","Zelensky","zelensky","zelenskyyua" </center>

Compared to Putin which only had 5 prominent aliases.
This and the fact that after the 10th word, the word frequencies become very close to each other with a slow decline.
Thus the frequency of the 10th most prominent word `military` is not that different from that of `zelensky`.

We also look at the lexical dispersion for some words we deemed relevant to the war. 
The lexical dispersion is constructed based on a document created from all the text, but ordered in regards to when the tweet was created.

![Lexical Dispersion]({static}/images/time-dependent-lexical-dispersion.png)

Here we see that the most prominent words have an even distribution, but something to note is that the word `help` which is also in the top 40 words has a slight decline over time.

# Deeper look into the presidents, word clouds

