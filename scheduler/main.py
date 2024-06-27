from argparse import ArgumentParser

from tasks import daily_task


def arg_parser():
    parser = ArgumentParser()
    parser.add_argument("--now", help="run the job now", action="store_true")
    return parser.parse_args()


def main():
    args = arg_parser()
    if args.now:
        daily_task.delay()


if __name__ == "__main__":
    main()
