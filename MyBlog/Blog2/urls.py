from django.conf.urls import url

import Blog2

from Blog2 import views

urlpatterns = [
    url(r"^$", Blog2.views.post_list, name='list'),
    url(r"^create/$", Blog2.views.post_create),
    url(r"^(?P<slug>[\w-]+)/$", Blog2.views.post_detail, name="detail"),
    url(r"^(?P<slug>[\w-]+)/edit$", Blog2.views.post_update, name="update"),
    url(r"^(?P<slug>[\w-]+)/delete/$", Blog2.views.post_delete),
]