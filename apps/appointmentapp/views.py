from django.shortcuts import render, HttpResponse, redirect
from .models import User, Task
from django.contrib import messages
import datetime

def index(request):
    return render(request, 'appointmentapp/index.html')

def validation(request):
    if request.method == "POST":
        user = User.Usermgr.filter(email = request.POST['email'])
        if user:
            messages.add_message(request, messages.INFO, 'User already exists, please login!')
            return redirect('/')
        else:
            result = User.Usermgr.register(request.POST['name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['date_of_birth'])
            if result[0] == True:
                request.session['user_id'] = result[1].id
                request.session['status'] = 'registered'
                return redirect('/welcome')
            else:
                error_msg = result[1]
                for i in range(len(error_msg)):
                    messages.add_message(request, messages.ERROR, error_msg[i])
                return redirect('/')
    else:
        return redirect('/')


def welcome(request):
    user =  User.Usermgr.filter(id=request.session['user_id'])
    name = user[0].name
    #tasks = user[0].task_set.all()
    todays_tasks = Task.taskMgr.todays_tasks(user[0].id)
    future_tasks = Task.taskMgr.future_tasks(user[0].id)
    #first_name = User.Usermgr.get(id=request.session['user_id']).first_name
    context = {
        'name': name,
        'todays_tasks': todays_tasks,
        'future_tasks': future_tasks,
        'date' : datetime.date.today()
    }
    return render(request, 'appointmentapp/welcome.html', context)


def login(request):
    if request.method == "POST":
        user = User.Usermgr.filter(email = request.POST['email'])
        if not user:
            messages.add_message(request, messages.INFO, 'User does not exist, please Register!')
            return redirect('/')
        else:
            result = User.Usermgr.login(request.POST['email'], request.POST['password'])
            i = User.Usermgr.filter(email = request.POST['email'])
            if result[0] == True:
                request.session['user_id'] = i[0].id
                request.session['status'] = 'log'
                return redirect('/welcome')
            else:
                error_msg = result[1]
                for i in range(len(error_msg)):
                    messages.add_message(request, messages.ERROR, error_msg[i])
                return redirect('/')
    return redirect('/')


def add(request):
    user_list =  User.Usermgr.filter(id=request.session['user_id'])
    t_date = request.POST['date']
    t_time = request.POST['time']
    title = request.POST['title']
    t_date_time = ('%s %s' % (t_date, t_time))
    t_date_time = datetime.datetime.strptime(t_date_time, '%Y-%m-%d %H:%M')
    if len(t_date) < 1:
        messages.add_message(request, messages.ERROR, 'You must complete the Date Field!')
    elif len(t_date) < 1:
        messages.add_message(request, messages.ERROR, 'You must complete the Time Field!')
    elif datetime.datetime.now() > t_date_time:
        messages.add_message(request, messages.ERROR, 'Only current and future time is allowed! ')
    elif len(title) < 1:
        messages.add_message(request, messages.ERROR, 'You must complete the Task Field!')
    else:
        task = Task(title=title, date=t_date, time=t_time, creator=user_list[0])
        task.save()
    return redirect('/welcome')


def edit(request, task_id):
    task =  Task.objects.get(id=task_id)
    context = {'task' : task, 'date':task.date.strftime('%Y-%m-%d'), 'time':task.time.strftime('%I:%M %p')}
    return render(request, 'appointmentapp/edit.html', context)


def update(request):

    if request.method == "POST":
        user_list =  User.Usermgr.filter(id=request.session['user_id'])
        task_list =  Task.taskMgr.filter(id=request.POST['id'])
        task = task_list[0]
        context = {'task' : task, 'date':task.date.strftime('%Y-%m-%d')}
        t_date = request.POST['date']
        t_time = request.POST['time']
        title = request.POST['title']
        status = request.POST['status']
        t_date_time = ('%s %s' % (t_date, t_time))
        t_date_time = datetime.datetime.strptime(t_date_time, '%Y-%m-%d %H:%M')
        if len(t_date) < 1:
            messages.add_message(request, messages.ERROR, 'You must complete the Date Field!')
            return render(request, 'appointmentapp/edit.html', context)
        elif len(t_time) < 1:
            messages.add_message(request, messages.ERROR, 'You must complete the Time Field!')
            return render(request, 'appointmentapp/edit.html', context)
        elif datetime.datetime.now() > t_date_time:
            messages.add_message(request, messages.ERROR, 'Only current and future time is allowed! ')
            return render(request, 'appointmentapp/edit.html', context)
        elif len(title) < 1:
            messages.add_message(request, messages.ERROR, 'You must complete the Task Field!')
            return render(request, 'appointmentapp/edit.html', context)
        else:
            task_list.update(title=title, date=t_date, time=t_time, status=status, creator=user_list[0])
            #task.save()
            return redirect('/welcome')

def delete(request, task_id):
    task = Task.objects.get(id = task_id)
    task.delete()
    return redirect('/welcome')


def logout(request):
    request.session.pop('user_id')
    return redirect ('/')
