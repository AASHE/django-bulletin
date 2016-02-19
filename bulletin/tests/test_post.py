import datetime

from django.contrib.auth.models import User
from django.test import TestCase
import pytz

from bulletin.models import Category, Post, PostCategory


class PostTests(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            date_submitted=datetime.datetime.now(pytz.utc),
            title='Blue headline',
            url='http://www.agami.com',
            submitter=User.objects.create(username='Burroughs'),
            approved=True,
            include_in_newsletter=False,
            feature=True,
            pub_date=datetime.datetime.now(pytz.utc),
            image="cleaver_artist.jpg")
        self.categories = [Category.objects.create(name="1"),
                           Category.objects.create(name="2"),
                           Category.objects.create(name="3")]
        PostCategory.objects.create(category=self.categories[0],
                                    post=self.post,
                                    primary=False)
        PostCategory.objects.create(category=self.categories[1],
                                    post=self.post,
                                    primary=True)
        PostCategory.objects.create(category=self.categories[2],
                                    post=self.post,
                                    primary=False)

    def test_primary_category_property_getter(self):
        """ Does Post.primary_category return the correct Category? """
        self.assertEqual(self.post.primary_category, self.categories[1])

    def test_primary_category_property_setter(self):
        """ Does Post.primary_category set the correct Category? """
        self.post.primary_category = self.categories[0]
        self.assertEqual(self.post.primary_category, self.categories[0])

    def test_clone_handles_simple_fields(self):
        """ Does clone() handle simple fields correctly? """
        clone = self.post.clone()
        self.assertEqual(clone.date_submitted, self.post.date_submitted)
        self.assertEqual(clone.title, self.post.title)
        self.assertEqual(clone.url, self.post.url)
        self.assertEqual(clone.submitter, self.post.submitter)
        self.assertEqual(clone.approved, self.post.approved)
        self.assertEqual(clone.include_in_newsletter,
                         self.post.include_in_newsletter)
        self.assertEqual(clone.feature, self.post.feature)
        self.assertEqual(clone.pub_date, self.post.pub_date)
        self.assertEqual(clone.image.name, self.post.image.name)

    def test_clone_handles_categories(self):
        """ Does clone() handle Post.categories correctly? """
        clone = self.post.clone()
        for i, post_category in enumerate(
                PostCategory.objects.filter(post=clone)):
            self.assertEqual(post_category.category,
                             self.categories[i].category)
            self.assertEqual(post_category.primary,
                             self.categories[i].primary)
