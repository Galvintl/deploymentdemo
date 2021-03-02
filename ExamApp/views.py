from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quotes
import bcrypt



# Create your views here.


def index(request):
    return render(request, "LoginForm.html")

def register(request):
    print(request.POST)

    ValidationErrors = User.objects.validateUser(request.POST)
    if len(ValidationErrors) > 0:
        for key, value in ValidationErrors.items():
            messages.error(request,value)
        return redirect("/")

    encryptedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    newUser=User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=encryptedpw)

    request.session['loggedInID']= newUser.id

    return redirect("/")


def login(request):
    print(request.POST)
    ValidationErrors = User.objects.validateLogin(request.POST)
    if len(ValidationErrors) > 0:
        for key, value in ValidationErrors.items():
            messages.error(request,value)
        return redirect("/")
    
    userswithMatchingEmail = User.objects.filter(email = request.POST['email'])
    request.session['loggedInId'] = userswithMatchingEmail[0].id

    return redirect("/quotes")


def logout(request):
    request.session.clear()
    return redirect("/")

def allquotes(request):
    context = {
        "allQuotes":Quotes.objects.all(),
        "loggedinUser" :User.objects.get(id= request.session['loggedInId'])
    }
    return render(request, "allquotes.html", context)

def deletequote (request, idQuote):
    deletequote=Quotes.objects.get(id=idQuote)
    deletequote.delete()

    return redirect("/quotes")

def createquote(request):
    print("newquote")
    ValidationErrors = Quotes.objects.validateQuote(request.POST)
    if len(ValidationErrors) > 0:
        for key, value in ValidationErrors.items():
            messages.error(request,value)
        return redirect("/quotes")

    newquote=Quotes.objects.create(author=request.POST["author"], quote=request.POST["quote"], post=User.objects.get(id=request.session['loggedInId']))
    User.objects.get(id=request.session['loggedInId']).liked.add(newquote)

    return redirect("/quotes")

def userquotes(request, idQuote):
    context = {
        "allQuotes":Quotes.objects.all(),
        "QuoteObj" : Quotes.objects.get(id=idQuote),
        "loggedinUser" :User.objects.get(id= request.session['loggedInId'])
    }
    return render(request, "userquotes.html", context)

def editaccount(request, idUser):
    context = {
        
        "idUser" :User.objects.get(id= request.session['loggedInId'])
        
    }
    
    return render(request, "editaccount.html", context)

def updateaccount(request, idUser):

    ValidationErrors = User.objects.validateUpdate(request.POST)
    if len(ValidationErrors) > 0:
        for key, value in ValidationErrors.items():
            messages.error(request,value)
        return redirect(f"/myaccount/{idUser}")
        
    # userswithMatchingEmail = User.objects.filter(email = request.POST['email'])
    # request.session['loggedInId'] = userswithMatchingEmail[0].id 
    # return redirect(f"/myaccount/{idUser}")

    update = User.objects.get(id=idUser)
    update.first_name = request.POST["first_name"]
    update.last_name = request.POST["last_name"]
    update.email = request.POST["email"]
    update.save()

    return redirect("/")


def like (request, idQuote):
    
    User.objects.get(id=request.session['loggedInId']).liked.add(Quotes.objects.get(id=idQuote))
    return redirect("/quotes")
