import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    args = parser.parse_args()

    print(f"Dear {args.actor}")
    print(f"title: {args.title}")
    print(f"body: {args.body}")
