from flask import render_template, request
from sprb import sprb
from classes.signed_request import SignedRequest
import json
from sforce_custom.partner import SforcePartnerClient


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
	
	request_data = json.loads(canvasRequestJSON)

	#
	#print str(request_data)
	print "starting the sf login"
	sf = SforcePartnerClient('sforce_custom/partner.wsdl')

	header = sf.generateHeader('SessionHeader')
	print "generated header"+str(header)
	token = request_data['client']['oauthToken']
	print "token"+token
	endpoint = request_data['client']['instanceUrl']+request_data['context']['links']['partnerUrl']
	print "endpoint "+endpoint
	header.sessionId = token
	sf.setSessionHeader(header)
	sf._sessionId = token
	sf._setEndpoint(endpoint)

	q = sf.queryAll("select id from Account")

	print "and the query size is: "+str(q.size)

	return render_template('canvas_post.html', canvasRequestJSON = canvasRequestJSON )

@sprb.route('/hello')
def hello():
	return "hello world"
