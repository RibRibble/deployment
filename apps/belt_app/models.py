from __future__ import unicode_literals

from django.db import models

from django.contrib import messages

import re, bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
	def validate (self, postData):
		print ("**postData from views.py***", postData)
		errors = []
		if len(postData['name']) < 1:
			errors.append("First name must be at least 1 character, please.")
		
		if len(postData['username']) < 1:
			errors.append("Username must be at least 1 character, please.")
		elif User.objects.filter( username = postData['username']).exists():
			errors.append("Username is taken, please try again, sorry :(")
		
		# if len(postData['email']) < 1:
		# 	errors.append("Email can not be blank, please.")
		# elif not EMAIL_REGEX.match (postData['email']):
		# 	errors.append("Email must be a valid email address, please.")
		# elif User.objects.filter( email = postData['email']).exists():
		# 	errors.append("Email address is already been added to the database.  Please try another.")
		
		if len(postData['password']) < 8:			
			errors.append("Password must have more than 8 characters, please.")
		
		if postData['confirm_password'] != postData['password']:			
			errors.append("Passwords must match, please.")
		
		# if len(postData['date_of_birth']) < 1:
		# 	errors.append("Date of Birth must not be blank, please.")
		print errors
		if len(errors) == 0:
			return True
		else:
			return(False, errors)

	def login(self, postData):
		print "***************"
		print postData
		try:
			logPostData = User.objects.get(username=postData['username'])
			print logPostData.username
			print logPostData.password
		except:
			return (False, "Please try again, your password or username is not valid ")
		if logPostData.password == bcrypt.hashpw(postData['password'].encode(), logPostData.password.encode()):
			return (True, "Congrats! You successfully logged in.", logPostData.name, logPostData.id)
		else:
			return (False, "Please try again, your password or username is not valid ")




class User(models.Model):
	name= models.CharField(max_length=255)
	username= models.CharField(max_length=255)
	# email= models.EmailField(max_length=255)

	password= models.CharField(max_length=255)
	# date_of_birth= models.DateTimeField(auto_now_add=True)
	created_at= models.DateTimeField(auto_now_add=True)
	updated_at= models.DateTimeField(auto_now=True)
	objects= UserManager()

# class trip_plans(models.model):
	


		

