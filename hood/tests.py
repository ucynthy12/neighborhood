from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

class HoodTestClass(TestCase):
    def setUp(self):
        self.my_hood=Hood(name='home',location='Kibagabaga',residents=1100,police=911,hospital=9191)
        self.my_hood.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.my_hood, Hood))

    def test_save_hood(self):
        self.my_hood.create_neigborhood()
        hoods= Hood.objects.all()
        self.assertTrue(len(hoods)>0)
    
    def test_delete_hood(self):
        self.my_hood.create_neigborhood()
        self.my_hood.delete_neigborhood()
        hoods = Hood.objects.all()
        self.assertTrue(len(hoods)==0)

    def test_update_hood(self):
        self.my_hood.create_neigborhood()
        self.my_hood.update_neighborhood(self.my_hood.id,'Kimi')
        update= Hood.objects.get(name='Kimi')
        self.assertEqual(update.name,'Kimi')
    
class ProfileTestClass(TestCase):

    def setUp(self):
        self.my_hood=Hood(name='home',location='Kibagabaga',residents=1100,police=911,hospital=9191)
        self.my_hood.save()

        self.new_user=User(username='ucynthy')
        self.new_user.save()

        self.new_profile = Profile(name='cynthia',location='344st12',user=self.new_user,bio='my bio',hood=self.my_hood)
        self.new_profile.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))

    def test_save_profile(self):
        self.new_profile.save_profile()
        profiles= Profile.objects.all()
        self.assertTrue(len(profiles)>0)
     
class BusinessTestClass(TestCase):

    def setUp(self):
        self.my_hood=Hood(name='home',location='Kibagabaga',residents=1100,police=911,hospital=9191)
        self.my_hood.save()
        self.new_user=User(username='ucynthy12')
        self.new_user.save()

        self.new_profile = Profile(name='cynthia',location='344st12',user=self.new_user,bio='my bio',hood=self.my_hood)
        self.new_profile.save()

    
        self.lacasa=Business(name='lacasa restaurant',email='lacasa@gmail.com',description='this is a test',hood=self.my_hood,user=self.new_profile.user)
        self.lacasa.save()

    def tearDown(self):
            User.objects.all().delete()
            Hood.objects.all().delete()
            Business.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.lacasa,Business))

    def test_save_business(self):
        self.lacasa.create_business()
        business=Business.objects.all()
        self.assertTrue(len(business)>0)

    def test_delete_business(self):
        self.lacasa.create_business()
        self.lacasa.delete_business()
        business= Business.objects.all()
        self.assertTrue(len(business)==0)

    def test_search_business(self):
        self.lacasa.create_business()
        find_business = Business.search_business('lacasa')
        self.assertTrue(len(find_business) >= 1)

class PostTestClass(TestCase):
    def setUp(self):
        self.new_user = User(username="ucynthy")
        self.new_user.save()
        self.my_hood=Hood(name='home',location='Kibagabaga',residents=1100,police=911,hospital=9191)

        self.my_hood.save()

        self.new_post=Post(title = 'Robbed',description = 'I was robbed',neighborhood=self.my_hood)

 
    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))       