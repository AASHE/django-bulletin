import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from bulletin.models import Newsletter, Issue, Section, Post, ScheduledPost


class PostTests(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            title='Test Post',
            url='http://www.example.com/',
            submitter=User.objects.create(username='user',
                                          password='pword'))
        self.issue = Issue.objects.create(
            newsletter=Newsletter.objects.create(name='Newsletter'),
            name='Name',
            pub_date=datetime.datetime.today())
        self.scheduled_post = ScheduledPost.objects.create(
            post=self.post,
            pub_date=self.issue.pub_date)

    def test_make_available_to_issue(self):
        """Does make_available_to_issue work?
        """
        available_post = self.scheduled_post.make_available_to_issue(
            self.issue)
        self.assertIsNotNone(available_post)

    def test_make_available_to_issue_already_in_issue(self):
        """Does make_availalble_to_issue work when post is already in issue?
        """
        section = Section.objects.create(name='Section',
                                         issue=self.issue)
        clone = self.post.clone()
        clone.section = section
        clone.save()

        available_post = self.scheduled_post.make_available_to_issue(
            self.issue)
        self.assertIsNone(available_post)

    def test_make_all_available_to_issue(self):
        """Does make_available_to_issue work?
        """
        second_post = Post.objects.create(
            title='Second Test Post',
            url='http://www.second.com/',
            submitter=User.objects.create(username='user2',
                                          password='pword2'))
        ScheduledPost.objects.create(post=second_post,
                                     pub_date=self.issue.pub_date)
        available_posts = ScheduledPost.make_all_available_to_issue(self.issue)
        self.assertEqual(2, len(available_posts))
        for post in available_posts:
            self.assertIn(post.cloned_from, [self.post, second_post])

    def test_make_all_available_to_issue_no_matching_scheduled_posts(self):
        """Does make_available_to_issue work when there are no scheduled
        posts?
        """
        second_post = Post.objects.create(
            title='Second Test Post',
            url='http://www.second.com/',
            submitter=User.objects.create(username='user2',
                                          password='pword2'))
        ScheduledPost.objects.create(post=second_post,
                                     pub_date=self.issue.pub_date)
        second_issue = Issue(
            name='Second Issue',
            pub_date=self.issue.pub_date + datetime.timedelta(1))
        available_posts = ScheduledPost.make_all_available_to_issue(
            second_issue)
        self.assertEqual(0, len(available_posts))
