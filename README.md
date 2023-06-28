# Deploy Large Language Models on MSE

Example of a simple [MSE application](https://docs.cosmian.com/microservice_encryption/overview/) to perform __confidential__ inference on LLM.

## Convert a model from HuggingFace

See [convert_model](./convert_model/) for instructions.

One can also use a custom fine-tuned model converted to `GGML` format.

## Deploy

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

## Clients

More ways to interact with the MSE app are shown in [clients_example](./clients_example/)
