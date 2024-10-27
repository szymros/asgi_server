# ASGI server

Minimal ASGI complient server. Currently only supports HTTP protocol

## Running

```python
poetry install
python -m asgi_server <file containing asgi app>:<asgi app variable name> <port>
```

## TODO

- error handling
- lifetime events maybe
- websockets maybe
