from django_filters import rest_framework as filters

from client.models import Member


class MemberFilter(filters.FilterSet):
    distance = filters.RangeFilter()

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'gender', 'distance')
