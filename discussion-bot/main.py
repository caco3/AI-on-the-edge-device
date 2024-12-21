import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    args = parser.parse_args()

    # write to file
    with open("response.md", "w") as f:
        f.write(f"Dear @{args.actor}\n")
        f.write(f"title: {args.title}\n")
        f.write(f"body: {args.body}\n")