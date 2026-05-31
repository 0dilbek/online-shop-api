import tempfile
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from ads.models import Advertisement


GIF_BYTES = (
    b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!'
    b'\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01'
    b'\x00\x00\x02\x02D\x01\x00;'
)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class AdvertisementPanelTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username='staff',
            password='pass',
            is_staff=True,
        )
        self.client.force_login(user)

    def test_create_advertisement_without_image(self):
        response = self.client.post(reverse('panel:ad-create'), {
            'title': 'Test reklama',
            'text': 'Reklama matni',
            'image_path': '',
        })

        self.assertRedirects(response, reverse('panel:ad-list'))
        self.assertTrue(Advertisement.objects.filter(title='Test reklama').exists())

    def test_create_advertisement_with_uploaded_image_uses_media_path(self):
        image = SimpleUploadedFile('ad.gif', GIF_BYTES, content_type='image/gif')

        response = self.client.post(reverse('panel:ad-create'), {
            'title': 'Rasmli reklama',
            'text': 'Reklama matni',
            'image_file': image,
        })

        self.assertRedirects(response, reverse('panel:ad-list'))
        ad = Advertisement.objects.get(title='Rasmli reklama')
        self.assertTrue(ad.image_path.startswith('media/ads/'))
        self.assertIn('/media/ads/', ad.image)

    def test_upload_storage_error_returns_form_error_without_saving(self):
        image = SimpleUploadedFile('ad.gif', GIF_BYTES, content_type='image/gif')

        with patch('panel.views.ads._save_image', side_effect=OSError):
            response = self.client.post(reverse('panel:ad-create'), {
                'title': 'Saqlanmasin',
                'text': 'Reklama matni',
                'image_file': image,
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Advertisement.objects.filter(title='Saqlanmasin').exists())
        self.assertFormError(
            response.context['form'],
            'image_file',
            "Rasmni saqlab bo'lmadi. Serverdagi media papka huquqlarini tekshiring.",
        )
