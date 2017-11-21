from django.db import models
import bcrypt
from datetime import datetime, timedelta, time
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        today = datetime.now().date()
        errors = {}
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name_error'] = "Name must be at least two characters"
        if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
            errors['password_length'] = "Password must be at least eight characters"
        if postData['password'] != postData['confirm_password']:
            errors['password_match'] = "Passwords must match"
        if User.objects.filter(email = postData['email']):
            errors['exist'] = "Account allready exist for this email.  Please choose another email."
        return errors

    def login(self, postData):
        member = User.objects.filter(email = postData['email'])
        if len(member) > 0:
            member = member[0]
            if bcrypt.checkpw(postData['password'].encode(), member.password.encode()):
                user = {'user': member}
                return user
            else:
                errors = { 'error': "Login Invalid"}
                return errors
        else:
            errors = { 'error': "Login Invalid"}
            return errors

class ActivityManager(models.Manager):
    def actvalidator(self, postData):
        today = datetime.now().date()
        errors = {}
        if not postData['title'] or not postData['description']:
            errors['name_error'] = "Please add Activity's Title and Description"
        if postData['date'] == '':
            errors['empty_date'] = 'No date was entered'
        else:
            if datetime.strptime(postData['date'],  "%Y-%m-%d").date() < today:
                errors['date_error'] = 'Activity date cannot be before today\'s date'
        if not postData['time']:
            errors['no_time'] = 'No time entered'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return '<User: {} {} {}>'.format(self.id, self.first_name, self.last_name)


class Activity(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()
    DURATION_CHOICES=(
        ('Days', 'Days'),
        ('Hours', 'Hours'),
        ('Minutes', 'Minutes'),
    )
    duration_type = models.CharField(max_length=200, choices=DURATION_CHOICES, default='Hours')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="event_coordinator")
    qty_participants = models.ManyToManyField(User, related_name="participants")
    objects = ActivityManager()
    def __str__(self):
        return '<Activity: {} {} {} {}>'.format(self.title,  self.date, self.time, self.duration)



