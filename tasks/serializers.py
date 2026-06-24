from rest_framework import serializers
from .models import Task
from accounts.models import User
from .models import Notification

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):

    created_by_name = serializers.CharField(source="created_by.username",read_only=True)
    assigned_to_names = serializers.SerializerMethodField()
    assigned_to = serializers.PrimaryKeyRelatedField(many=True,queryset=User.objects.all(),required=False)
    created_by_id = serializers.IntegerField(source="created_by.id",read_only=True)

    def get_assigned_to_names(self, obj):
        return [user.username for user in obj.assigned_to.all()]

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "created_by",
            "created_by_id",
            "created_by_name",
            "assigned_to",
            "assigned_to_names",
            "attachment",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
            "submission",
        ]
    
    def update(self, instance, validated_data):
            request = self.context["request"]
            user = request.user

            submission_file = request.FILES.get("submission")
            # EMPLOYEE
            if user.role == "employee":
                instance.status = validated_data.get("status", instance.status)

                if submission_file:
                    instance.submission = submission_file

                instance.save()
                return instance

            # MANAGER
            if user.role == "manager":
                if submission_file:
                    instance.submission = submission_file

                return super().update(instance, validated_data)

            return super().update(instance, validated_data)



# Notifiction Serializer
class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = "__all__"



