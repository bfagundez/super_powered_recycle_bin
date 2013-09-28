from flask import render_template, request
from sprb import sprb
from classes.signed_request import SignedRequest
import json
#import ipdb
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
		#ipdb.set_trace()
		recs.append(json.dumps(r))

	return json.dumps(recs)

@sprb.route('/canvas_testing')
def canvas_testing():
	# perform a login with credentials.
	# be able to test in a dev env.
	sf.login('force_presentation@brxprojects.com','Dumbl3d0r3!bHpxqOi7Di5i6cR0z45h8rECF','')
	return render_template('canvas_test.html')

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
