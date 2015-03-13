from django.contrib import admin

from .models import (Category,
                     Issue,
                     IssueTemplate,
                     Link,
                     Newsletter,
                     Post,
                     Section,
                     SectionTemplate)


for model in (Category,
              Issue,
              IssueTemplate,
              Link,
              Newsletter,
              Post,
              Section,
              SectionTemplate):
    admin.site.register(model)
