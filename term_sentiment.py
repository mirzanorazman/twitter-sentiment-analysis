import sys

def create_sent_dict(sentiment_file):
    """A function that creates a dictionary which contains terms as keys and their sentiment score as value

        Args:
            sentiment_file (string): The name of a tab-separated file that contains
                                     all terms and scores (e.g., the AFINN file).

        Returns:
            dicitonary: A dictionary with schema d[term] = score
        """
    scores = {}
    afinnfile = open(sentiment_file, 'r')
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    afinnfile.close()
    
    return scores

def get_tweet_sentiment(tweet, sent_scores):
    """A function that find the sentiment of a tweet and outputs a sentiment score.

            Args:
                tweet (string): A clean tweet
                sent_scores (dictionary): The dictionary output by the method create_sent_dict

            Returns:
                score (numeric): The sentiment score of the tweet
        """
    score = 0 
    wordMatched = []
    wintw = tweet.split()
    for wc in range(0, len(wintw)):
        if len(wintw) == 0:
            score = 0
            break
        start_index = wc
        maxStr = ""
        
        end_index = start_index
        phrase = ""
        while end_index < len(wintw):
            phrase += wintw[end_index] + " "
            if phrase.strip() in sent_scores:
                maxStr = phrase.strip()
            end_index += 1

        matched = False
        for w in wordMatched:
                if maxStr is w:
                    break
                elif maxStr in w and len(w.split()) > 1:
                    matched = True
        if not matched and maxStr is not "":
            wordMatched.append(maxStr)
            score += sent_scores.get(maxStr)
    
    return score

def term_sentiment(sent_scores, tweets_file):
    """A function that creates a dictionary which contains terms as keys and their sentiment score as value

            Args:
                sent_scores (dictionary): A dictionary with terms and their scores (the output of create_sent_dict)
                tweets_file (string): The name of a txt file that contain the clean tweets
            Returns:
                dicitonary: A dictionary with schema d[new_term] = score
            """
    new_term_sent = {}
    tweets_score = {}
    new_terms = {}
    
    # Populate new term sentiments
    tweets = open(tweets_file, 'r')

    for tweet in tweets:
        score = get_tweet_sentiment(tweet, sent_scores)
        tweets_score.update({tweet: score})
        
        wintw = tweet.split()
        for words in wintw:
            if words not in sent_scores:
                new_terms.update({words: 0})

    for words in new_terms:
        term_score = 0
        counter = 0
        # go to every tweet which the contains within, then calculate average
        for twt in tweets_score:
            twtStr = twt.split()
            if words in twtStr:
                term_score += tweets_score[twt]
                counter += 1
        # calculate avrg
        term_average = term_score/counter
        new_terms.update({words: term_average})
              
    for words in new_terms:
        new_term_sent.update({words: new_terms[words]})
        
  
    tweets.close()

    return new_term_sent


def main():
    sentiment_file = sys.argv[1]
    tweets_file = sys.argv[2]

    # Read the AFINN-111 data into a dictionary
    sent_scores = create_sent_dict(sentiment_file)

    # Derive the sentiment of new terms
    new_term_sent = term_sentiment(sent_scores, tweets_file)

    for term in new_term_sent:        
        print(term, new_term_sent[term])


if __name__ == '__main__':
    main()