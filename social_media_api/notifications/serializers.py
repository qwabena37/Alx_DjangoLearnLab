from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    actor_id = serializers.ReadOnlyField(source='actor.id')
    recipient = serializers.ReadOnlyField(source='recipient.username')
    recipient_id = serializers.ReadOnlyField(source='recipient.id')
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_id', 'actor', 'actor_id',
            'verb', 'target', 'unread', 'timestamp'
        ]
        read_only_fields = fields

    def get_target(self, obj):
        """
        Provide a simple representation of the target:
        return object id and model name when possible.
        """
        if obj.target:
            return {
                'id': getattr(obj.target, 'id', None),
                'repr': str(obj.target),
                'type': obj.target.__class__.__name__
            }
        return None
