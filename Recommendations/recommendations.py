from pymongo import MongoClient
from math import sqrt

class Recommendations:

    def __init__(self, config):
        self.config = config
        self.mongo = MongoClient(config['host'], config['port'])
        self.db = self.mongo[config['database']]
        self.tweets = self.db[config['tweets_db']]

    # Returns a dicionary of a user's ratings of a coffee
    # Currently all the ratings are binary based on whether the user has
    # tweeted about a coffee
    def getUserRatings(self, user_name):
        user_ratings = {};
        for row in self.tweets.find({'tweet.user.screen_name': user_name}):
            user_ratings[row['coffee_id']] = 1
        return user_ratings

    # Returns a list of usernames for the current user
    def getUsers(self):
        return self.tweets.distinct('tweet.user.screen_name')

    # Takes two sets of objects and returns the pearson_correlation between
    def pearson_correlation(self, set1, set2):
        intersection = set(set1.keys()) & set(set2.keys())
        n = len(intersection);
        if n == 0: return 0

        sum1 = sum([set1[coffee_id] for coffee_id in intersection]);
        sum2 = sum([set2[coffee_id] for coffee_id in intersection]);

        sum1sq = sum([pow(set1[coffee_id], 2) for coffee_id in intersection]);
        sum2sq = sum([pow(set2[coffee_id], 2) for coffee_id in intersection]);

        sumProducts = sum([set1[coffee_id] * set2[coffee_id] for coffee_id in intersection])

        num = sumProducts - (sum1 * sum2) / n
        den = sqrt( sum1sq - pow(sum1, 2) / n ) * sqrt( sum2sq - pow(sum2, 2) / n)
        print num, den
        if den == 0: return 0
        return num / den

    # Takes two sets of objects with binary data and returns the cosine similarity
    # between them
    def cosine_similarity(self, set1, set2):
        sim = 0
        print set1, set2
        if len(set1) != 0 and len(set2) != 0:
            intersection = set(set1.keys()) & set(set2.keys())
            print intersection
            sim = len(intersection) / (sqrt(len(set1)) * sqrt(len(set2)))
        return sim

    # Implements a very basic user based collaborative filtering algorithm
    # Does so very inefficiently
    # Determines the top recommendations for the user specified by user_name
    def user_based_recommendations(self, user_name):
        # Iterate through every user except self
        totals = {}
        similaritySum = {}

        # Calculate your similarity to that user
        user_items = self.getUserRatings(user_name);
        for user in self.getUsers():
            if user != user_name:
                compare_items = self.getUserRatings(user)
                similarity = self.cosine_similarity(user_items, compare_items)

                if similarity > 0:
                    unrated_set = set(compare_items.keys()) - set(user_items.keys())
                    for item in unrated_set:
                        totals.setdefault(item, 0)
                        similaritySum.setdefault(item, 0)
                        totals[item] += compare_items[item] * similarity
                        similaritySum[item] += similarity

        rankings = [ (total / similaritySum[item], item) for item, total in totals.items() ]

        rankings.sort()
        rankings.reverse()
        return rankings
