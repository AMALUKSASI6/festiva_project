from django.db import models
from datetime import datetime  
from django.contrib.auth.models import User

# Create your models here.

class Gallery(models.Model):
	image  = models.ImageField(upload_to='galleryimages')
	description = models.CharField(max_length = 500)

class Comments (models.Model):
	image = models.ForeignKey(Gallery,models.CASCADE)
	user = models.ForeignKey(User,models.CASCADE)
	comment = models.CharField(max_length = 500)

class Images(models.Model):
    name = models.CharField(max_length = 100)
    user = models.ForeignKey(User,models.CASCADE)
    email = models.CharField(max_length = 100)
    image  = models.ImageField(upload_to='images')
    date = 	models.DateTimeField(default=datetime.now(), blank=True)
    artistimage  = models.ImageField(upload_to='images')
    def __str__(self):
    	return "user = "+self.name
    
class Reachme(models.Model):
    user = models.ForeignKey(User,models.CASCADE)
    reply = models.CharField(max_length = 500)
    message =models.CharField(max_length = 500)
    def __str__(self):
        return str(self.user)+ " Message:"+self.message+" -Reply:"+self.reply
    class Meta:
        verbose_name_plural = "Messages"  

class Admincontact(models.Model):
    name  = models.CharField(max_length = 500)
    email  = models.CharField(max_length = 500)
    phonenumber  = models.CharField(max_length = 500)
    address = models.CharField(max_length = 500)
    def __str__(self):
        return "Name:"+self.name+" /Email:"+self.email+" /Phone Number"+self.phonenumber+" /Address: "+self.address
    class Meta:
        verbose_name_plural = "Admin Contact Details"    

class Events(models.Model):
    name  = models.CharField(max_length = 500)
    details  = models.CharField(max_length = 500)
    eventdate = models.DateTimeField(default=datetime.now(), blank=True)
    updateddate = models.DateTimeField(default=datetime.now(), blank=True)
    def __str__(self):
        return "Event :"+self.name+" , Date: "+str(self.eventdate)+"." 
    class Meta:
        verbose_name_plural = "Add Events"           

class Liveupdates(models.Model):
    event = models.ForeignKey(Events,models.CASCADE)
    update = models.CharField(max_length = 500)
    datetime = models.DateTimeField(default=datetime.now(), blank=True)
    def __str__(self):
        return str(self.event)+", Update : "+self.update
    class Meta:
        verbose_name_plural = "Add Live updates"         


class Eventcordinaters(models.Model):
    event = models.ForeignKey(Events,models.CASCADE)
    user = models.ForeignKey(User,models.CASCADE)
    accept = models.CharField(max_length = 100,choices=[('Pending', 'Pending'), ('Rejected', 'Rejected'),('Accepted', 'Accepted')])
    def __str__(self):
        return str(self.event)+", user : "+str(self.user)+", status : "+self.accept   
    class Meta:
        verbose_name_plural = "Event cordinaters"    

class Adminmessagestouser(models.Model):    
    user = models.ForeignKey(User,models.CASCADE,blank=True)
    message =models.CharField(max_length = 500)
    class Meta:
        verbose_name_plural = "Admin messages to users"     

