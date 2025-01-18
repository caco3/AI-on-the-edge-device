# Discussion Bot
The discussion bot can be used to create auto-responses on discussions.
The `responses.md` file is used a sa database and contains responses and trigger words.
When `response_generator.py` gets fed with a text, it parses the text, finds matching trigger words in the database and creates a list of suggestions.
The suggestions, wrapped between the content of `response_intro.md` and `response_outro.md`, then get put together to a response.

## Usage
To parse a discussion and generate a response, call it with
```bash
python response_generator.py --actor <ACTOR> --title <TITLE> --body <BODY>
```

Example:
```bash
python response_generator.py --actor "CaCO3" --title "Test" --body "Hi all. I have always wrong value and reflections. Also home assistant does not get any data."
```

## Data Format
It is important to make sure that the `responses.md` file has the right format!
Altrough it is a markdown file and can be rendered by a markdown viewer, it actually is parsed by the script.
Thus the format must be as following:
- A response starts with a title line and must have a leading `#` followed by a whitespace.
- The title can be empty. It also can be used to note some comments.
- The title line is followed by a one-line response. All markdown keywords are allowed, but it must stay on one line.
- Then one or more trigger words get listed as a list. Each line has one trigger word ar phrase.
- It might also be useful to add typos as trigger patterns, eg. `asistant`.
- It is suggested to separate the responses with empty lines for easier visual separation, although this is optional.

Example:
```
# Wrong Transitions
Check parameter numberanalogtodigittransitionstart
- lagging
- late transition
- early transition
```


## Testing
See [test/readme.md](test/readme.md)
