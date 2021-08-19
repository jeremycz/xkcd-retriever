import argparse

from xkcd.retriever import Retriever


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--index", type=int, help="display a specific comic by index")
parser.add_argument(
    "-r",
    "--random",
    action="store_true",
    default=False,
    help="display a random comic (default: false)",
)
parser.add_argument(
    "-l",
    "--latest",
    action="store_true",
    default=True,
    help="display the latest comic (default true)",
)

args = parser.parse_args()

retriever = Retriever()
retriever.initialise()

if args.index is not None:
    retriever.get_comic(args.index)
elif args.random:
    retriever.get_random()
elif args.latest:
    retriever.get_latest()
