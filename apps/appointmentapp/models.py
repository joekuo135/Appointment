from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
from django.core.exceptions import ValidationError
import datetime
import bcrypt
import re

Email_Regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
Password_Regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
Name_Regex = re.compile(r'^[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, name, email, password, confirm_password, date_of_birth):
        errors = []
        if len(name) < 2:
            errors.append('Name must be longer than 2 characters')
        if not Name_Regex.match(name):
            errors.append('Name cannot have numbers')
        if len(email) == 0:
            errors.append('Please enter an email address')
        if not Email_Regex.match(email):
            errors.append('Please enter a valid email address')
        if len(password) == 0:
            errors.append('Please enter a password')
        if not Password_Regex.match(password):
            errors.append('Password must contain at least one lowercase letter, one uppercase letter, and one digit')
        if not (password) == (confirm_password):
            errors.append('Password and confirm password must be the same')
        if len(date_of_birth) == 0:
            errors.append('Please enter a Date of Birth')
        if not len(errors) == 0:
            return (False, errors)
        else:
            password = str(password)
            pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
            user = User.Usermgr.create(name = name, email = email, password = pw_hash, date_of_birth = date_of_birth)
            return (True, user)

    def login(self, email, password):
        errors = []
        if len(email) == 0:
            errors.append('Please enter an email address')
        if not Email_Regex.match(email):
            errors.append('Please enter a valid email address')
        if len(password) == 0:
            errors.append('Please enter a password')
        if not Password_Regex.match(password):
            errors.append('Password must contain at least one lowercase letter, one uppercase letter, and one digit')
        if not len(errors) == 0:
            return (False, errors)
        else:
            user = User.Usermgr.filter(email = email)
            user_password = user[0].password
            if bcrypt.hashpw(str(password), str(user_password)) == user_password:
                return (True, user)
            else:
                errors.append('Password is incorrect!')
                return (False, errors)

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(auto_now_add=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    Usermgr = UserManager()
    objects = models.Manager()


class TaskManager(models.Manager):

    def todays_tasks(self, user_id):
        return self.filter(creator=user_id, date=datetime.date.today())

    def future_tasks(self, user_id):
        return self.filter(creator=user_id, date__gt=datetime.date.today())


def validate_future_date(value):
    if value < datetime.date.today():
        raise ValidationError(_('Today\'s date or in the future.'))


class Task(models.Model):
    title = models.CharField(max_length=255)
    STATUS_CHOICES = (
        (1, 'Done'),
        (2, 'Pending'),
        (3, 'Missed'),
    )
    status = models.IntegerField(default = 2, choices=STATUS_CHOICES)
    date = models.DateField(auto_now_add=False, auto_now=False, validators=[validate_future_date])
    time = models.TimeField(auto_now=False, auto_now_add=False)
    creator =  models.ForeignKey('User', related_name="itemcreater", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    taskMgr = TaskManager()
    objects = models.Manager()

    def is_done(self):
        return self.status == 1