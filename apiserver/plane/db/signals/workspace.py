from django.db.models.signals import post_save
from django.dispatch import receiver

from plane.api.permissions.project import Member
from plane.api.permissions.workspace import Owner, Admin
from plane.db.models import WorkspaceMember, Project, ProjectMember


@receiver(post_save, sender=WorkspaceMember)
def add_admin_and_owner_to_projects(sender, instance: WorkspaceMember, created, **kwargs):
    # Check if the new member is admin or owner or if the role of existing
    # user has been modified to owner or admin
    if instance.role in [Admin, Owner]:
        projects_in_workspace = Project.objects.filter(workspace=instance.workspace)
        for project in projects_in_workspace:
            ProjectMember.objects.update_or_create(project=project,
                                                   member=instance.member,
                                                   role=instance.role)
