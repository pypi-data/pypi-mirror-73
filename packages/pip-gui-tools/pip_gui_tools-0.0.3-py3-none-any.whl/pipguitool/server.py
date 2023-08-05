
import flask
import json

from pipguitool.PIP import PIP

from flask import request, abort, render_template

import os


p = PIP()
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/list', methods=['GET'])
def list():
    return json.dumps(p.list())

@app.route('/install', methods=['POST'])
def install():

	if not request.json or not 'packages' in request.json or not hasattr(request.json['packages'], "append"):
		abort(400)
	
	return json.dumps(p.install(request.json['packages'])), 201

@app.route('/remove', methods=['POST'])
def remove():

	if not request.json or not 'packages' in request.json or not hasattr(request.json['packages'], "append"):
		abort(400)
	
	return str(p.remove(request.json['packages'])), 201


@app.route('/', methods=['GET'])
def index():

	return render_template('index.html', packages=p.list())


def main():

	port=os.getenv('PORT', 4040)

	app.run(host="0.0.0.0", port=port, threaded=True)

if __name__ == '__main__':
    main()
