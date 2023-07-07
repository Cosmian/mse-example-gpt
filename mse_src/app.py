import os
import threading
from base64 import b64decode
from http import HTTPStatus
from json import dumps
from pathlib import Path

from ctransformers import AutoModelForCausalLM
from flask import Flask, Response, jsonify, request

app = Flask(__name__)

# The model is stored in the current working directory (./mse_src)
# More information: https://docs.staging.cosmian.com/microservice_encryption_home/develop/#the-paths
CWD_PATH = Path(os.getenv("MODULE_PATH")).resolve()
# Model parameters
MAX_RESPONSE_SIZE = 64

llm: AutoModelForCausalLM

# Concurrent use of the model is not supported
model_lock = threading.Lock()


@app.before_first_request
def init():
    """
    Function to initialize the model before handling any requests.
    Here the model is loaded from disk but it could be downloaded from a secure source.
    """
    global llm
    model_path = str(CWD_PATH / "ggml-model-q4_0.bin")
    try:
        llm = AutoModelForCausalLM.from_pretrained(model_path, model_type="gpt-neox")
    except ValueError as e:
        print(f"Model initialization error: {e}")


# -----------------#
#   Flask routes   #
# -----------------#
@app.get("/health")
def health_check():
    return Response(status=HTTPStatus.OK)


@app.route("/generate", methods=["POST"])
def generate():
    """Route for generating a response based on a query."""
    global model_lock

    query = request.json.get("query")
    if not query:
        return Response(status=HTTPStatus.BAD_REQUEST)

    with model_lock:  # Acquire model lock
        # Generate a response using the model
        res = llm(query, seed=123, threads=3, max_new_tokens=MAX_RESPONSE_SIZE)

    return jsonify({"response": res})


@app.route("/generate")
def chat():
    """
    Route for generating a stream response based on a prompt
    containing a query and chat history.
    """
    b64_prompt = request.args.get("prompt")
    if not b64_prompt:
        return Response(status=HTTPStatus.BAD_REQUEST)

    # Truncate context to leave space for answer
    prompt = b64decode(b64_prompt).decode("utf-8")
    max_context_size = llm.context_length - MAX_RESPONSE_SIZE
    context_tokens = llm.tokenize(prompt)[-max_context_size:]

    def stream_response():
        global model_lock
        msg_id = 0

        with model_lock:  # Acquire model lock
            # Stream model tokens as they are being generated
            for token in llm.generate(context_tokens, seed=123, threads=3):
                msg_id += 1
                msg_str = dumps(llm.detokenize(token))

                yield f"id: {msg_id}\nevent: data\ndata: {msg_str}\n\n"

                if msg_id == MAX_RESPONSE_SIZE:
                    break

        # End stream
        yield f"id: {msg_id + 1}\nevent: end\ndata: {{}}\n\n"

    # Create SSE response
    return Response(stream_response(), mimetype="text/event-stream")
