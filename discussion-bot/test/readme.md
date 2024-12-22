# Test of the discussion responder

The `discssions.json` file contains a list of discussion threads (first comment only).
The list got generated with the following cmd:
```bash
for i in {1..10}; do wget "https://api.github.com/repos/jomjol/AI-on-the-edge-device/discussions?per_page=100&page=$i" -O discussions_$i.json; done
```

Afterward I removed the first and last line of each file (remove the `[` and `]`) merged the files and wrap the new one again with `[` and `]`.

If you run the `test.py` script it will generate a HTML page which shows all discussions and the matching responses.
