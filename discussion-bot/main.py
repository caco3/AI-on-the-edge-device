import argparse
import logging

log = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    args = parser.parse_args()

    log.info(f"Dear @{args.actor}\n\n")
    log.info(f"title: {args.title}\n\n")
    log.info(f"body: {args.body}\n")

    # write to file
    with open("response.md", "w") as f:
        f.write(f"Dear @{args.actor}\n\n")
        f.write(f"title: {args.title}\n\n")
        f.write(f"body: {args.body}\n")