from django.shortcuts import render,redirect
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserForm


def room(request):
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




def room_page(request,pk):

  room = Room.objects.get(id=pk)
  room_messages = room.message_set.all().order_by('created') #retrieves all instances of messages related to rooms
  participants = room.participants.all()

  if request.method == 'POST':
    message = Message.objects.create(
      user = request.user,
      room = room,
      body = request.POST.get('message')
      )
    room.participants.add(request.user)
    return redirect('room-page',pk= room.id)

  context = {
    'room':room,
    'room_messages':room_messages,
    'participants':participants,
  }
  return render(request,'chat/room-page.html',context)



@login_required(login_url='login')
def deletemessage(request,pk):
  message = Message.objects.get(id=pk)

  if request.user != message.user:
    return HttpResponse(f"hey,you are not allowed to delete {room.host}'s room ")

  if request.method =='POST':
    message.delete()
    return redirect('room')
  
  return render(request,'chat/delete.html',{'room':room})






@login_required(login_url='login')
def createroom(request):
  form = RoomForm()
  topics = Topic.objects.all()


  if request.method == 'POST':
    topic_name= request.POST.get('topic')
    topic,created = Topic.objects.get_or_create(name=topic_name)

    Room.objects.create(
      host = request.user,
      topic= topic,
      name = request.POST.get('name'),
      description = request.POST.get('description')
      )
    return redirect('room')
    
  context = {'form': form, 'topics': topics}
  return render(request,'chat/room-form.html',context)

@login_required(login_url='login')
def updateroom(request,pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)
  topics = Topic.objects.all()


  if request.user != room.host:
    return HttpResponse(f"hey,you are not allowed to delete {room.host}'s room ")

  if request.method == 'POST':
      topic_name= request.POST.get('topic')
      topic,created = Topic.objects.get_or_create(name=topic_name)
      room.name = request.POST.get('name')
      room.topic = topic 
      room.description = request.POST.get('description')
      room.save()
      return redirect('room')
  
  context = {'form':form,'topics': topics}
  return render(request,'chat/room-form.html',context)

@login_required(login_url='login')
def deleteroom(request,pk):
  room = Room.objects.get(id=pk)

  if request.user != room.host:
    return HttpResponse(f"hey,you are not allowed to delete {room.host}'s room ")

  if request.method =='POST':
    room.delete()
    return redirect('room')
  
  return render(request,'chat/delete.html',{'room':room})



@login_required
def updateuser(request):
  user = request.user
  form = UserForm(instance=user)

  if request.method == 'POST':
     form = UserForm(request.POST, instance=user)
     if form.is_valid():
       form.save()
       return redirect('profile',pk = user.id)

  context = {
    'form':form
  }
  return render(request,"components/update-user.html",context)