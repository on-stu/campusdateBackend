from django.contrib import admin
from .models import Charm, ChatRoom, Chats, Event, Faq, Notice, Report, Review, User
# Register your models here.

admin.site.register(User)
admin.site.register(Notice)
admin.site.register(Faq)
admin.site.register(ChatRoom)
admin.site.register(Chats)
admin.site.register(Charm)
admin.site.register(Review)
admin.site.register(Event)
admin.site.register(Report)
