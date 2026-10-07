import csv


def save_to_csv(parsed) -> None:
    with open("data/results.csv", "w", newline="") as csvfile:
        fieldnames = ["created_at", "ping", "download", "upload"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed)
