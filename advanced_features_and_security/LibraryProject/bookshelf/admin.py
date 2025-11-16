# bookshelf/admin.py
from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # columns shown in the list page
    list_display = ("title", "author", "publication_year")

    # quick filters in the right sidebar
    list_filter = ("publication_year", "author")

    # search box - searches these fields (partial matches)
    search_fields = ("title", "author")

    # make title the clickable link to the change page
    list_display_links = ("title",)

    # allow inline editing of publication_year in the list view
    # (note: list_editable cannot include the same field as list_display_links)
    list_editable = ("publication_year",)

    # optional conveniences
    ordering = ("title",)
    list_per_page = 20


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Show custom fields in admin detail view
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': (
                'date_of_birth',
                'profile_photo',
            )
        }),
    )

    # Show custom fields when creating a new user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': (
                'date_of_birth',
                'profile_photo',
            )
        }),
    )


# THIS IS THE REQUIRED LINE
admin.site.register(CustomUser, CustomUserAdmin)
