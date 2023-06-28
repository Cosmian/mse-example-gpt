# Clients to interact with LLM deployed on MSE

## Install dependencies

```bash
pip install -r requirements.txt
```

## Simple query

* Query a locally running app

```bash
python query.py http://localhost:5000 "Deep learning is"
```

* Query the app deployed on MSE

```bash
python query.py https://$APP_DOMAIN_NAME "Deep learning is"
```

## Chat client

* Connect to a locally running app

```bash
python chat.py http://localhost:5000
```

* Connect to the app deployed on MSE

```bash
python chat.py https://$APP_DOMAIN_NAME
```
