from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from .models import User
# Create your views here.
def flash_errors(errors, request):
    for error in errors:
        messages.error(request, error)

def current_user(self, request):
    return User.objects.get(id = request.session['user_id'])

def index(request):
    print "index"
    return render(request, 'login/index.html')

def home(request):
    if 'user_id' in request.session:
        current_user = User.objects.get(id = request.session['user_id'])
        friends = current_user.friended.all()
        other_users = User.objects.exclude(id__in=friends).exclude(id=current_user.id)
        context = {
            'current_user': current_user,
            'friends': friends,
            'persons': other_users,
        }
        return render(request, 'login/home.html', context)
    return redirect(reverse('landing'))

def register(request):
    if request.method == "POST":
        #Validate form data
        errors = User.objects.validate_registration(request.POST)
        #Check if errors don't exist
        if not errors:
            #create User
            user = User.objects.create_user(request.POST)
            #log in the User
            request.session['user_id'] = user.id
            #redirect to success page
            return redirect(reverse('home'))
        #Flash errors
        flash_errors(errors, request)

        print request.POST

    return redirect(reverse('landing'))

def add(request, id):
    current_user = User.objects.current_user(request)
    friend = User.objects.filter(id=id).first()

    current_user.friended.add(friend)

    return redirect(reverse('home'))

def remove(request, id):
    current_user = User.objects.current_user(request)
    friend = User.objects.filter(id=id).first()

    current_user.friended.remove(friend)

    return redirect(reverse('home'))

def user(request, id):

        context = {

            'user': User.objects.filter(id=id).first()
        }
        return render(request, 'login/user.html', context)

def login(request):
    if request.method == "POST":
        #validate my login data
        check = User.objects.validate_login(request.POST)
        if 'user' in check:
            #log in user
            request.session['user_id'] = check['user'].id
            #redirect to succes page
            return redirect(reverse('home'))
        #flash error messages
        flash_errors(check['errors'], request)
    return redirect(reverse('landing'))

def logout(request):
    if 'user-id' in request.session:
        request.session.pop('user_id')

    return redirect(reverse('landing'))
