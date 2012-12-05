# -*- coding: utf-8 -*-
import os, datetime
import re
from unidecode import unidecode
import string
import random


from flask import Flask, request, render_template, redirect, abort

# import all of mongoengine
from mongoengine import *

# import data models
import models

# for json needs
import json
from flask import jsonify

# for file uploads
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = False

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")

# hardcoded categories for the checkboxes on the form
categories = ['web','physical computing','software','video','music','installation','assistive technology','developing nations','business','social networks']

# --------- Routes ----------

# this is our main page
@app.route("/", methods=['GET','POST'])
def index():
	return render_template('welcome_new.html')

# this is our main page
@app.route("/camtest", methods=['GET','POST'])
def camtest():
	return render_template('camtest.html')

@app.route("/v/<vid_id>")
def vid_view(vid_id):
	try:
		video = models.Video.objects.get(youTubeID=vid_id)
		vid_id = video.youTubeID
		time = video.reactionTime
		# prepare data for template
		templateData = {
			'vid_id' : vid_id,
			'reaction_time': time
		}

		# render and return template
		return render_template('video_view.html', **templateData)

	except:
		vid_id = vid_id
		templateData = {
			'vid_id' : vid_id,
			'reaction_time': 0
		}

		# render and return template
		return render_template('video_new.html', **templateData)


# Display all ideas for a specific category
@app.route("/s/<share_id>")
def share_page(share_id):
	try:
		this_share = models.Share.objects.get(easy_id=share_id)
		vid_id = this_share.youTubeID
		time = this_share.reactionTime
		
		reactions = models.Reaction.objects(share=this_share)

		templateData = {
			'vid_id' : vid_id,
			'reaction_time': time,
			'share_id': share_id,
			'reactions' : reactions
		}
		# render and return template
		return render_template('video_view.html', **templateData)

	except:
		return render_template('404.html'), 404

# Display all ideas for a specific category
@app.route("/m/<share_id>")
def matt_share_page(share_id):
	try:
		this_share = models.Share.objects.get(easy_id=share_id)
		vid_id = this_share.youTubeID
		time = this_share.reactionTime
		
		reactions = models.Reaction.objects(share=this_share)

		templateData = {
			'vid_id' : vid_id,
			'reaction_time': time,
			'share_id': share_id,
			'reactions' : reactions
		}
		# render and return template
		return render_template('video_view_matt.html', **templateData)

	except:
		return render_template('404.html'), 404


@app.route("/t/<share_id>")
def share_page_test(share_id):
	try:
		this_share = models.Share.objects.get(easy_id=share_id)
		vid_id = this_share.youTubeID
		time = this_share.reactionTime
		
		reactions = models.Reaction.objects(share=this_share)

		templateData = {
			'vid_id' : vid_id,
			'reaction_time': time,
			'share_id': share_id,
			'reactions' : reactions
		}
		# render and return template
		return render_template('video_view_kim.html', **templateData)

	except:
		return render_template('404.html'), 404


@app.route("/add", methods=['POST'])
def add():
	# if form was submitted and it is valid...
	if request.method == "POST":
		# get form data - create new idea
		share = models.Share()
		share.youTubeID = request.form.get('id','')
		share.reactionTime = request.form.get('time','')
		share.easy_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(5))
		share.save() # save it

		# redirect to the new idea page
		return redirect('/s/%s' % share.easy_id)

@app.route("/ajaxadd", methods=['POST'])
def ajaxadd():
	# if form was submitted and it is valid...
	if request.method == "POST":
		# get form data - create new idea
		share = models.Share()
		share.youTubeID = request.form.get('id','')
		app.logger.debug("ID was: " + request.form.get('id',''))
		share.reactionTime = int(request.form.get('time',''))
		share.easy_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for x in range(5))
		share.save() # save it

		# redirect to the new idea page
		return (share.easy_id)


@app.route("/listing", methods=['GET'])
def get_listing():

	shares = models.Share.objects()

	templateData = {
		'shares' : shares
	}

	# render and return template
	return render_template('listing.html', **templateData)


@app.route("/addreaction", methods=['POST'])
def add_reaction():
	# if form was submitted and it is valid...
	if request.method == "POST":
		# get form data - create new idea
		reaction = models.Reaction()
		reaction.fileID = request.form.get('file','')
		reaction.share = models.Share.objects.get(easy_id=request.form.get('share_id',''))
		reaction.save() # save it
	return "OK"

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	