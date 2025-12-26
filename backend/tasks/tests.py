from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Campaign


class CampaignModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
    def test_campaign_creation(self):
        campaign = Campaign.objects.create(
            name='Test Campaign',
            description='Test Description',
            campaign_type='email',
            status='active',
            budget=1000.00,
            created_by=self.user
        )
        self.assertEqual(campaign.name, 'Test Campaign')
        self.assertEqual(campaign.created_by, self.user)
        self.assertEqual(str(campaign), 'Test Campaign')


class CampaignViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.campaign = Campaign.objects.create(
            name='Test Campaign',
            description='Test Description',
            campaign_type='email',
            status='active',
            budget=1000.00,
            created_by=self.user
        )
        
    def test_get_campaigns(self):
        url = reverse('campaign-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_create_campaign(self):
        url = reverse('campaign-list')
        data = {
            'name': 'New Campaign',
            'description': 'New Description',
            'campaign_type': 'social',
            'status': 'planning',
            'budget': 2000.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.count(), 2)
        
    def test_update_campaign(self):
        url = reverse('campaign-detail', kwargs={'pk': self.campaign.pk})
        data = {'name': 'Updated Campaign'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.name, 'Updated Campaign')
        
    def test_delete_campaign(self):
        url = reverse('campaign-detail', kwargs={'pk': self.campaign.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Campaign.objects.count(), 0)
        
    def test_unauthorized_access(self):
        self.client.credentials()
        url = reverse('campaign-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)