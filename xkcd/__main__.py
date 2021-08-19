import argparse

from xkcd.retriever import Retriever


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--index", type=int)
parser.add_argument("-r", "--random", action="store_true", default=False)
parser.add_argument("-l", "--latest", action="store_true", default=True)

args = parser.parse_args()

retriever = Retriever()
retriever.initialise()

if args.index is not None:
    retriever.get_comic(args.index)
elif args.random:
    retriever.get_random()
elif args.latest:
    retriever.get_latest()
