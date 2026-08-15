from django.contrib import admin

from . import models

admin.site.site_header = "AstroBot administration"
admin.site.site_title = "AstroBot admin"
admin.site.index_title = "Trivia data"


class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = ["answer", "is_correct"]
    # the discord view renders four answer buttons
    extra = 4


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = [
        "title",
        "points",
        "difficulty",
        "is_active",
    ]
    list_display = [
        "title",
        "difficulty",
        "points",
        "is_active",
        "updated_at",
    ]
    list_filter = ["difficulty", "is_active"]
    search_fields = ["title"]
    inlines = [AnswerInlineModel]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["answer", "is_correct", "question"]
    list_filter = ["is_correct"]
    search_fields = ["answer", "question__title"]


@admin.register(models.Qusers)
class QusersAdmin(admin.ModelAdmin):
    fields = ["username", "totalpoints"]
    list_display = ["username", "totalpoints", "updated_at"]
    search_fields = ["username"]
