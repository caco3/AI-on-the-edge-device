import os
import logging

from response_generator import Response_Generator

log = logging.getLogger(__name__)

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

actor = os.environ["GH_DISCUSSION_ACTOR"]
title = os.environ["GH_DISCUSSION_TITLE"]
body = os.environ["GH_DISCUSSION_BODY"]

rg = Response_Generator("response_data.txt")

response = rg.process_discussion(actor, title, body)

#log.info(f"response: {response}")

# write to file
with open("response.md", "w") as f:
    f.write(f"{response}")
