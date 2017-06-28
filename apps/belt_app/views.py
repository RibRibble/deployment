from django.shortcuts import render, redirect
from models import User
from django.contrib import messages
import bcrypt


def index(request):
	# check = User.objects.get(email="pass@word.com")
	# print check
	return render(request, "belt_app/index.html")

def register(request):
	print ("**FORM DATA**", request.POST)
	is_validated = User.objects.validate(request.POST)

	if is_validated == True:
		user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()))
		print ("************************************************************",user)
		request.session['username'] = request.POST['username']
		request.session['user_id'] = user.id
		messages.success(request, "Congrats! You successfully registered.")
		return redirect('/success')
	else:
		print is_validated
		errors = is_validated[1]
		print ("^^ERRORS^^", errors)
		for error in errors:
			messages.error(request, error)
		return redirect('/')

def login(request):
	print request.POST
	result= User.objects.login(request.POST)
	if result[0] == False:
		messages.error(request, result[1])
		return redirect('/')
	else:
		request.session['username']=result[2]
		request.session['user_id'] = result[3]
		messages.success(request, result[1])
		return redirect('/success')


	return redirect('/')

def success(request):
	
	return render(request, "belt_app/success.html")

def logout(request):
	request.session.clear()

	messages.success(request, "You loged out.  Enjoy your day!")

	return redirect('/')
	




