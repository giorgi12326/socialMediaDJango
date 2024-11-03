from django.shortcuts import render,redirect
from .models import Room,Topic,Message,Profile
from django.db.models import Q
from .forms import RoomForm,ProfileForm,UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm



rooms = [
    {'id': 1, 'name': 'lets learn python!'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Frontend Developers'},
    {'id': 4, 'name': 'DZUDZU Developers'},
    {'id': 5, 'name': '(•)(•)'}
]
rooms = Room.objects.all()
topics = Topic.objects.all()

def registerPage(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        prof = Profile()
    
    
        if form.is_valid():
            user = form.save()
            prof.user = user
            prof.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"incorrect fields!")
    page = 'register'
    context = {'form':form,'page':page} 
    return render(request,'login_register.html',context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  
        user = authenticate(request, username=username, password=password)

        if(user != None):
            login(request,user)
            return redirect("/")
        else:
            messages.error(request,"not correct login info!")
        
    page = 'login'
    context = {'page':page}
    return render(request,'login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home') 

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    room_count = Room.objects.count()
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | 
                                Q(name__icontains = q)|
                                Q(description__icontains = q))
    
    list = {}
    for topic in topics:
        list[topic] = topic.room_set.count() 
    
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    display_more = True
    
    
    context = {'rooms':rooms,'list':list,'count':rooms.count(), 'room_messages':room_messages,'room_count':room_count,'display_more':display_more}
        
    return render(request,'home.html',context)

def room(request,pk):
    
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    
    if(request.method == 'POST'):
        message = Message.objects.create(
            host = request.user,
            room = room,
            description = request.POST.get('description'),
        )
        room.participants.add(request.user)
        return redirect('room',pk = pk)

    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request, 'room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if(request.method == "POST"):
        form = RoomForm(request.POST)
        if form.is_valid:
            room = form.save(commit=False)
            room.host = request.user            
            room.save()
            return redirect("home")
    context = {'form':form}

    return render(request,'room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(pk = pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form  = RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(pk=pk)
    if(request.method == 'POST'):
        room.delete()
        return redirect('home')
    context = {'context':room}
    return render(request,'delete_confirm.html',context)

def deleteMessage(request,pk):
    message = Message.objects.get(id = pk)
   
    if(request.method == 'POST'):
        message.delete()
    
        return redirect('room',pk = message.room.id)
    context = {'context':message}

    return render(request,'delete_confirm.html',context)

def userProfile(request,pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
   
    user = User.objects.get(pk=pk)
    
    rooms = user.room_set.filter(topic__name = q)
    room_count = rooms.count
  
    topics = {room.topic for room in rooms}
 
    list = {}
    for topic in topics:
        list[topic] = topic.room_set.filter(host = user).count() 
    room_messages = user.message_set.all()
    
    context= {'user':user,'topics':topics,'rooms':rooms,'room_messages':room_messages,'list':list,'room_count':room_count}
    return render(request,'user_profile.html',context)    

def topicset(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(Q(name__icontains = q))
    rooms = Room.objects.all()
    room_count = Room.objects.count()
    display_more = False
   
    context= {'topics':topics,'rooms':rooms,'room_count':room_count,'display_more':display_more}
    return render(request,"topics.html",context)

def settingsPage(request):
    form = UserForm()
    prof = ProfileForm()
    password_form = PasswordChangeForm(user = request.user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance = request.user)
        prof = ProfileForm(request.POST,request.FILES, instance = request.user.profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)


    
        if form.is_valid() & prof.is_valid(): 
            profile = prof.save(commit=False)
            userBoy = form.save()
            profile.user = userBoy
            print(profile.profile_image)
            profile.save()
           
            return redirect('settings')
        else :
            print(form.errors)
            print(prof.errors)
    
    context = {'form':form,'prof':prof,'password_form':password_form}
    
    return render(request,'settings.html',context)





