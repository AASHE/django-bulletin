import datetime
import operator
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import (Category,
                      Issue,
                      IssueTemplate,
                      Newsletter,
                      Section,
                      SectionTemplate,
                      Post,
                      AdSize,
                      Ad)


def section_template_factory(newsletter=None,
                             issue_template=None,
                             name='Test Section Template'):
    if newsletter is None:
        try:
            newsletter = Newsletter.objects.get(name='Test Newsletter')
        except Newsletter.DoesNotExist:
            newsletter = Newsletter.objects.create(name='Test Newsletter')
    issue_template = issue_template or IssueTemplate.objects.create(
        newsletter=newsletter,
        name='Test Issue Template')
    name = name or 'Test Section Template'
    section_template = SectionTemplate.objects.create(
        issue_template=issue_template,
        name=name)
    return section_template


class CategoryTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_category(self):
        """Can we create a Category?
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)
        self.client.force_authenticate(user=staff_user)
        url = reverse('bulletin:api:category-list')
        data = {'name': 'Test Category'}
        response = self.client.post(url,
                                    data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_only_for_admins(self):
        """Can only admins create a Category?
        """
        non_staff_user = User.objects.create(username='non-staff',
                                             is_staff=False)
        self.client.force_authenticate(user=non_staff_user)
        url = reverse('bulletin:api:category-list')
        data = {'name': 'Test Category'}
        response = self.client.post(url,
                                    data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_a_category_with_section_templates(self):
        """Can we list a Category that has related SectionTemplates?
        """
        category = Category.objects.create(name='Test Category')
        section_template = section_template_factory()
        another_section_template = section_template_factory(
            newsletter=section_template.issue_template,
            issue_template=section_template.issue_template,
            name='Another Test Section Template')
        category.section_templates.add(section_template,
                                       another_section_template)
        category.save()

        url = reverse('bulletin:api:category-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostTests(APITestCase):

    def setUp(self):
        self.new_post_data = {
            'title': 'Test Post Headline',
            'url': 'http://api.aashe.org'
        }
        newsletter = Newsletter(name='Test Newsletter')
        newsletter.save()
        self.issue = Issue.objects.create(newsletter=newsletter,
                                          pub_date=datetime.date.today())
        self.section = Section.objects.create(name='Test Section',
                                              issue=self.issue)
        self.client = APIClient()
        self.posts = {
            'blue': Post(section=self.section,
                         title='Blue headline',
                         url='http://www.agami.com',
                         submitter=User.objects.create(
                             username='Burroughs',
                             is_staff=True)),
            'red': Post(section=self.section,
                        title='Red headline',
                        url='http://www.red.com',
                        submitter=User.objects.create(
                            username='Camus',
                            is_staff=False)),
            'green': Post(section=self.section,
                          title='Green headline',
                          url='http://www.green.com',
                          submitter=User.objects.create(
                              username='DayGlo',
                              is_staff=False))
        }

        for post in self.posts.values():
            post.save()

    def test_create_post(self):
        """Can we create a Post?
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)
        self.client.force_authenticate(user=staff_user)
        url = reverse('bulletin:api:post-list')
        response = self.client.post(url,
                                    self.new_post_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_category(self):
        """Can we associate a Category and a Post?
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)
        self.client.force_authenticate(user=staff_user)
        post = Post(submitter=staff_user,
                    **self.new_post_data)
        post.save()
        category = Category(name='Test Category')
        category.save()
        url = reverse('bulletin:api:post-category-list',
                      kwargs={'pk': post.id})
        response = self.client.post(url,
                                    {'id': category.id,
                                     'name': category.name},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_move_post_up(self):
        """Can we move a post up in an issue?
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)
        self.client.force_authenticate(user=staff_user)
        initial_last_post = self.section.posts.order_by('position').last()

        url = reverse('bulletin:api:section-post-up',
                      kwargs={'section_pk': self.section.id,
                              'post_pk': initial_last_post.id})

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        current_last_post = self.section.posts.order_by('position').last()

        self.assertNotEqual(initial_last_post, current_last_post)

    def test_move_post_down(self):
        """Can we move a post down in an issue?
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)
        self.client.force_authenticate(user=staff_user)
        initial_first_post = self.section.posts.order_by('position').first()

        url = reverse('bulletin:api:section-post-down',
                      kwargs={'section_pk': self.section.id,
                              'post_pk': initial_first_post.id})

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        current_first_post = self.section.posts.order_by('position').first()

        self.assertNotEqual(initial_first_post, current_first_post)


class IssueTests(APITestCase):

    def setUp(self):
        self.issue_data = {
            'pub_date': '2014-01-04',
            'sections': [],
            'name': 'Test Issue {0}'.format(uuid.uuid4()),
            'subject': 'New Issue!',
            'from_name': 'The Editor',
            'from_email': settings.CONSTANT_CONTACT_FROM_EMAIL,
            'reply_to_email': settings.CONSTANT_CONTACT_REPLY_TO_EMAIL,

            'organization_name': 'Test org name',
            'address_line_1': 'Test address line 1',
            'address_line_2': 'Test address line 2',
            'address_line_3': 'Test address line 3',
            'city': 'Test city',
            'state': 'Test state',
            'international_state': 'Test international state',
            'postal_code': 'Test postal code',
            'country': 'FM',

            'html_template_name': 'bulletin/api/test/html_template.html',
            'text_template_name': 'bulletin/api/test/text_template.txt'
        }
        self.newsletter = Newsletter.objects.create(name='Test Newsletter')
        issue_kwargs = self.issue_data
        issue_kwargs.pop('sections')
        self.issue = Issue.objects.create(newsletter=self.newsletter,
                                          **issue_kwargs)
        Site.objects.create()

    def tearDown(self):
        if self.issue.email_marketing_campaign:
            # Deleting this EmailMarketingCampaign should also clean up
            # the one we just created on Constant Contact:
            self.issue.email_marketing_campaign.delete()

    def test_create_issue_in_newsletter(self):
        """Can we create an issue in a newsletter?
        """
        initial_num_issues_in_newsletter = self.newsletter.issues.count()
        url = reverse('bulletin:api:newsletter-issue-list',
                      kwargs={'pk': self.newsletter.id})
        client = APIClient()
        client.force_authenticate(user=User.objects.create(username='staff',
                                                           is_staff=True))

        response = client.post(url, self.issue_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.newsletter.issues.count(),
                         initial_num_issues_in_newsletter + 1)

    def test_create_issue_with_sections_in_newsletter(self):
        """Can we create an issue with sections in a newsletter?
        """
        url = reverse('bulletin:api:newsletter-issue-list',
                      kwargs={'pk': self.newsletter.id})
        client = APIClient()
        client.force_authenticate(user=User.objects.create(username='staff',
                                                           is_staff=True))

        issue_data = self.issue_data
        issue_data['sections'] = [
            {
                'name': 'Pets',
                'posts': []
            },
            {
                'name': 'Auto',
                'posts': []
            }
        ]
        # Set pub_date to something less than self.issue.pub_date so
        # Issue.objects.first() will find return one:
        issue_data['pub_date'] = '2000-10-10'

        response = client.post(url, issue_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        issue = Issue.objects.last()
        self.assertEqual(issue.sections.count(), 2)

    def test_upload_issue(self):
        """Can we upload an Issue to Constant Contact?
        """
        url = reverse('bulletin:api:issue-upload',
                      kwargs={'pk': self.issue.id})
        client = APIClient()
        client.force_authenticate(user=User.objects.create(username='staff',
                                                           is_staff=True))

        response = client.put(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # We have a dirty read.
        self.issue = Issue.objects.get(pk=self.issue.pk)

        self.assertIsNotNone(self.issue.email_marketing_campaign)

    def test_update_uploaded_issue(self):
        """Can we update an email marketing campaign on Constant Contact?
        """
        url = reverse('bulletin:api:issue-upload',
                      kwargs={'pk': self.issue.id})
        client = APIClient()
        client.force_authenticate(user=User.objects.create(username='staff',
                                                           is_staff=True))

        response = client.put(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # We have a dirty read.
        self.issue = Issue.objects.get(pk=self.issue.pk)

        NEW_SUBJECT = 'Billy Has A Big Day'

        self.issue.subject = NEW_SUBJECT
        self.issue.save()

        response = client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['subject'], NEW_SUBJECT)

    def test_delete_uploaded_issue(self):
        """Can we delete an email marketing campaign on Constant Contact?
        """
        url = reverse('bulletin:api:issue-upload',
                      kwargs={'pk': self.issue.id})
        client = APIClient()
        client.force_authenticate(user=User.objects.create(username='staff',
                                                           is_staff=True))

        response = client.put(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # We have a dirty read.
        self.issue = Issue.objects.get(pk=self.issue.pk)
        self.assertIsNotNone(self.issue.email_marketing_campaign)

        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # We have another dirty read.
        self.issue = Issue.objects.get(pk=self.issue.pk)
        self.assertIsNone(self.issue.email_marketing_campaign)

    def test_fill_issue_sorts_correctly(self):
        """When we fill an Issue, are the Posts sorted correctly?
        They should go into Issue Sections based on Post.category
        and content type.
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)

        first_category = Category.objects.create(name='First Test Category')
        second_category = Category.objects.create(name='Second Test Category')

        first_post = Post.objects.create(title='First headline',
                                         url='http://www.first.com',
                                         submitter=staff_user,
                                         approved=True,
                                         include_in_newsletter=True,
                                         category=first_category)

        second_post = Post.objects.create(title='Second headline',
                                          url='http://www.second.com',
                                          submitter=staff_user,
                                          approved=True,
                                          include_in_newsletter=True,
                                          category=second_category)

        post_content_type = ContentType.objects.get(app_label="bulletin",
                                                    name="post")

        section = Section.objects.create(issue=self.issue,
                                         name='First section')
        section.categories.add(first_category)
        section.content_types.add(post_content_type)
        section.save()

        url = reverse('bulletin:api:issue-fill',
                      kwargs={'pk': self.issue.id})
        client = APIClient()
        client.force_authenticate(user=staff_user)

        response = client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(section.posts.first(), first_post)
        self.assertNotIn(second_post, section.posts.all())

    def test_fill_issue(self):
        """Can we fill an Issue with Posts?
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)

        approved_post = Post.objects.create(
            title='Blue headline',
            url='http://www.blue.com',
            submitter=staff_user,
            approved=True,
            include_in_newsletter=True)

        def get_num_issue_posts():
            if self.issue.sections.all():
                num_issue_posts = reduce(operator.add,
                                         [section.posts.count()
                                          for section
                                          in self.issue.sections.all()])
            else:
                num_issue_posts = 0
            return num_issue_posts

        self.assertEqual(0, get_num_issue_posts())

        url = reverse('bulletin:api:issue-fill',
                      kwargs={'pk': self.issue.id})
        client = APIClient()
        client.force_authenticate(user=staff_user)

        response = client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(1, get_num_issue_posts())

        # We've got a dirty read here, so refresh it before checking it:
        approved_post = Post.objects.get(id=approved_post.id)

        self.assertIsNotNone(approved_post.section)


class SectionTests(APITestCase):

    def setUp(self):
        newsletter = Newsletter.objects.create(name='Test Newsletter')
        self.issue = Issue.objects.create(newsletter=newsletter,
                                          pub_date=datetime.date.today())
        self.client = APIClient()
        self.staff_user = User.objects.create(username='staff',
                                              is_staff=True)
        self.client.force_authenticate(user=self.staff_user)

    def test_create_section_in_issue(self):
        """Can we create a section in an issue?
        """
        url = reverse('bulletin:api:issue-section-list',
                      kwargs={'pk': self.issue.id})

        section_json = {
            'name': 'Pets',
            'posts': []
        }

        response = self.client.post(url, section_json, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_in_section(self):
        """Can we create a post inside a section?
        """
        section = Section(issue=self.issue,
                          name='Test Section')
        section.save()
        url = reverse('bulletin:api:section-post-list',
                      kwargs={'pk': section.id})

        post_json = {
            'title': 'Dog Bites Man',
            'url': 'http://api.aashe.org',
            'submitter': {
                'id': 1,
                'username': 'admin'
            }
        }

        response = self.client.post(url, post_json, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_move_section_up(self):
        """Can we move a section up in an issue?
        """
        sports = Section(issue=self.issue,
                         name='Sports')
        sports.save()
        comics = Section(issue=self.issue,
                         name='Comics')
        comics.save()
        news = Section(issue=self.issue,
                       name='News')
        news.save()

        url = reverse('bulletin:api:issue-section-up',
                      kwargs={'issue_pk': self.issue.id,
                              'section_pk': news.id})

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        news = Section.objects.get(pk=news.id)
        self.assertEqual(news.position, 2)

    def test_move_section_down(self):
        """Can we move a section down in an issue?
        """
        sports = Section(issue=self.issue,
                         name='Sports')
        sports.save()
        comics = Section(issue=self.issue,
                         name='Comics')
        comics.save()
        news = Section(issue=self.issue,
                       name='News')
        news.save()

        url = reverse('bulletin:api:issue-section-down',
                      kwargs={'issue_pk': self.issue.id,
                              'section_pk': sports.id})

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sports = Section.objects.get(pk=sports.id)
        self.assertEqual(comics.position, 2)


class SectionTemplateTests(APITestCase):

    def setUp(self):
        newsletter = Newsletter.objects.create(name='Test Newsletter')
        self.issue_template = IssueTemplate.objects.create(
            newsletter=newsletter,
            name='Test Issue Template')
        self.client = APIClient()
        self.staff_user = User.objects.create(username='staff',
                                              is_staff=True)
        self.client.force_authenticate(user=self.staff_user)

    def test_can_list_categories_for_a_section_template(self):
        """Can we list the Categories for a SectionTemplate?
        """
        section_template = SectionTemplate.objects.create(
            issue_template=self.issue_template,
            name='Comics')
        section_template.categories.add(
            Category.objects.create(name='Alley Oop'))
        section_template.save()

        url = reverse('bulletin:api:section-template-category-list',
                      kwargs={'pk': section_template.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AdSizeTests(APITestCase):

    def test_create_ad_size(self):
        """Can we create an AdSize?
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)
        self.client.force_authenticate(user=staff_user)
        url = reverse('bulletin:api:ad-size-list')
        data = {'name': 'Test AdSize',
                'width': 600,
                'height': 300}
        response = self.client.post(url,
                                    data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_ad_size(self):
        """Can we list AdSize objects?
        """
        ad_size = AdSize.objects.create(name='Test AdSize',
                                        width=1,
                                        height=1)

        url = reverse('bulletin:api:ad-size-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(ad_size.name,
                         response.data[0]['name'])


class AdTests(APITestCase):

    def test_create_ad(self):
        """Can we create an Ad?
        """
        staff_user = User.objects.create(username='staff',
                                         is_staff=True)
        self.client.force_authenticate(user=staff_user)

        url = reverse('bulletin:api:ad-list')

        ad_size = AdSize.objects.create(name='Test AdSize', width=1, height=1)

        data = {'name': 'Test Ad',
                'start': datetime.date.today(),
                'end': datetime.date.today(),
                'size': ad_size.pk,
                'url': 'http://www.aashe.org'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_ad(self):
        """Can we list Ad objects?
        """
        ad_size = AdSize.objects.create(name='Test AdSize', width=1, height=1)

        ad = Ad.objects.create(name='Test Ad',
                               start=datetime.date.today(),
                               end=datetime.date.today(),
                               size=ad_size,
                               url='http://www.aashe.org')

        url = reverse('bulletin:api:ad-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(ad.name,
                         response.data[0]['name'])
