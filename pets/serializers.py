from rest_framework import serializers
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer
from pets.models import PetGenre


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=PetGenre.choices,
        default=PetGenre.NOT_INFORMED
        )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
