import sys


def create_sent_dict(sentiment_file):
    """A function that creates a dictionary which contains terms as keys and their sentiment score as value

        Args:
            sentiment_file (string): The name of a tab-separated file that contains
                                     all terms and scores (e.g., the AFINN file).

        Returns:
            dicitonary: A dictionary with schema d[term] = score
    """
    afinnfile = open(sentiment_file, 'r')
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    afinnfile.close()
    # print(scores.items())
     
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
    
    #YOUR CODE GOES HERE
    # maximum substring
    # tweet: [not so good]
    # [not], [not so], [not so good], [so], [so good], [good]
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
            
            # wordMAtched = ['not so good']
            # next maxStr = 'so good'
                
        
    return score


def get_sentiment(tweets_file, sent_scores, output_file):
    """A function that finds the sentiment of each tweet and outputs a sentiment score (one per line).

            Args:
                tweets_file (string): The name of the file containing the clean tweets
                sent_scores (dictionary): The dictionary output by the method create_sent_dict
                output_file (string): The name of the file where the output will be written

            Returns:
                None
    """
    tweets = open(tweets_file, 'r')
    output = open(output_file, 'w')
    for tweet in tweets:
        score = get_tweet_sentiment(tweet, sent_scores)
        output.write('%d\n' % score)
    output.close()
    tweets.close()


def main():
    sentiment_file = sys.argv[1]
    tweets_file = sys.argv[2]
    output_file = "sentiment.txt"

    # Read the AFINN-111 data into a dictionary
    sent_scores = create_sent_dict(sentiment_file)
    # Read the tweet data and assign sentiment
    get_sentiment(tweets_file, sent_scores, output_file)


if __name__ == '__main__':
    main()