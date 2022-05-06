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

# Present Final end score

# Deeper look into all 4 paramters by lang and by nationality

# Deeper look into the words actually used

# Deeper look into the presidents, word clouds

