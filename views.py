from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm 
from .models import *
from django.core.files.storage import FileSystemStorage
# Create your views here.
def mainhome(request):
	return render(request, 'authenticate/mainhome.html')

def deletecomment(request):
	if request.method == 'POST':
		id = request.POST['id']
		x = Comments.objects.filter(id=id)
		x.delete()
		return redirect('gallery')
	else:
		return redirect('gallery')

def gallery(request):
	if request.method == 'POST':
		comment = request.POST['comment']
		image = request.POST['image']
		image = Gallery.objects.get(id=image)
		comments = Comments(image=image,user=request.user,comment=comment)
		comments.save()
		galleryimages = Gallery.objects.all()
		comments = Comments.objects.all()
		return render(request, 'authenticate/gallery.html',{'galleryimages':galleryimages,'comments':comments})
	else:	
		galleryimages = Gallery.objects.all()
		comments = Comments.objects.all()
		return render(request, 'authenticate/gallery.html',{'galleryimages':galleryimages,'comments':comments})
def home(request): 
	# try:
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		pincode = request.POST['pincode']
		try:
			image = request.FILES['image']
			fs = FileSystemStorage()
			filename = fs.save(image.name, image)
			uploaded_file_url = fs.url(filename)
		except:
			image = "--"	
		url = ""	
		url   = request.POST['url']
		if len(url)==0:
			url = "--------"
		address = request.POST['Address']
		tool = int(request.POST['tool'])
		image_data = Images(artistimage="---",name=name,user=request.user,email=email,pincode=pincode,image=image,url = url,address= address,tool=Drawingtool.objects.get(id=tool),approvedstatus='Pending',orderstatus="Pending",amount='will be updated.',paymentstatus='Not payed')
		image_data.save()
		msg  = 'Your request has been recorded.'
		gallery = Gallery.objects.all()
		tool = Drawingtool.objects.all()			
		return render(request, 'authenticate/home.html', {"msg":msg,'gallery':gallery,'tool':tool})
	else:
		msg=""
		gallery = Gallery.objects.all()
		events = Events.objects.all()
		return render(request, 'authenticate/home.html', {"msg":msg,'gallery':gallery,'events':events})
	# except:
		# return redirect('login')				
def allorders(request):
	datas = Liveupdates.objects.all().order_by('-datetime')
	return render(request, 'authenticate/allorders.html', {'datas':datas})

def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			return redirect('gallery') #routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('login')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'authenticate/register.html', context)

def edit_profile(request):
	try:
		if request.method =='POST':
			form = EditProfileForm(request.POST, instance= request.user)
			if form.is_valid():
				form.save()
				messages.success(request, ('You have edited your profile'))
				return redirect('home')
		else: 		#passes in user information 
			form = EditProfileForm(instance= request.user) 

		context = {'form': form}
		return render(request, 'authenticate/edit_profile.html', context)
	#return render(request, 'authenticate/edit_profile.html',{})
	except:
		return redirect('login')


def change_password(request):
	try:
		if request.method =='POST':
			form = PasswordChangeForm(data=request.POST, user= request.user)
			if form.is_valid():
				form.save()
				update_session_auth_hash(request, form.user)
				messages.success(request, ('You have edited your password'))
				return redirect('home')
		else: 		#passes in user information 
			form = PasswordChangeForm(user= request.user) 

		context = {'form': form}
		return render(request, 'authenticate/change_password.html', context)
	except:
		return redirect('login')
			
def message_artist(request):
	try:
		if request.method == 'POST':
			message = request.POST['message']
			data = Reachme(user= request.user,message=message)
			data.save()
			msg = "Admin Informed"
			reachme = Reachme.objects.filter(user=request.user)
			return render(request, 'authenticate/message_artist.html', {"msg":msg,'reachme':reachme})
		else:	
			msg = ""
			reachme = Reachme.objects.filter(user=request.user)
			return render(request, 'authenticate/message_artist.html', {"msg":msg,'reachme':reachme})	
	except:
			return redirect('login')


def temp(request):
	return render(request, 'authenticate/temp.html', {})	
def contact(request):
	con = Admincontact.objects.all()
	return render(request, 'authenticate/contact.html', {'con':con})	
def cordinater(request):
	if request.method == 'POST':
		status = request.POST['status']
		event = request.POST['event']
		event = Events.objects.get(id=int(event))
		Eventcor = Eventcordinaters.objects.get(user=request.user,event=event)
		Eventcor.accept = status
		Eventcor.save()
		datas =  Eventcordinaters.objects.filter(user=request.user)
		return render(request, 'authenticate/cordinater.html', {'datas':datas})
	else:
		datas =  Eventcordinaters.objects.filter(user=request.user)
		return render(request, 'authenticate/cordinater.html', {'datas':datas})
def calender(request):
	return render(request, 'authenticate/calender.html', {})	