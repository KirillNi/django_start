from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command
from authapp.models import ShopUser


class TestMainappSmoke(TestCase):
   def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

   def test_mainapp_urls(self):
       response = self.client.get('/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/contact/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/products/')
       self.assertEqual(response.status_code, 200)

       response = self.client.get('/products/category/0/')
       self.assertEqual(response.status_code, 200)

       for category in ProductCategory.objects.all():
           response = self.client.get(f'/products/category/{category.pk}/')
           self.assertEqual(response.status_code, 200)

       for product in Product.objects.all():
           response = self.client.get(f'/products/product/{product.pk}/')
           self.assertEqual(response.status_code, 200)

   def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')


class TestUserManagement(TestCase):
   def setUp(self):
       call_command('flush', '--noinput')
       call_command('loaddata', 'test_db.json')
       self.client = Client()

       self.superuser = ShopUser.objects.create_superuser('django2', 'django2@geekshop.local', 'geekbrains')

       self.user = ShopUser.objects.create_user('tarantino', 'tarantino@geekshop.local', 'geekbrains')

       self.user_with__first_name = ShopUser.objects.create_user('umaturman', 'umaturman@geekshop.local',
                                                                 'geekbrains', first_name='Ума')

   def test_user_login(self):
       # главная без логина
       response = self.client.get('/')
       self.assertEqual(response.status_code, 200)
       self.assertTrue(response.context['user'].is_anonymous)
       self.assertEqual(response.context['title'], 'главная')
       self.assertNotContains(response, 'Пользователь', status_code=200)
       # self.assertNotIn('Пользователь', response.content.decode())

       # данные пользователя
       self.client.login(username='tarantino', password='geekbrains')

       # логинимся
       response = self.client.get('/auth/login/')
       self.assertFalse(response.context['user'].is_anonymous)
       self.assertEqual(response.context['user'], self.user)

       # главная после логина
       response = self.client.get('/')
       self.assertContains(response, 'Пользователь', status_code=200)
       self.assertEqual(response.context['user'], self.user)
       # self.assertIn('Пользователь', response.content.decode())

   def tearDown(self):
       call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')

