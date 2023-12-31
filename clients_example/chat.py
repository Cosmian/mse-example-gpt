import argparse
import ast
import signal
from base64 import b64encode
from typing import Optional

import requests
import sseclient
from termcolor import colored
from utils.cert import get_ssl_certificate


def format_prompt(query: str, history: str):
    """Formats the user prompt for Llama models."""
    if len(history) == 0:
        return f"[INST] <<SYS>>\nYou are a helpful assistant.\n<</SYS>>\n\n{query} [/INST] "
    else:
        return f"[INST] {query} [/INST] "


def b64_encode_str(input: str, encoding="utf-8") -> str:
    """Base64 encodes the input string."""
    return b64encode(input.encode(encoding)).decode(encoding)


def signal_handler(signal, frame):
    print("Exiting...")
    raise SystemExit


def send_query(url: str, prompt: str, cert_path: Optional[str] = None):
    """
    Sends a GET query in stream mode.

    Args:
        url (str): The URL of the API.
        prompt (str): The query prompt.
        cert_path (Path, optional): The path to the SSL certificate. Defaults to None.

    Returns:
        Response: The response stream from the API.
    """
    data = {"prompt": prompt}
    response = requests.get(
        f"{url}/generate",
        params=data,
        stream=True,
        verify=cert_path,
    )

    if response.status_code != 200:
        raise Exception(f"Bad response: {response.status_code} {response.text}")

    return response


def main(url: str, use_prompt: bool = False):
    """
    Chat with GPT models running on MSE.

    Args:
        url (str): The URL of the secure API.
    """
    if not url.startswith("http"):
        # If the URL does not have a scheme, assume HTTP and display a warning message.
        print(f"WARNING: no scheme found in {url}. Continuing with HTTP.")
        url = f"http://{url}"

    cert_path = get_ssl_certificate(url)

    signal.signal(signal.SIGINT, signal_handler)
    history = ""
    try:
        while True:
            # Read user query
            user_query = ""
            while not user_query:
                user_query = input(colored("User> ", "blue"))

            # Apply custom format for OpenAssistant models
            if use_prompt:
                user_query = format_prompt(user_query, history)

            # Append the user query to the history
            history += user_query

            # Send request to the MSE application
            stream_response = send_query(url, b64_encode_str(history), cert_path)
            client = sseclient.SSEClient(stream_response)

            print(colored("Assistant> ", "green"), end="", flush=True)

            # Listen to the API response stream until a end event is reach
            for event in client.events():
                if event.event == "end":
                    break
                string_response = str(ast.literal_eval(event.data))
                # Print the generated text and it to the history
                print(string_response, end="", flush=True)
                history += string_response

            print("")
    except SystemExit:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MSE chat example.")
    parser.add_argument("url", type=str, help="URL of the secure API")
    parser.add_argument(
        "--prompt",
        action="store_true",
        help="Use Llama prompt formatting",
    )

    try:
        args = parser.parse_args()
        main(args.url, args.prompt)
    except SystemExit:
        parser.print_help()
        raise
