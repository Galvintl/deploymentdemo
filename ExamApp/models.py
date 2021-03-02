from django.db import models
from datetime import date
import re
import bcrypt


# Create your models here.


class UserManager(models.Manager):
    def validateUser(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        userEmailMatches = User.objects.filter(email = postData["email"])
        errors = {}
        if len(postData['first_name']) ==0:
            errors['first_name'] = "Your first name is required"
        elif len(postData['first_name']) < 2 :
            errors['first_name'] = "Your first name should contain at least 2 letters."
        if len(postData['last_name']) ==0:
            errors["last_name"] = "Your last name is required "
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name should be at least 2 letters long"
        if len(postData['email']) ==0:
            errors["email"] = "Email required!" 
        elif not EMAIL_REGEX.match(postData["email"]):
            errors['emailPattern'] = "Email is not valid, should be in a valid format, i.e. YourEmailAddress@provider.com!"
        elif len(userEmailMatches) > 0:
            errors['emailTaken'] = "Looks like you already registered, or your doppelganger!"
        if len(postData['password']) == 0:
            errors['password'] = "Password required"
        elif len(postData['password']) < 8:
            errors['password'] = "Please make password at least 8 characters long"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password does not match"
        
        return errors

    def validateEmail(self, postData):
        errors = {}
        userEmailMatches = User.objects.filter(email = postData["email"])
        if len(userEmailMatches) == 0:
            errors['emailNotFound'] = "This email is not yet registered.  Please register first."

        return errors

    def validateLogin(self, postData):
        errors = {}
        userEmailMatches = User.objects.filter(email = postData["email"])
        if len(userEmailMatches) == 0:
            errors['emailNotFound']="Email not found, please register first!"
        elif  not bcrypt.checkpw(postData['password'].encode(), userEmailMatches[0].password.encode()):

            errors["incorrectPassword"]= "Incorrect Password"

        return errors

    def validateUpdate(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        userEmailMatches = User.objects.filter(email = postData["email"])
        errors = {}
        if len(postData['first_name']) ==0:
            errors['first_name'] = "Your first name is required"
        elif len(postData['first_name']) < 2 :
            errors['first_name'] = "Your first name should contain at least 2 letters."
        if len(postData['last_name']) ==0:
            errors["last_name"] = "Your last name is required "
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name should be at least 2 letters long"
        if len(postData['email']) ==0:
            errors["email"] = "Email required!" 
        elif not EMAIL_REGEX.match(postData["email"]):
            errors['emailPattern'] = "Email is not valid, should be in a valid format, i.e. YourEmailAddress@provider.com!"
        elif len(userEmailMatches) > 0:
            errors['emailTaken'] = "Looks like you already registered, or your doppelganger!"

        return errors 

class QuotesManager(models.Manager):
    def validateQuote(self, postData):
        errors = {}
        if len(postData['author']) == 0:
            errors['author'] = "Author is required"
        elif len(postData['author']) < 3 :
            errors['author'] = "An Author name should contain at least 3 letters."
        if len(postData['quote']) == 0:
            errors['quote'] = "A quote is required "
        elif len(postData['quote']) < 10:
            errors['quote'] = "The quote should be at least 10 letters long"

        return errors


class User (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"<first_name:{self.first_name}, last_name:{self.last_name}, email={self.email}>"

class Quotes (models.Model):
    author = models.CharField(max_length=255)
    quote = models.CharField(max_length=255)
    like = models.ManyToManyField(User, related_name="liked")
    post = models.ForeignKey(User, related_name="posted", on_delete = models.CASCADE)
    objects = QuotesManager ()

    def __str__(self):
        return f"<author:{self.author}, quote:{self.quote}>"