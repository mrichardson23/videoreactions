# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

import logging

class Video(Document):
	youTubeID = StringField()
	reactionTime = IntField()

class Reaction(Document):
	video = ReferenceField('Video')
	fileName = StringField()