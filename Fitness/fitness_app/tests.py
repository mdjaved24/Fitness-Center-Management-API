from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from fitness_app.models import FitnessCenter
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, timedelta

User = get_user_model()

class FitnessCenterTests(APITestCase):
    def setUp(self):
        # Create users
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.owner1 = User.objects.create_user(
            username='owner1',
            email='owner1@example.com',
            password='owner1pass'
        )
        self.owner2 = User.objects.create_user(
            username='owner2',
            email='owner2@example.com',
            password='owner2pass'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass'
        )
        
        # Create fitness centers
        self.center1 = FitnessCenter.objects.create(
            name='Power Gym',
            address='123 Fitness St',
            monthly_fee=1000,
            total_sessions=8,
            category='GYM',
            facilities='Treadmills,Weights,Showers',
            owner=self.owner1,
            is_verified=True,
            established_date=date.today() - timedelta(days=365))
        
        self.center2 = FitnessCenter.objects.create(
            name='Peace Yoga',
            address='456 Wellness Ave',
            monthly_fee=1500,
            total_sessions=12,
            category='YOGA',
            facilities='Mats,Meditation Room',
            owner=self.owner2,
            is_verified=False,
            established_date=date.today() - timedelta(days=180))
        
        # URLs
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.center_list_url = reverse('center-list')
        self.category_filter_url = lambda category: reverse('category-filter', kwargs={'category': category})
        self.center_detail_url = lambda id: reverse('center-detail', args=[id])

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    # Authentication Tests
    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpass'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        data = {
            'username': 'owner1',
            'password': 'owner1pass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # Center List Tests
    def test_get_center_list_unauthenticated(self):
        response = self.client.get(self.center_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Now checking direct response length
        # Check price per session calculation
        self.assertAlmostEqual(response.data[0]['price_per_session'], 125.0)  # 1000/8
        self.assertAlmostEqual(response.data[1]['price_per_session'], 125.0)  # 1500/12

    # Filtering Tests (Query Params)
    def test_filter_by_monthly_fee(self):
        url = f"{self.center_list_url}?min_fee=1200&max_fee=1600"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Peace Yoga')

    def test_filter_by_facilities(self):
        url = f"{self.center_list_url}?facilities=Showers"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Power Gym')

    # Filtering Tests (Path Param)
    def test_filter_by_category_path_param(self):
        url = self.category_filter_url('YOGA')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Peace Yoga')

    # Ordering Tests
    def test_order_by_monthly_fee(self):
        url = f"{self.center_list_url}?ordering=monthly_fee"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Power Gym')
        self.assertEqual(response.data[1]['name'], 'Peace Yoga')

    def test_order_by_established_date_desc(self):
        url = f"{self.center_list_url}?ordering=-established_date"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Peace Yoga')
        self.assertEqual(response.data[1]['name'], 'Power Gym')

    # Center Detail Tests
    def test_get_center_detail_with_calculation(self):
        url = self.center_detail_url(self.center1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Power Gym')
        self.assertAlmostEqual(response.data['price_per_session'], 125.0)  # 1000/8

    # Create Center Tests
    def test_create_center_with_invalid_data(self):
        token = self.get_token_for_user(self.owner1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {
            'name': 'Invalid Center',
            'address': '789 Test Rd',
            'monthly_fee': 499,  # Below minimum
            'total_sessions': 3,  # Below minimum
            'category': 'GYM',
            'facilities': 'Test',
            'established_date': date.today() + timedelta(days=1)  # Future date
        }
        response = self.client.post(self.center_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('monthly_fee', response.data)
        self.assertIn('total_sessions', response.data)
        self.assertIn('established_date', response.data)

    # Update Tests
    def test_update_center_by_owner(self):
        token = self.get_token_for_user(self.owner1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = self.center_detail_url(self.center1.id)
        data = {
            'name': 'Power Gym Plus',
            'address': '123 Fitness St Updated',
            'monthly_fee': 1200,
            'total_sessions': 10,
            'category': 'GYM',
            'facilities': 'Treadmills,Weights,Showers,Pool',
            'established_date': self.center1.established_date
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.center1.refresh_from_db()
        self.assertEqual(self.center1.name, 'Power Gym Plus')
        # Check calculation in response
        self.assertAlmostEqual(response.data['price_per_session'], 120.0)  # 1200/10

    # Test for unique name validation
    def test_create_center_duplicate_name(self):
        token = self.get_token_for_user(self.owner1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {
            'name': 'Power Gym',  # Duplicate name
            'address': '789 Test Rd',
            'monthly_fee': 1000,
            'total_sessions': 8,
            'category': 'GYM',
            'facilities': 'Test',
            'established_date': date.today()
        }
        response = self.client.post(self.center_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'][0], 'fitness center with this name already exists.')