# Deploy Large Language Models on MSE

Example of a simple [MSE application](https://docs.cosmian.com/microservice_encryption/overview/) to perform __confidential__ inference on LLM.

The MSE app is composed of the following files:

```bash
├── mse_src                   # Code folder to encrypt and deploy in the enclave
│   ├── app.py                # Flask application
│   └── requirements.txt      # Python packages to install during deployment
└── mse.toml                  # MSE config file
```

The example `mse.toml` is using the free hardware provided by Cosmian.
More information about config file [here](https://docs.cosmian.com/microservice_encryption/configuration/).

__Here are the steps to follow to deploy your own confidential AI app!__

## 1 - Convert a model from HuggingFace

See [convert_model](./convert_model/) for instructions.

One can also use a custom fine-tuned model converted to `GGML` format.

Finally, you should copy the resulting model file to `./mse_src`:

```bash
mse_src/
├── app.py
├── ggml-model-q4_0.bin
└── requirements.txt
```

## 2 - Deploy

* Install [`mse-cli`](https://docs.cosmian.com/microservice_encryption/getting_started/) on your computer.

* Test locally

```bash
mse test
```

* Simple text generation test

```bash
curl -X POST http://localhost:5000/generate \
     -H 'Content-Type: application/json' \
     -d '{"query":"User data protection is important for AI applications since"}'
```

* Deploy on MSE

```bash
$ mse deploy
...
Deploying your app 'demo-mse-gpt' with 4096M memory and 3.00 CPU cores...
...
💡 You can now test your application: 

     curl https://$APP_DOMAIN_NAME/health --cacert $CERT_PATH
```

Keep the `url` and `certificate path` to perform requests to the MSE app.

* Simple text generation test

```bash
curl https://$APP_DOMAIN_NAME/generate --cacert $CERT_PATH
     -H 'Content-Type: application/json' \
     -d '{"query":"User data protection is important for AI applications since"}'
```

## 3 - Interact with your application

More ways to interact with the MSE app are shown in [clients_example](./clients_example/)
