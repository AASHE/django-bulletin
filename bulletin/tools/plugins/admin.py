from django.contrib import admin

from .models import (Job,
                     NewResource,
                     Story,
                     Opportunity)

for model in (Job,
              NewResource,
              Story,
              Opportunity):
    admin.site.register(model)
