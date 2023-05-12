import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of todo's. Does not persist if Python session is restarted.
_COINS = {}

# CRUD Endpoints for Shitcoins
@app.post("/ethereum/shitcoins/<string:username>")
async def add_coin(username):
    request = await quart.request.get_json(force=True)
    if username not in _COINS:
        _COINS[username] = []
    _COINS[username].append(request["shitcoin"])
    return quart.Response(response='OK', status=200)

@app.get("/ethereum/shitcoins/<string:username>")
async def get_coins(username):
    return quart.Response(response=json.dumps(_COINS.get(username, [])), status=200)

@app.delete("/ethereum/shitcoins/<string:username>")
async def delete_coin(username):
    request = await quart.request.get_json(force=True)
    if username not in _COINS:
        return quart.Response(response='User not found', status=404)
    if request["shitcoin"] not in _COINS[username]:
        return quart.Response(response='Coin not found', status=404)
    _COINS[username].remove(request["shitcoin"])
    return quart.Response(response='OK', status=200)

# Get coin price
# @app.get("/ethereum/price/<string:coin>")
# async def get_price(coin):
#     url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
#     async with quart.ClientSession() as session:
#         async with session.get(url) as response:
#             data = await response.json()
#             return quart.Response(response=json.dumps(data), status=200)

# Required Endpoints
@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
