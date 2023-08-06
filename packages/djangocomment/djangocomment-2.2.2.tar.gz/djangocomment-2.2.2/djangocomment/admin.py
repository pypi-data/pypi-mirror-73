from django.contrib import admin
from djangocomment.models import CommentModel
from djangocomment.modeladmins import CommentModelAdmin


# Register your models here.
admin.site.register(CommentModel, CommentModelAdmin)
