from src.twitter import create_tweet, tweet


def main():
    tweet_text = create_tweet()
    tweet(tweet_text)


if __name__ == "__main__":
    main()