from rest_framework import serializers

from client.models import Member
from client.api.models import Match


class MemberSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(allow_null=True)

    class Meta:
        model = Member
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'gender', 'photo')
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class MemberListSerializer(serializers.ModelSerializer):
    distance = serializers.DecimalField(max_digits=6, decimal_places=1, read_only=True)

    class Meta:
        model = Member
        fields = ('id', 'first_name', 'last_name', 'gender', 'email', 'long', 'lat', 'distance')


class MatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'
        read_only_fields = ('owner', 'partners')

    def create(self, validated_data):
        match = Match.objects.update_or_create(
            owner=validated_data.get('owner', None),
            partners=validated_data.get('partners', None),
            defaults={'like': validated_data.get('like')}
        )
        return match
