from urllib import request


def fetch(path: str) -> None:
    url = f"http://127.0.0.1:9000{path}"
    print(f"\n=== GET {url} ===")
    try:
        with request.urlopen(url) as resp:
            body = resp.read().decode("utf-8")
            print("Status:", resp.status)
            print("Body:", body)
    except Exception as e:
        print("Request failed:", e)


def main() -> None:
    fetch("/metrics/overall")
    fetch("/metrics/by_strategy")
    fetch("/metrics/by_account")


if __name__ == "__main__":
    main()
