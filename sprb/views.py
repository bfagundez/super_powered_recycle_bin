from flask import render_template, request
from sprb import sprb
from classes.signed_request import SignedRequest
import json
import os
from sforce_custom.partner import SforcePartnerClient

# load WSDL declaration file
sf = SforcePartnerClient('sprb/partner.wsdl')

@sprb.route('/')
def index():
	return render_template('index.html')

@sprb.route('/get_bin_records/<object_name>')
def get_bin_records(object_name):
	q = sf.queryAll("select id,Name from Account where isDeleted = true")
	recs = []
	for r in q.records:
		recs.append(str(r))

	return str(recs)

@sprb.route('/canvas', methods=['POST',])
def canvas():
	sr_param = request.form['signed_request']
	secret = os.environ.get('CANVAS_SECRET')
	srHelper = SignedRequest(secret,sr_param)
	canvasRequestJSON = srHelper.verifyAndDecode()
	
	#load request data json to extract parameters
	request_data = json.loads(canvasRequestJSON)
	header = sf.generateHeader('SessionHeader')
	
	# oauth token (that will work as session id)
	token = request_data['client']['oauthToken']
	endpoint = request_data['client']['instanceUrl']+request_data['context']['links']['partnerUrl']
	
	# set sf soap toolkit headers
	header.sessionId = token
	sf.setSessionHeader(header)
	sf._sessionId = token
	sf._setEndpoint(endpoint)

	return render_template('canvas_post.html', canvasRequestJSON = canvasRequestJSON )

@sprb.route('/hello')
def hello():
	return "hello world"
