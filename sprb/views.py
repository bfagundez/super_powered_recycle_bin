from flask import render_template
from sprb import sprb

@sprb.route('/')
def index():
	return render_template('index.html')
