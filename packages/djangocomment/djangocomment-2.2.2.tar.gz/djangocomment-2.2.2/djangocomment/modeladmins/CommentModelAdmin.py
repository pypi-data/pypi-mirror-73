from django import forms
from django.db import models
from django.contrib.admin import ModelAdmin


class CommentModelAdmin(ModelAdmin):
    list_display        = ["content_type", "object_id", "pk", "author", "status"]
    list_filter         = ["created_at", "updated_at", "status"]

    formfield_overrides = {
        models.PositiveIntegerField: {'widget': forms.NumberInput(attrs={"size": 20})},
        models.TextField: {'widget': forms.Textarea(attrs={'cols': 50, 'rows': 5})}

    }

    fieldsets           = (
        ("Content object", {
            "classes": ["extrapretty", "collapse"],
            "fields": ["content_type", "object_id"]
        }),
        ("Content", {
            "classes": ["extrapretty"],
            "fields": ["parent", "content"]
        }),
        ("Status", {
            "classes": ["extrapretty", "collapse"],
            "fields": ["author", "status"]
        })
    )