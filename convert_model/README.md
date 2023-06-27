# Convert Model from [`HuggingFace`](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) to [`GGML`](http://ggml.ai)

* Clone and build  `GGML` repo

```bash
git clone https://github.com/ggerganov/ggml
cd ggml
python3 -m pip install -r requirements.txt
mkdir build && cd build
cmake ..
make -j
```

* Download [`pythia-1b`](https://huggingface.co/EleutherAI/pythia-1b) model weights

```bash
# Make sure you have git-lfs installed (https://git-lfs.com)
git lfs install
git clone https://huggingface.co/EleutherAI/pythia-1b
```

* Convert model to `GGML` format

```bash
python3 ../examples/gpt-neox/convert-h5-to-ggml.py ./pythia-1b/ 1
```

* Quantize model to 5 or 4 bits

```bash
# Quantize to 4 bits
./bin/gpt-neox-quantize ./pythia-1b/ggml-model-f16.bin ./pythia-1b/ggml-model-q4_0.bin q4_0
```

The result is a 600 MB file `ggml-model-q4_0.bin` you can copy to [`mse_src/`](../mse_src/)
