import os
from http import HTTPStatus
from pathlib import Path

from ctransformers import AutoModelForCausalLM
from flask import Flask, Response, jsonify, request

app = Flask(__name__)

CWD_PATH = Path(os.getenv("MODULE_PATH", "./mse_src")).resolve()
llm: AutoModelForCausalLM


@app.before_first_request
def init():
    global llm

    try:
        llm = AutoModelForCausalLM.from_pretrained(
            str(CWD_PATH / "ggml-model-q4_0.bin"), model_type="gpt-neox"
        )
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
    json_data = request.json
    query = json_data.get("query")
    if not query:
        return Response(status=HTTPStatus.BAD_REQUEST)

    res = llm(query, seed=123, threads=3, max_new_tokens=64)

    return jsonify({"response": res})
