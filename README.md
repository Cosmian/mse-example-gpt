# Deploy Large Language Models on MSE

Example of a simple MSE application to perform inference on LLM securely.

## Convert a model from HuggingFace

See [convert_model](./convert_model/) for instructions.

One can also use a custom fine-tuned model converted to `GGML` format.

## Deploy

* Test locally

```bash
mse test
```

```bash
curl http://0.0.0.0:5000/health
```

```bash
curl -X POST http://localhost:5000/generate \
     -H 'Content-Type: application/json' \
     -d '{"query":"User data protection is important for AI applications since"}'
```

* Deploy on MSE

```bash
mse deploy
```

```bash
curl https://$APP_DOMAIN_NAME/health --cacert cert.pem
```

```bash
curl https://$APP_DOMAIN_NAME/generate --cacert cert.pem
     -H 'Content-Type: application/json' \
     -d '{"query":"User data protection is important for AI applications since"}'
```
