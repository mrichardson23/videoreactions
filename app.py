# -*- coding: utf-8 -*-
import os, datetime
import re
from unidecode import unidecode


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

	# get Idea form from models.py
	idea_form = models.IdeaForm(request.form)
	
	# if form was submitted and it is valid...
	if request.method == "POST" and idea_form.validate():
	
		# get form data - create new idea
		idea = models.Idea()
		idea.creator = request.form.get('creator','anonymous')
		idea.title = request.form.get('title','no title')
		idea.slug = slugify(idea.title + " " + idea.creator)
		idea.idea = request.form.get('idea','')
		idea.categories = request.form.getlist('categories') # getlist will pull multiple items 'categories' into a list
		
		idea.save() # save it

		# redirect to the new idea page
		return redirect('/ideas/%s' % idea.slug)

	else:

		# for form management, checkboxes are weird (in wtforms)
		# prepare checklist items for form
		# you'll need to take the form checkboxes submitted
		# and idea_form.categories list needs to be populated.
		if request.method=="POST" and request.form.getlist('categories'):
			for c in request.form.getlist('categories'):
				idea_form.categories.append_entry(c)


		# render the template
		templateData = {
			'ideas' : models.Idea.objects(),
			'categories' : categories,
			'form' : idea_form
		}
		return render_template("main.html", **templateData)

# Display all ideas for a specific category
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



@app.route("/add", methods=['POST'])
def add():
	# if form was submitted and it is valid...
	if request.method == "POST":
	
		# get form data - create new idea
		video = models.Video()
		video.youTubeID = request.form.get('id','')
		video.reactionTime = request.form.get('time','')
		video.save() # save it

		# redirect to the new idea page
		return redirect('/v/%s' % request.form.get('id',''))

@app.route("/upload", methods=['POST', 'GET'])
def upload():
	if request.method == 'POST':
		ourData = request.stream.read()
		#filename = 'works.jpg'
		#conn = S3Connection('AKIAJ72GKBG7RUPSN2RA', 'tPMdmk8vCxq1PvqeSKideTPnTzVK2bN8TE4uDAZ4')
		#bucket = 'video_reactions'
		#k = Key(bucket)
		#k.key = 'foobar'
		return type(ourData)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404



# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	