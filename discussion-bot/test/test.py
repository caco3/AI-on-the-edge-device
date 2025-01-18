import os
import logging
import json
import markdown
import tarfile

import sys
sys.path.append("..")
from response_generator import Response_Generator

log = logging.getLogger(__name__)

css = """
body {
    font-family: sans-serif;
    
    table {
        border-collapse: collapse;
    }
        
    tr {
      border-bottom: 1pt solid black;
    }

    td {
        padding: 5px;
        vertical-align: top;
        max-width: 1200px;
    }
    
    .vertical-separator {
        border-left: 1pt solid lightgray;
    }
}

"""

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

if os.path.exists("discussions.json"):
    os.remove("discussions.json")

file = tarfile.open('discussions.tar.gz')
file.extract('discussions.json', "./")
file.close()

with open("discussions.json", "r") as f:
    discussions = json.load(f)

    # open output file html
    output_file = open("result.html", "w")

    output_file.write("<html>")
    output_file.write("<head>\n")
    output_file.write("<style>\n")
    output_file.write(css)
    output_file.write("</style>\n")
    output_file.write("</head>\n")
    output_file.write("<body>\n")
    output_file.write("<h1>Discussions/Responses</h1>")
    output_file.write("<table>")
    output_file.write("<tr>")
    output_file.write("<th>Discussion (first comment only)</th>")
    output_file.write("<th class=vertical-separator>Response</th>")
    output_file.write("</tr>")

    rg = Response_Generator(os.path.dirname(__file__) + "/../" + "responses.md",
                            os.path.dirname(__file__) + "/../" + "response_intro.md",
                            os.path.dirname(__file__) + "/../" + "response_outro.md")

    for i in range(len(discussions) - 1, -1, -1):
        log.info(f"Processing discussion {len(discussions) - i}/{len(discussions)}...")
        actor = discussions[i]["user"]["login"]
        title = discussions[i]["title"]
        body = discussions[i]["body"]
        number = discussions[i]["number"]
        html_url = discussions[i]["html_url"]
        created_at= discussions[i]["created_at"].split("T")[0]

        #if number != 1496:
        #    continue

        #log.info(f"actor: {actor}, title: {title}, body: {body}")

        response = rg.process_discussion(actor, title, body)
        #log.info(f"response: {response}")

        title_html = f"{title} ([#{number}]({html_url}), {created_at})"
        title_html = markdown.markdown(title_html)
        body_html = body.replace("![", "[")  # Replace images by the link to the image
        body_html = body_html.replace("<img", "<a")  # Replace images by the link to the image
        body_html = markdown.markdown(body_html)
        response_html = markdown.markdown(response)

        response_html = f"<!-- {response_html} -->".replace("<ul>", "--><ul>").replace("</ul>", "</ul><!--")

        output_file.write(f"<tr><td><h3>{title_html}</h3>{body_html}</td><td class=vertical-separator>{response_html}</td></tr>")

        # break  # testing

    output_file.write("</table>")
    output_file.write("</body>")
    output_file.write("</html>")
    output_file.close()

    log.info("Done. Please open the result.html file in a webbrowser.")