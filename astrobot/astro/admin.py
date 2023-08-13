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
    ]
    list_display = [
        'title',
        'updated_at',
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
        "Username",
        "Total Points",
    ]
    list_display = [
        "Username",
        "Total Points",
        'updated_at',
    ]