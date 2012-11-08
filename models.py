# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime

import logging

class Share(Document):
	easy_id = StringField()
	youTubeID = StringField()
	reactionTime = IntField()

class Reaction(Document):
	share = ReferenceField('Share')
	fileID = StringField()