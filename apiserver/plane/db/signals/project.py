from django.db.models.signals import post_save
from django.dispatch import receiver

from plane.api.permissions.workspace import Owner, Admin
from plane.db.models import Project, User, ProjectMember


@receiver(post_save, sender=Project)
def add_admin_and_owner_to_project(sender, instance: Project, created, **kwargs):
    workspace = instance.workspace
    if created:
        admin_and_owner_users = User.objects.filter(
            member_workspace__workspace=workspace,
            member_workspace__role__in=[Admin, Owner]
        )
        for user in admin_and_owner_users:
            ProjectMember.objects.create(project=instance,
                                         member=user,
                                         role=user.workspace_member.get(workspace=workspace).role)
