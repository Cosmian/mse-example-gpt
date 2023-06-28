import argparse
import json
from typing import Optional

import requests
from termcolor import colored
from utils.cert import get_ssl_certificate


def send_query(url: str, query: str, cert_path: Optional[str] = None):
    """
    Sends a POST query.

    Args:
        url (str): The URL of the API.
        query (str): The query.
        cert_path (Path, optional): The path to the SSL certificate. Defaults to None.

    Returns:
        Response: The generated text from the API.
    """
    data = {"query": query}
    response = requests.post(
        f"{url}/generate",
        json=data,
        verify=cert_path,
    )

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code} {response.text}")

    return json.loads(response.text)


def main(url: str, query: str):
    """
    Query GPT models running on MSE.

    Args:
        url (str): The URL of the secure API.
        query (str): User query
    """
    if not url.startswith("http"):
        # If the URL does not have a scheme, assume HTTP and display a warning message.
        print(f"WARNING: no scheme found in {url}. Continuing with HTTP.")
        url = f"http://{url}"

    cert_path = get_ssl_certificate(url)

    print(query, end="", flush=True)
    res = send_query(url, query, cert_path=cert_path)
    print(colored(res["response"], "green"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MSE query example.")
    parser.add_argument("url", type=str, help="URL of the secure API")
    parser.add_argument("query", type=str, help="Input query")

    try:
        args = parser.parse_args()
        main(args.url, args.query)
    except SystemExit:
        parser.print_help()
        raise
