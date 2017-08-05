from flask import Flask
from flask import request


app = Flask(__name__)

@app.route('/')
def index(name=""):
    name = str(request.args.get('name', name))
    if name not in set_done:
        size = Counter.get_size(start_path = name)
        set_done.add(name)
        done[name] = size
    else:
        size = done[name]
    return str(size)

if __name__ == "__main__":
    global done
    done = {}
    global set_done
    set_done = set()
    app.run(debug=True)

