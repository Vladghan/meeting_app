from django.core import mail

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView

from meetapp.settings import EMAIL_HOST_USER
from .models import Member
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from .serializers import MemberSerializer, MemberListSerializer, MatchCreateSerializer
from .service import MemberFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import ACos, Sin, Cos, Abs, Radians
from django.db.models import F


class CreateMemberView(CreateAPIView):
    model = Member
    permission_classes = [
        AllowAny  # Or anon users can't register
    ]
    serializer_class = MemberSerializer


class MembersViewSet(ModelViewSet):
    serializer_class = MemberListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MemberFilter
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        members = Member.objects.all().annotate(
            distance=6371.009 * ACos(
                Sin(Radians(Abs(self.request.user.lat))) * Sin(Radians(Abs(F('lat')))) +
                Cos(Radians(Abs(self.request.user.lat))) * Cos(Radians(Abs(F('lat')))) *
                Cos(Abs(Radians(self.request.user.long) - Radians(F('long')))))).order_by('id')
        return members

    def get_serializer_class(self):
        if self.action == 'list':
            return MemberListSerializer


class MatchCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        owner = Member.objects.get(id=pk)
        you = request.user
        serializer = MatchCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner, partners=you)

            if request.data['like']:
                if owner.pk in you.match_owner.values_list('partners', flat=True):
                    if you.match_owner.get(partners=owner).like:
                        connection = mail.get_connection()
                        connection.open()
                        messages = []
                        for user in [(you, owner), (owner, you)]:
                            email_subject = 'У Вас взаимная симпатия'
                            email_body = f'Вы понравились {user[0].first_name}! Почта участника: {user[0].email}'
                            email = mail.EmailMessage(
                                email_subject,
                                email_body,
                                EMAIL_HOST_USER,
                                [user[1].email],
                            )
                            messages.append(email)
                        connection.send_messages(messages)
                        connection.close()

            return Response(status=201)
        else:
            return Response(status=400)
