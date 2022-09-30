from django.contrib import admin

from .models import (UserProfile,
                     Post,
                     Reaction,
                     Friendship,
                     Follow)

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Friendship)
admin.site.register(Follow)
