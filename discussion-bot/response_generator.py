import os
import logging

log = logging.getLogger(__name__)

class Data_Record_Parser():
    data_records = []

    def __init__(self, response_file):
        self.parse_responses(response_file)

    def parse_responses(self, response_file):
        with open(response_file, "r") as f:
            for line in f:
                line = line.strip()
                if line == "":  # Empty line
                    continue

                if line.startswith("#"):  # Title line -> response start
                    if len(self.data_records) > 1:  # This is not the first response
                        # Make sure the previous response record has at least one trigger pattern
                        if len(self.data_records[-2]["trigger_patterns"]) == 0:  # Number of trigger patterns of the 2nd last record
                            raise Exception("The previous response record has no trigger patterns!")

                    self.data_records.append({"title": line.replace("# ", ""), "response": None, "trigger_patterns": []})

                elif line.startswith("-"):  # Trigger pattern line
                    if self.data_records[-1]["response"] == None:  # Record has no response yet
                        raise Exception("The response record has no response line!")
                    self.data_records[-1]["trigger_patterns"].append(line.replace("- ", ""))  # Add to trigger patterns

                else:  # Response line
                    self.data_records[-1]["response"] = line  # Add as response line

        log.info(f"Found {len(self.data_records)} data records")
        # import pprint
        # pprint.pprint(self.data_records, width=300)


    def get_records(self):
        return self.data_records


class Response_Generator():
    def __init__(self, response_file, intro_file, outro_file):
        parser = Data_Record_Parser(response_file)
        self.data_records = parser.get_records()
        self.intro = open(intro_file, "r").read()
        self.outro = open(outro_file, "r").read()

    def process_discussion(self, actor, title, body):
        """Analyses the given title and body and creates a response based on the found trigger words
        Input and output have to be in the markdown format"""
        title = title.lower()
        body = body.lower()

        responses = []

        for data_record in self.data_records:
            for trigger_pattern in data_record["trigger_patterns"]:
                if (trigger_pattern.lower() in title) or (trigger_pattern.lower() in body):
                    responses.append([trigger_pattern, data_record["response"]])
                    break

        if len(responses) > 0:  # At least one trigger pattern matched
            response = self.intro + "\n"
            response = response.replace("{actor}", actor)

            for finding in responses:
                response += f" - **{finding[0]}:** {finding[1]}\n"

            response += "\n" +self.outro
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

    rg = Response_Generator(os.path.dirname(__file__) + "/" + "responses.md",
                            os.path.dirname(__file__) + "/" + "response_intro.md",
                            os.path.dirname(__file__) + "/" + "response_outro.md")

    response = rg.process_discussion(actor, title, body)

    log.info(f"response:\n{response}")
