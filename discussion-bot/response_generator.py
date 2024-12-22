import os
import logging

log = logging.getLogger(__name__)

class Data_Record_Parser():
    data_records = []

    def __init__(self, data_file):
        records_count = 0
        record_started = False
        with open(data_file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith(";"):  # Comment line
                    continue

                if line != "": # Line contains data
                    if not record_started:
                        record_started = True
                        self.data_records.append({"response": None, "trigger_patterns": []})
                        records_count += 1

                    if self.data_records[records_count - 1]["response"] == None:  # Record has no response yet -> Add line as response
                        self.data_records[records_count - 1]["response"] = line
                    else: # Record has a response -> Add line as trigger pattern
                        self.data_records[records_count - 1]["trigger_patterns"].append(line)
                else:  # Empty line -> end of record
                    record_started = False
                    continue

        log.info(f"Found {records_count} data records")

    def get_records(self):
        return self.data_records


class Response_Generator():
    def __init__(self, data_file):
        parser = Data_Record_Parser(data_file)
        self.data_records = parser.get_records()

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
            response = f"Hi @{actor}"
            response += """
    
I am the (experimental) AIOTED-Bot 🤖

Have you already checked our [documentation](https://jomjol.github.io/AI-on-the-edge-device-docs)?
I analyzed your question and would like to help you.
Here are some useful links based on your input:

"""

            for finding in responses:
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


    print(os.path.realpath(__file__) + "/" + "response_data.txt")
    rg = Response_Generator(os.path.dirname(__file__) + "/" + "response_data.txt")

    response = rg.process_discussion(actor, title, body)

    log.info("response:")
    log.info(f"{response}")
