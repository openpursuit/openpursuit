from django.contrib import admin
from djangoOp.op.models import *

class QuizAdmin(admin.ModelAdmin):
    list_display = ("question", "author", "upper_case_name", "date")
#    prepopulated_fields = {"slug": ("title",)}
    def upper_case_name(self, obj):
         return ("%s %s" % (obj.author.first_name, obj.author.last_name))
    upper_case_name.short_description = 'Name'

admin.site.register(Quiz, QuizAdmin)
admin.site.register(FBProfile)
admin.site.register(TagsScore)
admin.site.register(Tags)
admin.site.register(QuizCollection)
admin.site.register(FBChallenge)
#class Admin:
#                date_hierarchy = 'date'
#                list_display = ('question', 'author')
#                list_filter = ('author','date')
#                pass

