from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notification.objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.recipient != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        notification.unread = False
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
