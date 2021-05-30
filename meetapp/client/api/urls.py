from django.urls import path

from client.api.views import CreateMemberView, MembersViewSet, MatchCreateView

urlpatterns = [
    path('clients/create/', CreateMemberView.as_view()),
    path('list/', MembersViewSet.as_view({'get': 'list'})),
    path('clients/<int:pk>/match/', MatchCreateView.as_view()),
]
