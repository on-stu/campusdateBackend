from django.urls import path, include
from .views import AddUserChatRoomView, ChangePasswordView, CharmViewSet, ChatRoomViewSet, ChatViewSet, EmailChecker, EventViewSet, FaqViewSet, LoginView, NoticeViewSet, OneUser, ReadChatView, RegisterView, ReviewViewSet, UserView, UsersBySex, ValidateEmailView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('notice', NoticeViewSet)
router.register('faq', FaqViewSet)
router.register('chatroom', ChatRoomViewSet)
router.register('chat', ChatViewSet)
router.register('charm', CharmViewSet)
router.register('review', ReviewViewSet)
router.register('event', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('emailchecker/', EmailChecker.as_view()),
    path('emailvalidate/', ValidateEmailView.as_view()),
    path('user/', UserView.as_view()),
    path('usersbysex/', UsersBySex.as_view()),
    path('user/<int:userId>/', OneUser.as_view()),
    path('addChat/', AddUserChatRoomView.as_view()),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(),
         name='auth_change_password'),
    path('readchat/', ReadChatView.as_view())

]
