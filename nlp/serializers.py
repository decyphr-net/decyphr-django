from rest_framework.serializers import CharField, ModelSerializer
from rest_framework.serializers import Serializer as DRFSerializer

from nlp.models import TextPiece


class Deserializer(DRFSerializer):
    text_to_be_processed = CharField(required=True)
    language_code = CharField(required=False)
    processor = CharField(required=False)


class Serializer(ModelSerializer):
    class Meta:
        model = TextPiece
        fields = "__all__"
