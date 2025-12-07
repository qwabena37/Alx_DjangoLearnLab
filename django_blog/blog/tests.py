from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('joe', 'joe@example.com', 'password')
        self.user2 = User.objects.create_user('ann', 'ann@example.com', 'password')
        self.post = Post.objects.create(title='t', content='c', author=self.user)

    def test_authenticated_user_can_comment(self):
        self.client.login(username='ann', password='password')
        resp = self.client.post(reverse('post-detail', kwargs={'pk': self.post.pk}), {'content': 'Nice post!'}, follow=True)
        self.assertContains(resp, 'Nice post!')
