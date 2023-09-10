from django.contrib import admin

from . import models


class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = [
        'answer',
        'is_correct'
    ]

# Register your models here.
@admin.register(models.Question)


class QuestionAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'points',
        'difficulty',
        'optional_image',
    ]
    list_display = [
        'title',
        'updated_at',
        'optional_image',
    ]
    inlines = [
        AnswerInlineModel,
    ]
    
@admin.register(models.Answer)

class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'answer',
        'is_correct',
        'question'
    ]
@admin.register(models.Qusers)
class QusersAdmin(admin.ModelAdmin):
    fields = [
        "username",
        "totalpoints",
    ]
    list_display = [
        "username",
        "totalpoints",
        'updated_at',
    ]