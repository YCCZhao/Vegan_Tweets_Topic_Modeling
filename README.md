# Vegan_Tweets_Topic_Modeling

For this project I streamed 459,265 tweets - 145,243 of it are unique, then I applied NLP method for topic model so that it was understood that what people were talking about vegan. The motivation is that being both groups after I became vegan I found that each group has negative sentiment toward the other group. So I hoped through this project, I could find why the reason.

# Project Process

1. Use tweepy to stream tweets for a week
2. Clean tweets
3. Tokenization
4. TFIDF -> LSA -> Similarity Matrix
5. Remove Duplicate Tweets
6. Model1: TFIDF -> LSA -> KMeans
7. Model2: CountVectorizer -> LDA -> Topic modeling

# Detail Steps
1. (This jupyter notebook)[./Request_Tweets_API.ipynb] has the code to request tweet via RESTful API or streamming API. (stream_vegan_tweets.py)[./stream_vegan_tweets.py] has the code of streaming tweets with the word "vegan". Then  the tweets are sved in a Mongo Database. The earlier version of the python code failed to request full text of tweets, thus (Fix_Truncated_tweets.ipynb)[./Fix_Truncated_tweets.ipynb] was written to re-request tweets in extended mode..

2. I removed urls, user names, emoji, and line breaks from the tweets. Then I group them so that each row is an unique tweets, retweets counts also was summed. 

3. Once tweets were cleaned, I used SpaCy for tokenization. I added customized stopwords such as "amp", "think", "want", "like", etc. Lemma of a word was used as token rather than the word itself. Unigram, entities detected by SpaCy, and  noun chunks detected by SpaCy are used as tokens. 

4. After tokenization, token is fed into sklearn's TfidfVectorizer. Then gensim's LsiModel is used to reduce dimension. Then pair-wise cosine similarity is calculated used reduced dimension word vectors. The LsiModel started with 300 reduced dimension, and decreased until 50, then I saw tweets with 0.9 similarity are indeed similar, thus I used 100 reduced dimensions. On top of that, I used similarity matrix to remove duplicate tweets, and add number to retweet counts. 

5. With new dataset that does not have duplicate tweets, I fet them into sklearn's TfidfVectorizer and used gensim's LsiModel to reduce dimensions. Then I used document-topic matrix to fit a Kmeans model. 

6. Different numbers of clusters was tried to find the ideal number of clusters. Based on the elbow plot, 17 cluster seems to yeild a better result. However, the final clusters didn't make much sense. So then I decided to use LDA.

7. 10 Topics were modeled using LDA, and they seem to provide a better insights. The topics seem to be about meat, skincare, recipe, chicken, food, protein, milk, animal, recipe video, and plantbased.

8. I also tried HDP from gensim, HDP should find the best number of topic for you. However the result doesn't seems like better than ones yield by LDA.
