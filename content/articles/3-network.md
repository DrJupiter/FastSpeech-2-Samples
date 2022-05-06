---
Title: Network analysis
Date: 2022-01-03 16:00
Category: Template
---

Having analyzed the overall sentiment towards different topics related to the war, we now 
combine this with a focus on networks. As mentioned at the outset, we hypothesize that war will have a polarizing effect on the communities within the network of Ukrainian and Russian users tweeting on topics related to the war. The rationale being that in times of war people can be expected to tone down criticism towards ‘their side’ and conversely also drop any nuances about ‘the other side’, which instead becomes the epitome of evil. For example, the Ukrainian President Volodomyr Zelenskyy has been involved in a number of corruption scandals. His approval rating was below 40% immediately before the war, but has subsequently risen to [over 90%](https://www.reddit.com/r/ukraine/comments/t2ufsn/ukrainian_president_zelenskyy_is_having_90/). With examples like these, we expect to see an increasing difference in the sentiment between and decrease in interaction between these communities over time as the war progresses.  

# Community division based on ‘Ukraine support’ metric

For the rest of this project we will use and test the quality of the division of the network into communities based on their ‘Ukraine support’ sentiment score. This approach has potential issues. Firstly, it is a questionable metric due to ambiguities of how to interpret negative or positive sentiments as mentioned earlier. Secondly, consider which conclusions can be drawn if we find that this is a bad community split (which the next section indeed does) using methods such as the modularity score of the split. In that case, there are a number of scenarios which can explain such a finding:

- 1) Either it is the case that the ‘Ukraine support’ score is uninformative of actually existing communities in the network. This would entail that the ‘Ukraine support’ metric is flawed.
- 2) Alternatively, the ‘Ukraine support’ metric accurately captures the sentiment of the users, but this sentiment is just not a good community split. This would entail that the war does not have a polarizing effect on the network structure, since users with different opinions continue to interact with each other.
- 3) Lastly, it is possible that Twitter is just not a very community oriented forum, but instead mostly a place where individuals scream into the void. 

If the third scenario holds true, we should be able to identify this by analyzing properties of the graph such as the in- and out-degree distribution. A later section shows that this is actually the case. However, this does not exclude either scenario one or two. 

In order to alleviate some of this ambiguity, a final section introduces a new metric, which looks at changes in interactions and once-removed interactions from the first 10 days compared to the last 10 days of the dataset. This will be explained then, but first we examine the communities in the network using the community detection algorithms that we learned in this course.

# Initial graph analysis

Initially we constructed a directed graph, where users replying to or retweeting other users' Tweets are nodes with outgoing edges and users whose Tweets are replied to conversely have ingoing edges. In our network with 7068 Ukrainian and Russian there are 191595 Tweets which are shown as edges in the following figure:

![Network graph]({static}/images/largegraph.png)

The network has 7068 users who are split into three communities:

- 1472 Ukraine supporters (blue nodes)
- 1159 Russia supporters (red nodes)
- 2611 Neutral users (light gray)
- 1118 Users whose Tweets did not allow for classification (dark gray)

The remaining 14326 dark gray nodes are Twitter users that lie outside the dataset in the sense that we do not have access to their Tweets and therefore cannot determine their position towards the conflict. In total there are 20687 nodes and only 19195 edges, which means that the graph is very sparsely connected. As a result, thresholding the graph at a minimum degree level resulted in most of the graph disappearing. 

The sparseness of the graph can also be visualized by plotting the in degree vs. out degree of each user:

![Degree distribution]({static}/images/degree_big.png)

Here we see that all users who have 0 out degree are outside the network as marked by their black color. Most nodes have only 1 out degree, which corresponds to them only having made a single Tweet in the time period. We find very few users have both a high in- and out degree, which suggests that the users retweeting other users are not the same that are being retweeted themselves. This suggests that the graph is heavy-tailed, which is typical for real world networks. 

An issue with having a graph that contains nodes that lie outside our community split is that we cannot determine the strength of the split, since we have no reasonable way of assigning the unknown nodes to a community. For this reason, the following graph partitioning analyses will be limited to the interactions between users that are contained within our dataset. This significantly limits the network and results in a graph with 379 nodes and 280 edges:

![Network graph limited to within dataset nodes]({static}/images/degree_big.png)

Of these users there are:
- 91 Ukraine supporters (blue nodes)
- 76 Russia supporters (red nodes)
- 143 Neutral users (light gray)
- 69 Users whose Tweets did not allow for classification (dark gray)

A similar level of sparseness is observed in this graph as illustrated by plotting in- and out degree distributions:

![Degree distribution in limited graph]({static}/images/degree_small.png)

Our interpretation of these results is that Twitter is a network with relatively few connections - i.e. little interaction between users. This suggests that scenario three as described earlier (Twitter is a place where people shout into the void) seems to hold true.  

# Modularity

With the abovementioned caveat regarding the uncertainty of scenario one (Ukraine support score is uninformative) vs scenario two (Users are equally likely to interact with people with differing opinions on the conflict)  in mind, we now test the strength of the partitioning of the network achieved by using the ‘Ukraine support’ metric. However, what does it mean for a partitioning of a network to be ‘strong’ - i.e. good? It can be argued that a good community split is one in *“which there are fewer than expected edges between communities”*[M.E.J. Newmanm, "Modularity and community structure in networks", 2006](https://www.pnas.org/doi/10.1073/pnas.0601602103).  This is what is captured by the modularity of a community split of a network. A split with high modularity will have many connections within the community but few connections between communities. In other words, modularity can be seen as a relative density measure, where the degree of within-community connectedness is seen relative to the between-community connectedness. 

Our community split has a modularity score of 0.062. In order to get a measure for how high this score is, we compare it to 10.000 degree preserving random networks generated using the double edge swap algorithm. The  mean modularity score of these networks will be normally distributed, which allows us to statistically evaluate whether the ‘Ukraine support’ split is statistically different by seeing if it falls outside two standard deviations of the mean of the randomly generated networks.

![Statistical evaluation of 'Ukraine support' community split]({static}/images/random_small_graph.png)

As is seen in the figure below, our split is not better than random. This can be compared to a community split obtained by using the Louvain algorithm, which results in the following partitions:


![Louvain split]({static}/images/louvain.png)

The modularity score of the Louvain algorithm was found to be 0.93. Again using the double edge swap algorithm and generating 10000 random networks, we can confirm that this is a significantly better community split than random: 

![Statistical evaluation of Louvain community split]({static}/images/random_lou_small.png)

We can therefore conclude that the ‘Ukraine support’ community split is quite bad, but this does not tell us much about the reason for it performing so much worse than the Louvain algorithm. Is it because Ukrainian- and Russian supporters actually interact a lot on Twitter or is it because the metric is too ambiguous making ‘Ukraine support’ and uninformative measure?

In order to investigate this, we calculated something that we call “once-removed-agreement-degree”. This describes how much people are connected to other people who agree or disagree with them looking at their direct connections and their connections once removed, so the connections of their connections.

If a user interacts directly with a user of similar opinion on the conflict, he or she gets a score of +1. If the user interacts with a user who interacts with another user of similar opinion (i.e. interaction once removed), the user gets a score of +½. Conversely, the user gets respectively -1 and -½ for interacting and once-removed-interacting with users of opposite opinion on the conflict. 

The benefit of this measure is that it allows us to extract information from the larger network that also includes nodes outside of the network. Thus we can see if people get news from the same media, consider the same content etc. Positive score implies they are connected to people they agree with, and negative score implies they are connected to people they disagree with. A score close to zero implies they are equally distributed. We find the the following once-removed-agreement scores:

![Once removed agreement]({static}/images/once_removed_degree.png)

We find that both Russia supporters and Ukraine supporters have a positive score, which implies that they interact more with users of similar opinion. This is evidence against the aforementioned scenario two (that users of different opinions interact). As such, it seems that the reason for the low modularity score using the ‘Ukraine support’ community split is likely to be because the metric itself is inaccurate. 