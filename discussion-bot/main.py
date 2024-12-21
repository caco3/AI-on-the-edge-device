import os
import logging

log = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    actor = os.environ["GH_DISCUSSION_ACTOR"]
    title = os.environ["GH_DISCUSSION_TITLE"]
    body = os.environ["GH_DISCUSSION_BODY"].replace("`", "")

    log.info(f"Dear @{actor}\n\n")
    log.info(f"title: {title}\n\n")
    log.info(f"body: {body}\n")

    # write to file
    with open("response.md", "w") as f:
        f.write(f"Dear @{actor}\n\n")
        f.write(f"title: {title}\n\n")
        f.write(f"body: {body}\n")
