# Authentication:
# Users obtain tokens by POSTing username/password to /api-token-auth/
# All CRUD operations on BookViewSet require token authentication.
#
# Permissions:
# BookViewSet uses IsAuthenticated to restrict access.
