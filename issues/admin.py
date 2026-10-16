from django.contrib import admin

from .models import Comment, Report


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ["created_at"]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "district",
        "status",
        "votes",
        "created_at",
    ]
    list_filter = ["category", "district", "status"]
    search_fields = ["title", "description", "reporter_name"]
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["report", "author_name", "text", "created_at"]
    search_fields = ["text", "author_name"]
