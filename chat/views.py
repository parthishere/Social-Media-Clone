from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def room(request, room_id):
    return render(request, 'room.html', {"room_id":room_id})