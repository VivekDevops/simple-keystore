from flask import Flask, json, request

app = Flask(__name__)

keystore = {"key1": "value1", "key2": "value2", "key3": "value3", "abc-1": "abc-1", "abc-2": "abc-2", "xyz-1": "xyz-1", "xyz-2": "xyz-2"}
@app.route("/")
def index():
    return "Simple Key Value Store!"

@app.route("/get/<key>")
def get(key):
    if key in keystore:
        return json.dumps(keystore[key])
    else:
        return "Supplied Key does not exist in the store!"
@app.route("/getall")
def getall():
    return keystore

@app.route("/set", methods=["POST"])
def set():
    keystore.update(request.json)
    # keystore[request.json['key']] = request.json['value']
    return keystore
@app.route("/search")
def search(): 
    search_key = request.args.get('suffix', None)
    if search_key == None:
        search_key = request.args.get('prefix', None)
        if search_key == None:
            return "Only suffix and prefix functionality is implemented for search endpoint"
        else:
            res = [val for key, val in keystore.items() if key.startswith(search_key)]
            return json.dumps(res)
    else:
        res = [val for key, val in keystore.items() if key.endswith(search_key)]
        return json.dumps(res)
    # return [value for key, value in keystore.keys() if search_key.lower() in key.lower()]

@app.route("/del/<key>", methods=["DELETE"])
def delete(key):
    if key in keystore:
        del keystore[key]
        return f"{key} deleted successfully!!"
    else:
        return f"Key: {key} not found in the store"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')