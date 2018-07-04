import nltk
import itertools
import re
import twitter
import secrets

nltk.download("wordnet")

SANITIZE = re.compile("[^A-Za-z0-9_]")

synsets = ["food.n.01", "food.n.02"]
possible_names = set()


for synset in synsets:
    synset = nltk.corpus.wordnet.synset(synset)

    for word in synset.closure(lambda s: s.hyponyms()):
        for synonym in word.lemmas():
            name = synonym.name().lower() + "_ass"

            possible_names.add(SANITIZE.sub("", name))
            possible_names.add(SANITIZE.sub("", name.replace("_", "")))
            possible_names.add(SANITIZE.sub("", name.replace("-", "_")))

api  = twitter.Api(**secrets.secrets, application_only_auth=True, sleep_on_rate_limit=True)

for i in range(0, len(possible_names), 100):
    users = list(itertools.islice(possible_names, i, i + 100))

    for user in api.UsersLookup(screen_name=users):
        print(user.name + " - https://twitter.com/" + user.screen_name)
