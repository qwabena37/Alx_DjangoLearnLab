# Django Permissions & Groups Setup

## Custom Permissions (models.py)
Custom permissions defined in the Article model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
Groups created and configured in Django Admin:
- Viewers → can_view
- Editors → can_view, can_create, can_edit
- Admins → all permissions

## Views
Each protected view uses @permission_required to enforce access:
- article_list → can_view
- article_create → can_create
- article_edit → can_edit
- article_delete → can_delete

## Testing
Create test users and assign them to the groups.
Verify that only allowed actions succeed.

