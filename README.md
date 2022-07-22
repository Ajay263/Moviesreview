<!-- This is a chaet sheet for django commands to create a movie review app  -->



<!-- Create project folder -->

mkdir MovieReview
cd MovieReview

<!-- Craete a virtual enviroment -->
python -m venv venv
venv\Scripts\activate


<!-- install django -->
pip install Django==4.0


<!-- Creating a Django project -->
django-admin startproject moviereviews .
django-admin startapp whatsapp
python manage.py migrate
python manage.py runserver



<!--  Creating a first app-->

python3 manage.py startapp movie

add the app to settings 

<!-- Creates urls -->


inside urls.py ( Movie revies root)
from movie import views as movieViews


urlpatterns = [
 path('admin/', admin.site.urls),
 path('', movieViews.home),
 
 
 ]

 <!-- Django Templates -->
 the Django Template Language (DTL). 
 ** {{ … }}** variables eg name , age variable

 ** {%. .. %} ** tags eg for ,if

 <!-- <form action="{% url 'signup' %}">    this means upon clickiung the submit button the page is going to be redirected to the about page ,  **NB**   this is the name that is specified in the urls   eg in this project 
 path('signup/', movieViews.signup, name='signup'), -->


***Nb***   dONT FORGET TO REGISTER THE MAIN TEMPLATE IN SETTINGS EG 
'DIRS': [os.path.join(BASE_DIR,'moviereviews/templates')],








<!-- Create your  Function based views -->
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

<!-- Creating Models  -->
from django.db import models


class Movie(models.Model):
 title = models.CharField(max_length=100)
 description = models.CharField(max_length=250)
 image = models.ImageField(upload_to='movie/images/')
 url = models.URLField(blank=True)

 <!-- Each models has ot its own propertiey wich depends on the type of data that will be stored inthat certain fild   eg Charfield -->


 <!-- ****Dont Forget T o un these Commands after creating the models so as tosave the models to the database -->


python manage.py makemigrations
python manage.py migrate



 <!-- Register the Model to the Admin -->

from django.contrib import admin
from .models import Movie
admin.site.register(Movie)


<!-- Create a SuperUser -->

python3 manage.py createsuperuser


<!-- How to change the superuser password? -->

python manage.py changepassword <username>

<!-- Serving the stored images -->


    <!-- in Settings  -->
    import os

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'



            <!--in the main urls.py -->

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
 …
]
urlpatterns += static(settings.MEDIA_URL,
 document_root=settings.MEDIA_ROOT)



 <!-- Serving static files -->
 In the settings file add 

 STATICFILES_DIRS = [
 BASE_DIR / 'moviereviews/static/',]

 <!-- Creating a signup form -->
 <!-- This is avery  sensiti topic but it is very easy when using django because one will beusing the Django inbuilt authentication system -->

 create an app called accounts
 configure all the urls as usual, BUT VIEWS MUST BE HANDLED AS SHOWN BELOW

 <!-- vIEWS -->
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def signupaccount(request):
    return render(request, 'signupaccount.html',{'form':UserCreationForm})




We will import UserCreationForm, which Django provides to easily create
a signup form to register new users. Django forms are a vast topic in itself, and
we will see how powerful they can be. We pass in the form to signupaccount.
html.


Next, create /accounts/templates/signupaccount.html and simply fill
in the following:


{{ form }}



POST keeps the submitted information hidden from the URL. GET, in contrast,
has the submitted data in the URL – for example, http://localhost:8000/
signup/?email=greg%40greglim.com. Because the username and password
are sensitive information, we want them hidden. A POST request will not put the
information in the URL.
In general, we use POST requests for creation and GET requests for retrieval. There
are also other requests, such as UPDATE, DELETE, and PUT, but they are more
important for creating APIs.
There is a line, {% csrf_token %}. Django provides this to protect our form
from cross-site request forgery (CSRF) attacks. You should use it for all your
Django forms.
To output our form data, we use {{ form.as_p }}, which renders it within
paragraph (<p>) tags.


<!-- Creating a user -->

inside the views paste the code below so as to create a usr after submiting the sign u page

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect


def signupaccount(request):
 if request.method == 'GET':
     Creating a user 107
     return render(request, 'signupaccount.html',{'form':UserCreationForm})
 else:
    if request.POST['password1'] == request.POST['password2']:
     user = User.objects.create_user(request.POST['username'],password= request.POST['password1'])
     user.save()
     login(request, user)
     return redirect('home')
<!-- hANDLIND ERRORS WHILE CREATING AN ACCOUNT -->
else:
     return render(request, 'signupaccount.html',{'form':UserCreationForm,'error':'Passwords do not match'})


<!--Raising AN error if the user already exists  -->
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db import IntegrityError

# Create your views here.


def signupaccount(request):
 if request.method == 'GET':
     return render(request, 'signupaccount.html',{'form':UserCreationForm})
 else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('home')
      except IntegrityError:
       return render(request,'signupaccount.html',{'form':UserCreationForm,'error':'Username already taken. Choose new username.'})
   else:
         return render(request, 'signupaccount.html',{'form':UserCreationForm,'error':'Passwords do not match'})




<!-- Customizing the user creation form -->
create a forms.py file in the accounts

from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super(UserCreateForm, self).__init__(*args,**kwargs)

    for fieldname in ['username', 'password1','password2']:
        self.fields[fieldname].help_text = None
        self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

<!-- then add the following code in to your views .py ie delete just copy the whole code the replace the one you have previously entered -->

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User

# Create your views here.


def signupaccount(request):
 if request.method == 'GET':
     return render(request, 'signupaccount.html',{'form':UserCreateForm})
 else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('home')
      except IntegrityError:
       return render(request,'signupaccount.html',{'form':UserCreateForm,'error':'Username already taken. Choose new username.'})
   else:
         return render(request, 'signupaccount.html',{'form':UserCreateForm,'error':'Passwords do not match'})






































































 

 