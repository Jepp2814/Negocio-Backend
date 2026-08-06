from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_endpoint_returns_ok(self):
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_home_endpoint_returns_payload(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Sitio funcionando ✅')


class PerfilSelectorTests(TestCase):
    def test_new_user_appears_in_profile_selector(self):
        response = self.client.post(
            reverse('registro'),
            {
                'first_name': 'Ana',
                'last_name': 'López',
                'fecha_nacimiento': '2000-01-01',
                'pais': 'Colombia',
                'ciudad': 'Bogotá',
                'email': 'ana@example.com',
                'celular': '3000000000',
                'username': 'ana123',
                'password1': 'Test1234!',
                'password2': 'Test1234!',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('login'))
        self.assertContains(response, 'ana123')
