from rest_framework.serializers import ModelSerializer

from preferences.models import Preferences


class PreferencesSerializer(ModelSerializer):
    class Meta:
        model = Preferences
        fields = "__all__"
