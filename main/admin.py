from django.contrib import admin

from .models import *


class CodeImageInLine(admin.TabularInline):
    model = CodeImage
    max_num = 10


# class StarInline(admin.TabularInline):
#     model = Star
#     max_num = 1


# @admin.register(Project)
# class PostAdmin(admin.ModelAdmin):
#     inlines = [CodeImageInLine, StarInline, ]


admin.site.register(Feedback)

