from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from chatroom.models import Room,Topic,Message
from django.db.models import Q






# def homepage(request):

#   rooms = Room.objects.all #gets all the rooms available on the web app 

#   room_messages = Message.objects.all() #gets all the messages available on the web app 

#   context={
#     'rooms':rooms,
#     'room_messages' : room_messages

#   }
#   return render(request,'base/base.html',context)

def homepage(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  rooms = Room.objects.filter(Q(topic__name__icontains=q)|Q(name__icontains=q))
  topics =Topic.objects.all()
  no_rooms = rooms.count()
  room_messages = Message.objects.filter(Q(room__name__icontains = q)|(Q(room__topic__name__icontains = q)))

  context={
    'rooms':rooms,
    'topics':topics,
    'no_rooms':no_rooms,
    'room_messages':room_messages,

  }
  return render(request,'base/base.html',context)


def loginUser(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home-page')

  if request.method == 'POST':
    username = request.POST.get("username")
    password = request.POST.get('password')

    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request,'user not found')

    user = authenticate(request,username=username,password=password) # checks whether the user is on the app 

    if user is not None:
      login(request,user) #logs the user in 
      return redirect('home-page') #returns to home-page
    else:
      messages.error(request,'username or password is not found')



  context = {'page':page} 
  return render(request,'base/login-register.html',context)


def logoutUser(request):
  logout(request)
  return redirect('home-page')

def register(request):
  if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         user = form.save()
        #  user.save()

         login(request,user)
         return redirect('home-page')
      else:
        messages.error(request,'Registeration failed')
  else:
    form = UserCreationForm()
  return render(request,'base/login-register.html',{'form':form})

@login_required
def profile(request,pk):
   user = User.objects.get(id=pk)
   rooms = user.room_set.all() # all instance of room related to user 
   topics = Topic.objects.all()
   room_messages = user.message_set.all() #all instance of message related to user 


   context={
     'user':user, 
     'rooms':rooms,
     'topics':topics,
    'room_messages':room_messages }
   return render(request,'components/profile.html',context)


