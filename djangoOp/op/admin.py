from django.contrib import admin
from djangoOp.op.models import *

class QuizAdmin(admin.ModelAdmin):
    list_display = ("question", "author")
#    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Quiz, QuizAdmin)
admin.site.register(FBProfile)
admin.site.register(TagsScore)
admin.site.register(Tags)
#class Admin:
#                date_hierarchy = 'date'
#                list_display = ('question', 'author')
#                list_filter = ('author','date')
#                pass

