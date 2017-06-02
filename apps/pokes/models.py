from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def reg(self,postData):
        if len(postData['name']) < 2 or any(char.isdigit() for char in postData['name']):
            return {'error' : 'No fewer than 2 characters in Name; letters only'}
        elif len(postData['alias']) < 2 :
            return {'error' : 'No fewer than 2 characters in Alias.'}
        elif not EMAIL_REGEX.match(postData['email']):
            return {'error' : 'Invalid Format'}
        elif len(postData['pwd']) < 8:
            return {'error': 'No fewer than 8 characters in password'}
        elif postData['confirm_pwd'] != postData['pwd']:
            return {'error': 'No match password'}

        else:
            hashed_pw = bcrypt.hashpw(postData['pwd'].encode('utf-8'), bcrypt.gensalt())
            return {'theUser' : User.objects.create(name = postData['name'], alias = postData['alias'],email = postData['email'], password = hashed_pw) }

    def login(self, postData):
        if not EMAIL_REGEX.match(postData['email']):
            return {'error' : 'Invalid Format'}

        user = User.objects.get(email = postData['email'])
        if not user:
            return {'error' : 'user does not exist.'}
        else:
            stored_hash = user.password
            input_hash = bcrypt.hashpw(postData['pwd'].encode(), stored_hash.encode())
            if not input_hash == stored_hash:
                return {'error' : 'Wrong password'}
            else:
                print "Success"
                return {'theUser' : user }



class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return "id: " + str(self.id) + ", alias: " + self.alias

    objects = UserManager()


class Poke(models.Model):
    user = models.ForeignKey(User, related_name="pokes_sent_to")
    to_who = models.ForeignKey(User, related_name = "pokes_receive_from")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


