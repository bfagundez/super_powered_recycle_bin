from flask import render_template, request
from sprb import sprb
from classes.signed_request import SignedRequest
import json

@sprb.route('/')
def index():
	return render_template('index.html')

@sprb.route('/canvas', methods=['POST',])
def canvas():
	print 'received call'

	sr_param = request.form['signed_request']
	print 'got param'+sr_param

	secret = '1576956863759220964'
	print 'calling helper'
	srHelper = SignedRequest(secret,sr_param)
	canvasRequestJSON = srHelper.verifyAndDecode()
	return render_template('canvas_post.html', canvasRequestJSON = json.dumps(canvasRequestJSON) )

@sprb.route('/hello')
def hello():
	return "hello world"
