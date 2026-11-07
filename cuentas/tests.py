from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CuentasTests(TestCase):

    def test_registro_crea_usuario_e_inicia_sesion(self):
        respuesta = self.client.post(reverse('cuentas:registro'), {
            'username': 'prueba1',
            'first_name': 'Ana',
            'last_name': 'Prueba',
            'email': 'prueba1@ejemplo.com',
            'password1': 'Acordeon#2027x',
            'password2': 'Acordeon#2027x',
        })
        self.assertRedirects(respuesta, reverse('votaciones:inicio'))
        self.assertTrue(User.objects.filter(username='prueba1').exists())
        self.assertIn('_auth_user_id', self.client.session)

    def test_registro_con_contrasenas_distintas_no_crea_usuario(self):
        self.client.post(reverse('cuentas:registro'), {
            'username': 'prueba2',
            'first_name': 'Luis',
            'last_name': 'Prueba',
            'email': 'prueba2@ejemplo.com',
            'password1': 'Acordeon#2027x',
            'password2': 'OtraClave#999',
        })
        self.assertFalse(User.objects.filter(username='prueba2').exists())

    def test_perfil_requiere_iniciar_sesion(self):
        respuesta = self.client.get(reverse('cuentas:perfil'))
        url_esperada = reverse('cuentas:login') + '?next=' + reverse('cuentas:perfil')
        self.assertRedirects(respuesta, url_esperada)

    def test_login_y_logout(self):
        User.objects.create_user(username='votante', password='Acordeon#2027x')

        respuesta = self.client.post(reverse('cuentas:login'), {
            'username': 'votante',
            'password': 'Acordeon#2027x',
        })
        self.assertRedirects(respuesta, reverse('votaciones:inicio'))
        self.assertIn('_auth_user_id', self.client.session)

        respuesta = self.client.post(reverse('cuentas:logout'))
        self.assertRedirects(respuesta, reverse('votaciones:inicio'))
        self.assertNotIn('_auth_user_id', self.client.session)