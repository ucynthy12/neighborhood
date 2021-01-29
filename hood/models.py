from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


class Hood(models.Model):
    locations = (
        ('Nyarutarama','Nyarutarama'),
        ('Kibagabaga','Kibagabaga'),
        ('Kimironko','Kimironko'),
        ('Kicukiro','Kicukiro'),
        ('Remera','Remera')
    )
    name = models.CharField(max_length=200)
    image = CloudinaryField('image')
    residents = models.CharField(max_length=200)
    location = models.CharField(max_length=200,choices=locations)

    class Meta:
        ordering =['-pk']

    def create_neigborhood(self):
        self.save()

    def delete_neigborhood(self):
        self.delete()
    
    @classmethod
    def find_neigborhood(cls,neigborhood_id):
        return cls.objects.filter(id=neigborhood_id)
    @classmethod
    def update_neighborhood(cls,id,name):
        return cls.objects.filter(id =id).update(name=name)
    def update_occupants(cls,id,name):
        return cls.objects.filter(id =id).update(name=name)

    def __str__(self):
        return f'{self.name} Hood'

class Profile(models.Model):
    profile_picture = CloudinaryField('image')
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    bio = models.CharField(max_length=500)
    name = models.CharField(max_length=300)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f'{self.user.username} profile'

    def save_profile(self):
        self.save()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,null=True)
    description = models.TextField()
    neighborhood = models.ForeignKey(Hood,on_delete=models.CASCADE,related_name='poster')
    posted_on = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.title} Post'

class Business(models.Model):
    name= models.CharField(max_length=200)
    email= models.EmailField(max_length=300)
    description = models.TextField(blank=True)
    neighborhood = models.ForeignKey(Hood,on_delete=models.CASCADE,related_name='business')
    user = models.ForeignKey(Profile,on_delete =models.CASCADE,related_name='owner')

    def __str__(self):
        return f'{self.name} Business'

    def create_business(self):
        self.save()
    
    def delete_business(self):
        self.delete()
    
    @classmethod
    def search_business(self,search_term):
        return cls.objects.filter(name__icontains = search_term).all()

 
