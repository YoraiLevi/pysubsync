import argparse
from pysubsync import Subtitles


def main():
    parser = argparse.ArgumentParser(
        description='Syncronizes subtitles based on correctly synced subtitles')
    parser.add_argument('synced_subtitles')
    parser.add_argument('desynced_subtitles')
    parser.add_argument('output_name')
    parser.add_argument('-harshness', type=float, default=3)
    args = parser.parse_args()
    synced = Subtitles.load(args.synced_subtitles)
    desynced = Subtitles.load(args.desynced_subtitles)
    desynced.sync(synced, harshness=args.harshness)
    desynced.save(args.output_name)

if __name__ == "__main__":
    main()
