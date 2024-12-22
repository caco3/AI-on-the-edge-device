import os
import logging

log = logging.getLogger(__name__)

class Response_generator():
    def __init__(self):
        pass

    # List of trigger words and their responses
    # [["TRIGGER WORD 1", "TRIGGER WORD 2", ...], "RESPONSE"]
    # The trigger words are NOT case-sensitive!
    trigger_list = [
        [["homeassistant", "Home Assistant", "Home-assistant"], "Check HomeAssistant"],
        [["wrong values"], "Improve ROI, ..."],
        [["lagging", "late transition", "transition", "early"], "Check parameter numberanalogtodigittransitionstart"],
        [["reflection"], "Improve LED, diffusor, see xxx"],
        [["LCD", "matrix"], "See LCD/Matrix xxx"],
        [["Rate too high"], "See the [FAQ](https://jomjol.github.io/AI-on-the-edge-device-docs/FAQs/#rate-too-high-read)"],
        # [[""], ""],
    ]

    def process_discussion(self, actor, title, body):
        """Analyses the given title and body and creates a response based on the found trigger words
        Input and output have to be in the markdown format"""
        trigger_word_responses = []

        for entry in self.trigger_list:
            for word in entry[0]:
                if (word.lower() in title.lower()) or (word.lower() in body.lower()):
                    trigger_word_responses.append([word, entry[1]])

        if len(trigger_word_responses) > 0:
            response = f"Hi @{actor}"
            response += """
    
I am the (experimental) AIOTED-Bot 🤖

Have you already checked our [documentation](https://jomjol.github.io/AI-on-the-edge-device-docs)?
I analyzed your question and would like to help you.
Here are some useful links based on your input:

"""

            for finding in trigger_word_responses:
                response += f" - **{finding[0]}:** {finding[1]}\n"

            response += """
If this all does not help and you need support of an experienced user or developer to look into it (after you really studied the documentation), you can write a reply with the text `help-needed`.
Please be aware that we are a small team and run this project in our private, free time, so our time to give support is really limitted!"""
        else:
            response = ""

        return response


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    args = parser.parse_args()

    actor = args.actor
    title = args.title
    body = args.body

    rg = Response_generator()

    response = rg.process_discussion(actor, title, body)

    log.info("response:")
    log.info(f"{response}")
