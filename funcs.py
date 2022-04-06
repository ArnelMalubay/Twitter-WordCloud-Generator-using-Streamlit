# This file contains the functions needed for fetching tweets and performing some text processing on them.

import pandas as pd 
import twint as tw 
import re
import itertools as it

# Fetches tweets satisfying some parameters (name, criteria (most popular vs. most recent), limit) using Twint and stores them in a list
def fetch_tweets(name, crit, lim):
    c = tw.Config()
    c.Username = name
    c.Limit = lim 
    if crit == "most popular":
        c.Popular_tweets = True 
    c.Hide_output = True 
    c.Filter_retweets = True 
    c.Pandas = True
    tw.run.Search(c)
    results = tw.storage.panda.Tweets_df["tweet"].tolist()
    return results

# Performs stopword removal and other text processing on a given text (will be applied per tweet later on)
def list_words(text):
    text = re.sub('[^A-Za-z0-9 ]+', '', text).lower()
    words = text.split()
    v1 = []
    for word in words:
        if word[:4] == "http" or word[:3] == "tco" or len(word) == 1:
            continue 
        else:
            v1.append(word)
    v2 = []
    eng_stopwords = ['you', 'should', 'ourselves', 'seem', 'but', 'every', 'really', 'without', 'beyond', 'afterwards', 'its', 'less', 'rather', 'each', 'thereby', 'us', 'besides', 'who', 'namely', 'on', 'serious', 'all', 'hereafter', 'we', 'anything', 'are', 'nine', 'somehow', 'since', 'whereby', 'thence', 'too', 'name', 'top', 'show', 'anyhow', 'formerly', 'whether', 'my', 'again', 'already', 'the', 'almost', 'except', 'is', 'get', 'per', 'third', 'how', 'call', 'may', 'move', 'part', 'towards', 'became', 'hereby', 'upon', 'above', 'even', 'what', 'when', 'three', 'yours', 'although', 'himself', 'however', 'over', 'same', 'further', 'other', 'elsewhere', 'our', 'now', 'mine', 'being', 'her', 'will', 'someone', 'see', 'onto', 'from', 'did', 'anyone', 'due', 'together', 'hereupon', 'also', 'and', 'nowhere', 'still', 'therefore', 'beside', 'because', 'alone', 'fifty', 'moreover', 'ten', 'four', 'whom', 'where', 'yourself', 'everyone', 'there', 'between', 'perhaps', 'hundred', 'several', 'thereafter', 'them', 'anyway', 'behind', 'during', 'six', 'twelve', 'within', 'around', 'make', 'bottom', 'than', 'was', 'can', 'an', 'else', 'go', 'take', 'using', 'among', 'themselves', 'give', 'nevertheless', 'indeed', 'nothing', 'through', 'always', 'with', 'nobody', 'both', 'something', 'empty', 'could', 'cannot', 'after', 'whereafter', 'used', 'whose', 'he', 'itself', 'much', 'another', 'his', 'into', 'just', 'sometime', 'everywhere', 'your', 'those', 'below', 'thereupon', 'forty', 'former', 'five', 'none', 'full', 'once', 'becomes', 'everything', 'only', 'yourselves', 'about', 'under', 'please', 'most', 'had', 'therein', 'which', 'put', 'have', 'front', 'well', 'whence', 'until', 'two', 'back', 'regarding', 'whither', 'do', 'him', 'ours', 'side', 'to', 'might', 'via', 'up', 'yet', 'otherwise', 'meanwhile', 'latterly', 'ever', 'one', 'fifteen', 'last', 'these', 'has', 'throughout', 'beforehand', 'does', 'done', 'must', 'be', 'eleven', 'others', 'either', 'down', 'nor', 'such', 'toward', 'while', 'here', 'ca', 'herein', 'noone', 'quite', 'wherein', 'herself', 'am', 'amount', 'whoever', 'before', 'next', 'whereupon', 'out', 'as', 'i', 'it', 'by', 'enough', 'never', 'of', 'unless', 'wherever', 'whatever', 're', 'at', 'seems', 'against', 'own', 'along', 'becoming', 'doing', 'a', 'if', 'or', 'whenever', 'me', 'any', 'first', 'keep', 'more', 'say', 'whereas', 'for', 'been', 'become', 'this', 'various', 'whole', 'sixty', 'very', 'across', 'hence', 'mostly', 'amongst', 'no', 'seeming', 'off', 'she', 'sometimes', 'that', 'thru', 'latter', 'made', 'thus', 'why', 'not', 'eight', 'so', 'would', 'anywhere', 'somewhere', 'then', 'often', 'hers', 'twenty', 'though', 'some', 'were', 'in', 'few', 'neither', 'many', 'seemed', 'they', 'myself', 'their', 'least']
    fil_stopwords = ['masyado', 'maaaring', 'ikaw', 'kanila', 'nagkaroon', 'ibaba', 'ano', 'ibig', 'ito', 'iyon', 'kailanman', 'sino', 'saan', 'pero', 'mga', 'ngayon', 'paano', 'mismo', 'iyo', 'kong', 'walang', 'ating', 'kanilang', 'naging', 'gayunman', 'marapat', 'gusto', 'may', 'marami', 'bilang', 'sabi', 'ay', 'katiyakan', 'ang', 'nabanggit', 'pangalawa', 'nila', 'pataas', 'ko', 'paraan', 'atin', 'kung', 'tayo', 'iyong', 'lamang', 'din', 'bawat', 'dito', 'bababa', 'kulang', 'sabihin', 'akin', 'kanyang', 'ka', 'maging', 'sa', 'apat', 'pagitan', 'ginagawa', 'laban', 'ako', 'para', 'isa', 'na', 'pababa', 'pagkatapos', 'muli', 'mahusay', 'nilang', 'ni', 'isang', 'paggawa', 'kaysa', 'sila', 'gumawa', 'iba', 'kanya', 'kanino', 'palabas', 'makita', 'pa', 'ng', 'dalawa', 'amin', 'kahit', 'itaas', 'mayroon', 'hanggang', 'o', 'aking', 'sarili', 'ginawa', 'pagkakaroon', 'una', 'bago', 'narito', 'pumunta', 'kailangan', 'likod', 'nakita', 'panahon', 'aming', 'gagawin', 'alin', 'ilalim', 'kapag', 'am', 'ginawang', 'lahat', 'karamihan', 'nito', 'doon', 'tulad', 'at', 'kumuha', 'namin', 'ibabaw', 'dapat', 'lima', 'maaari', 'inyong', 'nais', 'huwag', 'ilagay', 'napaka', 'katulad', 'niyang', 'pamamagitan', 'siya', 'noon', 'minsan', 'pumupunta', 'habang', 'mula', 'dahil', 'pareho', 'tatlo', 'tungkol', 'anumang', 'kaya', 'hindi', 'kapwa', 'bakit', 'niya', 'kami', 'ilan', 'nasaan']
    for word in v1:
        if word in eng_stopwords or word in fil_stopwords:
            continue
        else:
            v2.append(word)
    return v2

# Returns all the words from tweets satisfying the parameters name, criteria, and limit
def words_from_tweet(name, crit, lim):
    tweets = fetch_tweets(name, crit, lim)
    lists = [list_words(tweet) for tweet in tweets]
    words = " ".join(list(it.chain.from_iterable(lists)))
    return words