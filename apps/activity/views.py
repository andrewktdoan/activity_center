from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt
from datetime import datetime, timedelta, time
from django.contrib.sessions.models import Session

def index(request):
	return render(request, 'activity/index.html')

def process(request):
	if request.method == 'POST':
		errors = User.objects.validator(request.POST)
		if errors:
			for error in errors:
				print errors
				messages.error(request, errors[error])
			return redirect('/')
		else:
			hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'],email = request.POST['email'], password = hashed_pw)
			request.session['id'] =  user.id
			return redirect('/success')
	return redirect('/')

def login(request):
	if request.method == 'POST':
		member = User.objects.login(request.POST)
		if 'user' in member:
			request.session['id'] = member['user'].id
			request.session['email'] = member['user'].email
			return redirect('/success')
		else:
			for error in member:
				messages.error(request, member[error])
			print messages
			return redirect('/')
	return redirect('/')

def success(request): #Routing to the Dashboard
	if not 'id' in request.session:
		return redirect('/')
	today = datetime.now().date()
	context = {
        "activities": Activity.objects.all().exclude(date__lte=today).order_by('date', 'time'),
        "user": User.objects.get(id=request.session['id'])
    }
	return render(request, 'activity/dashboard.html', context)


def create_activity(request):
	if not 'id' in request.session:
		return redirect('/')
	errors = Activity.objects.actvalidator(request.POST)
	if errors:
		for error in errors:
			print errors[error]
			messages.error(request, errors[error])
        	return redirect('/new')
        else:
        	user = User.objects.get(id = request.session['id'])
        	Activity.objects.create(

        title= request.POST['title'], 
        time= datetime.strptime(request.POST['time'],  "%H:%M").time(), 
        date= datetime.strptime(request.POST['date'], "%Y-%m-%d").date(), 
        duration_type= request.POST['duration_type'], 
        duration= request.POST['duration'], 
        description= request.POST['description'], 
        creator = User.objects.get(id = request.session['id'])

        )
    	return redirect('/success')

def activity(request, act_id):
	if not 'id' in request.session:
		return redirect('/')
	context={
		'activity': Activity.objects.get(id=act_id)
	}
	return render(request, 'activity/activity.html', context)

def new_activity(request):
	if not 'id' in request.session:
		return redirect('/')
	return render(request, 'activity/create_activity.html')

def delete_activity(request, act_id):
	if not 'id' in request.session:
		return redirect('/')
	Activity.objects.get(id=act_id).delete()
	return redirect('/success')

def join_activity(request, act_id):
	if not 'id' in request.session:
		return redirect('/')

	# if request.POST['date']== Activity.objects.get(id = act_id).datetime:
	# 	messages.error(request,'You are already have plans for this date/time')
	# 	return redirect('/success')
	me = User.objects.get(id=request.session['id'])
	Activity.objects.get(id=act_id).qty_participants.add(me)
	return redirect('/success')
    
def leave_activity(request, act_id):
	if not 'id' in request.session:
		return redirect('/')
	Activity.objects.get(id=act_id).qty_participants.remove(User.objects.get(id=request.session['id']))
	return redirect('/success')

def logout(request):
    Session.objects.all().delete()
    return redirect('/')



