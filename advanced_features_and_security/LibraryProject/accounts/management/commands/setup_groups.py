from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        permissions = Permission.objects.filter(codename__in=[
            "can_view", "can_create", "can_edit", "can_delete"
        ])

        # Create groups
        viewers, _ = Group.objects.get_or_create(name="Viewers")
        editors, _ = Group.objects.get_or_create(name="Editors")
        admins, _ = Group.objects.get_or_create(name="Admins")

        # Assign permissions
        viewers.permissions.set(permissions.filter(codename="can_view"))
        editors.permissions.set(permissions.filter(codename__in=["can_view", "can_create", "can_edit"]))
        admins.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Groups and permissions configured."))
