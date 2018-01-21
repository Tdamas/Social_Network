from __future__ import unicode_literals
from django.db import models
import datetime
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_registration(self, form_data):
        errors = []
        #First name errors
        if len(form_data['name']) < 2:
            errors.append("Name is required of at least 2 characters.")
        #Alias
        if len(form_data['alias']) < 2:
            errors.append("Alias is required of at least 2 characters.")
        #Email
        if len(form_data['email']) == 0:
            errors.append("Email address is required.")
        #Password
        if len(form_data['password']) == 0:
            errors.append("Password is required.")
        #Password confirmation
        if form_data['confirm_PW'] != form_data['confirm_PW']:
            errors.append("Password must match.")

        return errors

    def validate_login(self, form_data):
        errors = []
        #Email
        if len(form_data['email']) == 0:
            errors.append("Email address is required.")
        #Password
        if len(form_data['password']) == 0:
            errors.append("Password is required.")

        user = User.objects.filter(email=form_data['email']).first()

        if user:
            user_password = form_data['password'].encode()
            db_password = user.password.encode()

            if bcrypt.checkpw(user_password, db_password):
                return {'user': user}
            errors.append('Invalid password.')
        errors.append('No account with that email.')

        return {'errors': errors}

    def create_user(self, form_data):
        hashedpw  = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())

        return User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'],
            password = hashedpw,
        )
    
    def current_user(self, request):
        current_user = User.objects.get(id = request.session['user_id'])
        return current_user


class User(models.Model):
    name = models.CharField(max_length = 90, default=" ")
    email = models.CharField(max_length = 45)
    alias = models.CharField(max_length = 45, default=" ")
    friended = models.ManyToManyField("self", related_name="friended_by")
    password = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        string_output = "id: {} name: {} alias: {} email: {} created_at: {} updated_at: {}"
        return string_output.format (
        self.id,
        self.name,
        self.alias,
        self.email,
        self.created_at,
        self.updated_at,
    )
    objects = UserManager()
