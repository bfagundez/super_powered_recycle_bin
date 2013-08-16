from flask import render_template, request
from sprb import sprb
from classes.signed_request import SignedRequest

@sprb.route('/')
def index():
	return render_template('index.html')

@sprb.route('/canvas', methods=['POST',])
def canvas():
	sr_param = request.args.get('signed_request')
	secret = '1576956863759220964'
	srHelper = SignedRequest(secret,sr_param)
	canvasRequestJSON = srHelper.verifyAndDecode()
	return render_template('canvas_post.html', canvasRequestJSON = canvasRequestJSON )

@sprb.route('/hello')
def hello():
	return "hello world"
