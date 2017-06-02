from django.shortcuts import render, redirect
from .models import User, Poke
from django.db.models import Count

# Create your views here.
def index(request):

    return render(request, 'pokes/index.html')


def create(request):
    context = {
        'name' : request.POST['name'], 
        'alias' : request.POST['alias'], 
        'email' : request.POST['email'], 
        'pwd' : request.POST['pwd'], 
        'confirm_pwd' : request.POST['confirm_pwd']
    }

    user = User.objects.reg(context)

    if 'error' in user:
        messages.warning(request, user['error'])
        return redirect('/')
    
    if 'theUser' in user:
        request.session['alias'] = user['theUser'].alias
        request.session['id'] = user['theUser'].id
        return redirect('/pokes')

def login_process(request):
    context = { 
        'email' : request.POST['email'], 
        'pwd' : request.POST['pwd'] 
    }
    user = User.objects.login(context)

    if 'error' in user:
        messages.warning(request, user['error'])
        return redirect('/')
    
    if 'theUser' in user:
        request.session['alias'] = user['theUser'].alias
        request.session['id'] = user['theUser'].id
        return redirect('/pokes')


def pokes(request):
    # print User.objects.get(id = request.session['id']).pokes_receive_from.all().count()

    users = Poke.objects.filter(to_who = User.objects.get(id = request.session['id'])).values('user').annotate(num_of_pokes = Count('to_who'))
    allinfo = []
    
    for user in users:
        info = {}
        info['name'] = User.objects.get(id = user['user']).alias
        info['num'] = user['num_of_pokes']
        allinfo.append(info)


    context = {
        'name' : request.session['alias'],
        'how_many' : len(allinfo),
        'allinfo' : allinfo,
        'other_users' : User.objects.exclude(id = request.session['id'])
    }
    return render(request, 'pokes/pokes.html', context)

def make_poke(request, user_id, active_user_id):
    Poke.objects.create(user = User.objects.get(id = active_user_id), to_who = User.objects.get(id = user_id))
    return redirect('/pokes')


def logout(request):
    request.session.clear()
    return  redirect('/')