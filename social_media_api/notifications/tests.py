from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class LikesNotificationsTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass')
        self.user2 = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(author=self.user1, title='t', content='c')

    def test_like_creates_notification(self):
        # login user2 and like post
        self.client.force_authenticate(user=self.user2)
        resp = self.client.post(f'/api/posts/{self.post.pk}/like/')
        self.assertEqual(resp.status_code, 201)
        # check recipient notifications
        self.client.force_authenticate(user=self.user1)
        notif_resp = self.client.get('/api/notifications/')
        self.assertEqual(notif_resp.status_code, 200)
        self.assertTrue(any(n['actor'] == 'bob' and n['verb'] == 'liked' for n in notif_resp.data))
