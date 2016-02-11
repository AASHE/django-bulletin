from datetimewidget.widgets import DateWidget
from django.forms import (BooleanField,
                          EmailField,
                          EmailInput,
                          Form,
                          ModelChoiceField,
                          ModelForm,
                          ModelMultipleChoiceField)
from django.forms.widgets import HiddenInput, SelectMultiple
from form_utils.widgets import ImageWidget

from .models import (Category,
                     Issue,
                     IssueTemplate,
                     Link,
                     Newsletter,
                     Section,
                     SectionTemplate,
                     Post,
                     Ad)


class NewsletterForm(ModelForm):

    class Meta:
        model = Newsletter
        fields = ['name',
                  'mailing_list']


class NewsletterSubscribeForm(Form):
    email_address = EmailField(
        label='',
        error_messages={'required': 'Please enter your email address',
                        'invalid': 'Please enter a valid email address'},
        widget=EmailInput(attrs={'class': 'form-control'}))


class IssueCreateForm(ModelForm):
    issue_template = ModelChoiceField(queryset=IssueTemplate.objects.all(),
                                      required=False)

    class Meta:
        model = Issue
        fields = ['name', 'pub_date', 'issue_template']
        widgets = {
            'pub_date': DateWidget(usel10n=True, bootstrap_version=3)
        }


class IssueSettingsForm(ModelForm):

    class Meta:
        model = Issue
        fields = [
            'name',
            'pub_date',
            'subject',
            'introduction',
            'from_name',
            'from_email',
            'reply_to_email',
            'organization_name',
            'address_line_1',
            'address_line_2',
            'address_line_3',
            'city',
            'state',
            'international_state',
            'postal_code',
            'country',
            'html_template_name',
            'text_template_name'
        ]


class IssueUploadForm(Form):
    pass


class SectionForm(ModelForm):

    class Meta:
        model = Section
        fields = ['name']


class SectionPostForm(ModelForm):

    available_posts = ModelMultipleChoiceField(
        queryset=Post.available_for_newsletter())

    class Meta:
        model = Section
        fields = ['available_posts', 'position']
        widgets = {'position': HiddenInput()}


class SectionPostRemoveForm(ModelForm):

    confirmation = BooleanField(label="Remove from section?")

    class Meta:
        model = Section
        fields = ['confirmation']


class IssueDeleteForm(ModelForm):

    class Meta:
        model = Issue
        exclude = ['id']


class SectionDeleteForm(ModelForm):

    class Meta:
        model = Section
        exclude = ['id']


class PostSubmitForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title',
                  'url',
                  'categories']

    def __init__(self, *args, **kwargs):
        super(PostSubmitForm, self).__init__(*args, **kwargs)
        # Don't show categories, only subcategories:
        self.fields['categories'].queryset = Category.objects.exclude(
            parent=None).exclude(private=True).order_by('name')


class PostUpdateForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title',
                  'url',
                  'approved',
                  'pub_date',
                  'include_in_newsletter',
                  'feature',
                  'categories']
        widgets = {
            'pub_date': DateWidget(usel10n=True, bootstrap_version=3),
            'categories': SelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        # Don't show categories, only subcategories:
        self.fields['categories'].queryset = Category.objects.exclude(
            parent=None).exclude(private=True).order_by('name')


class LinkForm(ModelForm):

    class Meta:
        model = Link
        fields = ['text',
                  'url']


class IssueTemplateForm(ModelForm):

    class Meta:
        model = IssueTemplate
        fields = ['name']


class IssueTemplateUpdateSettingsForm(ModelForm):

    class Meta:
        model = IssueTemplate
        fields = [
            'subject',
            'from_name',
            'from_email',
            'reply_to_email',
            'organization_name',
            'address_line_1',
            'address_line_2',
            'address_line_3',
            'city',
            'state',
            'international_state',
            'postal_code',
            'country',
            'html_template_name',
            'text_template_name'
        ]


class IssueTemplateDeleteForm(ModelForm):
    confirmation = BooleanField(label="Remove from section?")

    class Meta:
        model = IssueTemplate
        fields = ['confirmation']


class SectionTemplateForm(ModelForm):

    class Meta:
        model = SectionTemplate
        fields = ['name', 'position']
        widgets = {'position': HiddenInput()}


class SectionTemplateDeleteForm(ModelForm):

    class Meta:
        model = SectionTemplate
        exclude = ['id']


class SectionTemplateCategoryAddForm(ModelForm):

    unsectioned_categories = ModelMultipleChoiceField(
        queryset=Category.objects.filter(section_templates=None))

    class Meta:
        model = Category
        fields = ['unsectioned_categories']


class SectionTemplateCategoryRemoveForm(ModelForm):

    confirmation = BooleanField(label="Remove from section?")

    class Meta:
        model = SectionTemplate
        fields = ['confirmation']


class AdCreateForm(ModelForm):

    class Meta:
        model = Ad
        widgets = {
            'start': DateWidget(usel10n=True, bootstrap_version=3),
            'end': DateWidget(usel10n=True, bootstrap_version=3),
            'image': ImageWidget()
        }
        exclude = ['id']


class AdUpdateForm(ModelForm):

    class Meta:
        model = Ad
        widgets = {
            'start': DateWidget(usel10n=True, bootstrap_version=3),
            'end': DateWidget(usel10n=True, bootstrap_version=3),
            'image': ImageWidget()
        }
        exclude = ['id']


class AdDeleteForm(ModelForm):

    class Meta:
        model = Ad
        exclude = ['id']
