import os
import logging
import markdown

log = logging.getLogger(__name__)


# List of trigger words and their responses
# [["TRIGGER WORD 1", "TRIGGER WORD 2", ...], "RESPONSE"]
# The trigger words are NOT case-sensitive!
trigger_list = [
  [["homeassistant", "Home Assistant", "Home-assistant"], "Check HomeAssistant"],
  [["wrong values"], "Improve ROI, ..."],
  [["lagging", "late transition", "transition", "early"], "Check parameter numberanalogtodigittransitionstart"],
  [["reflection"], "Improve LED, diffusor, ..."],
  [["LCD", "matrix"], "LCD/Matrix"],
  [["Rate too high"], "Set the https://jomjol.github.io/AI-on-the-edge-device-docs/FAQs/#rate-too-high-read"],
 # [[""], ""],
]


def process_discussion(actor, title, body):
    """Analyses the given title and body and creates a response based on teh found trigegr words"""
    log.info(f"Dear @{actor}")
    log.info(f"title: {title}")

    title = markdown.markdown(title)
    title = title.replace("p>", "h1>")

    body = body.replace("`", "")  # remove the code starts as it upsets bash
    body = body.replace("![", "[")  # Replace images with the links to the images
    log.info(f"body: {body}")

    body = markdown.markdown(body)

    trigger_word_responses =[]

    for entry in trigger_list:
        for word in entry[0]:
            if (word.lower() in title.lower()) or (word.lower() in body.lower()):
                trigger_word_responses.append([word, entry[1]])

    if len(trigger_word_responses) > 0:
        response = f"Hi @{actor}"
        response += """

I am the AIOTED-Bot 🤖

Have you already checked our [documentation](https://jomjol.github.io/AI-on-the-edge-device-docs)?
I analyzed your question and would like to help you on your issue.
Here are some useful links based on your input:

"""

        for finding in trigger_word_responses:
            response += f" -** {finding[0]}:** {finding[1]}\n"

        response += """
        
If this all does not help and you need support of an experienced user or developer to look into it (after you really studied the documentation), write a reply with the text `help-needed`.
Please be aware that we are a small team and run this project in our private, free time"""
    else:
        response = ""
    
    return response


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    actor = os.environ["GH_DISCUSSION_ACTOR"]
    title = os.environ["GH_DISCUSSION_TITLE"]
    body = os.environ["GH_DISCUSSION_BODY"]

    response = process_discussion(actor, title, body)

    log.info(f"response: {response}")

    # write to file
    with open("response.md", "w") as f:
        f.write(f"{response}")
