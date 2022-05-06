---
Title: Motivation and Data
Date: 2022-01-01 16:30
Category: Template
---

Link to [Github repository](https://github.com/DrJupiter/02467-final)
Link to [Noteboo](https://github.com/DrJupiter/02467-final/blob/main/main.ipynb)

# Why study the Russia-Ukraine war?

War is a topic whose terrible importance speaks for itself. The question is rather: what can we as data scientists contribute by analyzing it? One particular aspect of this war that arguably lends itself well to a computational social science analysis, is that both sides arguably frame it as a matter of protecting citizens who they perceive as part of their national community. Consider the following quote, which is how Vladimir Putin begins an essay from July 12th 2021: 

“During the recent Direct Line, when I was asked about Russian-Ukrainian relations, I said that Russians and Ukrainians were one people – a single whole. These words were not driven by some short-term considerations or prompted by the current political context. It is what I have said on numerous occasions and what I firmly believe.“

In this article Putin seems to genuinely believe that Ukraine and Russia essentially are one country. Furthermore, he contends that many if not most Ukranians will perceive a reunion with Russia as a liberation, whereas the Ukrainian government - quite naturally - view Russia's actions as an attack. As such, both sides thereby implicitly stipulate that ‘the people’ will have a positive or negative sentiment towards the Russian ‘liberation’ or ‘attack’ depending on which side is asked. However, this is not something that needs to be stipulated, but can in theory actually be measured since it is an empirical question. This is what we set out to do in this project, by using Twitter data as a proxy for public sentiment.  

It seems that the Russian military offensive is going worse than they anticipated, which can only be attributed to the Ukrainian opposition being fiercer than Russia expected. This begs the question: “Did Russia misinterpret the Ukrainian sentiment at the outset of the war? Or did the war worsen the Ukrainian sentiment towards Russia, which might explain the stronger than expected opposition?” . We also use network analysis to test Putin’s claims about Russia and Ukraine being essentially  “one people”  and see if the war has had an effect on the interaction between users on Twitter. Specifically, we anticipate that the war will have a polarizing effect such that people of different sentiment will interact less.

# Data Collection

This project uses Twitter data gathered using the Twitter API v2. The API allows developers to pull Tweets based on a list of keywords. We based our data collection on a dataset of dehydrated Tweets created by an international research team who continuously update it as the conflict progresses (REF). For these Tweets to be dehydrated means that the dataset only contains Tweet ID’s, which is required by Twitters’ guidelines for data sharing. Subsequently, we hydrated the Tweets from the first 20 days of the conflict from 27/02/2022 - 18/03/2022 using the Twitter API v2. The dataset in its hydrated form consists of 850K usable Tweets with the following variables available:

- tweet_id
- user_id
- parent_id
- language
- text
- created_time
- hashtags
- topics
- mentions

The text was cleaned by removing links using regex, a string pattern searching technique, and translating emojis into text. Thereafter, the text was translated to english using google translate. It was essential to translate the emojis, as they carry a lot of emotion, thus affecting the semantic score. Without translating them, google translate would simply have removed them.

A potential complication in basing our analysis on a pre-collected set of dehydrated Tweets, is that we did not have control over how these were collected. The authors of the employed dataset describe the purpose of their collection as: “This data can help in studying the political discourse, opinion mining, and (mis)information propagation on Twitter”
[Ehsan-Ul Haq, Gareth Tyson, Lik-Hang Lee, Tristan Braud, and Pan Hui, “Twitter dataset for 2022 russo-ukrainian crisis,” 2022](https://arxiv.org/pdf/2203.02955.pdf)
This aligns well with our purpose of investigating potential developments in the sentiment on the conflict, as well as the conflict’s effect on inter- and intra-community interactions.

## A closer look at the data collection

In order to gain more information on the dataset, we investigated how the data was collected. Initially the daily volume of tweets can be plotted:

![Daily volume]({static}/images/volumedaily.png)


It is surprising that the daily volume maintains a relatively constant level, which suggests that a daily cap might be limiting the data collection.
The researchers who collected  the dataset make no mention of an API limit, but we hypothesize that they were given ‘Academic Research’ access, which sets a limit of 10 million Tweets/month or a daily limit of just over 300.000 Tweets.
To see if such a limit inhibits the data collection, we looked at the distribution of time of day the Tweets were made over the entire period:

![Daily Frequency]({static}/images/tweetfreq.png)

As seen, the Tweets are spread over the entire day for all days, which makes it less likely that the data collection was limited by a fixed daily cap. This instead suggests that the relatively constant daily volume of Tweets on the conflict is representative of the actual interest in the conflict being stable throughout the first 20 days, except for a slight bump in the first two days of the conflict. One potential reason for this surprisingly constant daily volume of Tweets is that the data was collected using a list of hashtags and mentions. It might be that daily fluctuations in the frequenicies of these cancel each other out.
A side effect of the data collection relying on hashtags and mentions is that users who do not utilize these are not included in the dataset. This includes the Ukrainian President Volodymyr Zelenskyj who does not use any of the hashtags or mentions used in the data collection.

# Repurposing the data

Tweets are a ready-made data source, since their authors did not directly intend for them to be part of this analysis. For this reason, it is important to consider which limitations, advantages and potential this poses. The intention of most users tweeting on the conflict is presumably to voice their opinion on the Ukraine-Russia conflict and thereby position themselves politically in relation to it. An advantage of our approach is therefore, that there likely is a pretty good overlap between what the data was originally meant for and how we utilize it; namly sentiment- and network analysis.


However, a significant disadvantage of Twitter data in relation to our research topic lies in its unrepresentative user base.
Multiple studies have found that Twitter users are on average younger, better educated and more politically active and therefore not representative of the general population [Pew Research Center, "Sizing up Twitter Users", 2019](https://www.pewresearch.org/internet/2019/04/24/sizing-up-twitter-users/).
Furthermore, we are particularly interested in analyzing potential developments in the interaction between communities whose sentiment differs on the topic.

For this reason, it is not ideal that the dominant sentiment on Twitter is anti-Russian, as is illustrated in the following figure,  which shows the development of sentiment over the time period:


![Russia Support]({static}/images/russia-support.png)

<center>This plot shows a sentiment metric concerning support for Ukraine, in Tweets made by what we through a proxy have determined to be Russian and Ukrainian users in our dataset. The specifics of these metrics will be explained later.</center>

## A western bias

The reason for this observed anti-Russian bias is likely because very few Russian-speaking people use Twitter and instead use the similar platform ‘VK’, which has a reach of over 73% in Russia as compared to [14% of Twitter](https://www.statista.com/chart/26988/most-popular-social-media-in-russia/). _This is also illustrated in the figure below_.
In our hydrated dataset, we do not have access to geolocation due to [Twitter policies](https://developer.twitter.com/en/developer-terms/agreement-and-policy).
Instead we use language as a proxy for nationality. This is an imperfect measure because Russian is the dominant language in some regions of Ukraine and is [the first language of 30% of the population](https://translatorswithoutborders.org/wp-content/uploads/2021/07/Ukraine-Language-Map.pdf)

![Ukraine Social Media]({static}/images/socailmedia.png)

As shown in the first figure below, we find that the distribution of language in our dataset is heavily dominated by English, with Russian and Ukrainian taking up less than 1% combined. When looking at users who have made at least one post in Ukrainian or Russian and taking this as a proxy for their nationality, the proportion of Tweets made by Ukranians and Russians increases slightly as seen in the second figure below. 

![Langauge Distribution]({static}/images/pie_stock.png)
![Langauge Distribution]({static}/images/pie_lang_proxy.png)

# The Ukrainian-Russian subset of the data

When restricting the dataset to Tweets made by users identified as Ukrainian or Russian using the abovementioned proxy, the dataset consists of 7068 unique users and 16045 Tweets. This will constitute our primary dataset for the remainder of the project. There are two main reasons for this choice:

1.) It is the sentiment and networks of Ukrainian and Russian users that are most relevant for answering the research questions we set out in the beginning.

2.) Preprocessing the data is computationally quite heavy and time consuming. It is therefore infeasible to e.g. translate all foreign Tweets to English. This issue is circumvented by only focusing on Ukrainian and Russian users, whose Tweets only constitute 1.95% of the dataset.

However, this choice also has some disadvantages. Firstly, our proxy for nationality is imperfect as described earlier. Presumably many Ukrainians only Tweet in English, since this is the dominant language on Twitter, and these are left out of our analysis. Secondly, the resulting dataset is relatively small and this limits the potential for interactions between users within the dataset. 

