from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.functions.getScore import getScore
from api.serializers import ChangePasswordSerializer, CharmSerializer, ChatRoomsSerializer, ChatSerializer, EventSerializer, FaqSerializer, NoticeSerializer, ReviewSerializer, UserSerializer
from api.models import Charm, ChatRoom, Chats, Event, Faq, Notice, Review, User
from validate_email_address import validate_email_or_fail
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
import base64
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from django.core.files.base import ContentFile
from dateutil.parser import parse
from rest_framework import filters


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        photoUrl = request.data['photoUrl']
        email = request.data['email']
        format, imgstr = photoUrl.split(';base64,')
        ext = format.split('/')[-1]
        print(request.data['birthday'])
        birthday = request.data['birthday']
        birthday = parse(birthday)
        data['birthday'] = birthday
        photoUrl = ContentFile(base64.b64decode(
            imgstr), name='{}.'.format(email) + ext)
        data['photoUrl'] = photoUrl

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        userInfo = serializer.data
        try:
            token = Token.objects.get(user_id=userInfo['id'])
        except Token.DoesNotExist:
            token = Token.objects.create(user=userInfo)

        response = Response()
        response.data = {
            'message': "success",
            'token': token.key,
            'userInfo': userInfo
        }

        return response


class ValidateEmailView(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        user = User.objects.get(email=email)
        if user is None:
            raise AuthenticationFailed('User not found!')
        try:
            token = Token.objects.get(user_id=user.id)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        response = Response()
        response.data = {
            'message': "success",
            'token': token.key
        }

        return response


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        user = User.objects.get(email=request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        data = request.data
        try:
            photoUrl = request.data['photoUrl']
            email = request.user
            format, imgstr = photoUrl.split(';base64,')
            ext = format.split('/')[-1]
            photoUrl = ContentFile(base64.b64decode(
                imgstr), name='{}.'.format(email) + ext)
            data['photoUrl'] = photoUrl
        except:
            pass
        user_id = request.user.id
        user_object = User.objects.get(id=user_id)
        update_user_serializer = UserSerializer(
            user_object, data=data)
        update_user_serializer.is_valid(raise_exception=True)

        if update_user_serializer.is_valid():
            update_user_serializer.save()
            return Response(update_user_serializer.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_204_NO_CONTENT)

    def delete(self, request):
        user = request.user
        user_object = User.objects.get(email=user)
        user_object.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class OneUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, userId):
        try:
            user = User.objects.get(id=userId)
            serializer = UserSerializer(user)

            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class UsersBySex(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        myInfo = request.user.whoAmIScore
        myIdeal = request.user.myIdealsScore
        myHobby = request.user.myHobbiesScore
        skipUser = request.user.skipUser
        if(request.user.sex == "male"):
            users = User.objects.filter(
                sex="female", university=request.user.university)
            response_data = []
            for user in users:
                userInfo = user.whoAmIScore
                userIdeal = user.myIdealsScore
                userHobby = user.myHobbiesScore
                score = getScore(myInfo, myIdeal, myHobby,
                                 userInfo, userIdeal, userHobby)
                serializer = UserSerializer(user)
                if(user.id not in skipUser and user.is_admin != True):
                    response_data.append(
                        {'data': serializer.data, 'orderKey': score})
            sorted_data = sorted(
                response_data, key=lambda d: d['orderKey'])
            # print(sorted_data)
            return Response(sorted_data)
        else:
            users = User.objects.filter(
                sex="male", university=request.user.university)
            response_data = []
            for user in users:
                userInfo = user.whoAmIScore
                userIdeal = user.myIdealsScore
                userHobby = user.myHobbiesScore
                score = getScore(myInfo, myIdeal, myHobby,
                                 userInfo, userIdeal, userHobby)
                serializer = UserSerializer(user)
                if(user.id not in skipUser and user.is_admin != True):
                    response_data.append(
                        {'data': serializer.data, 'orderKey': score})
            sorted_data = sorted(
                response_data, key=lambda d: d['orderKey'])
            return Response(sorted_data)


class EmailChecker(APIView):
    def post(self, request):
        email = request.data['email']
        try:
            isvalid = validate_email_or_fail(email, verify=True)
        except Exception as e:
            print(e)
        if(isvalid):
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_204_NO_CONTENT)


class AddUserChatRoomView(APIView):
    def post(self, request):
        chatRoomId = request.data['chatRoomId']
        participants = request.data['participants']
        response = []
        try:
            for participant in participants:
                user_object = User.objects.get(id=participant)
                chatRoomsList = list(user_object.chatRooms)
                if(chatRoomId not in chatRoomsList):
                    chatRoomsList.append(chatRoomId)
                user_serializer = UserSerializer(
                    user_object, data={'chatRooms': chatRoomsList})
                if(user_serializer.is_valid()):
                    user_serializer.save()
                    response.append(user_serializer.data)
                else:
                    print(user_serializer.error_messages)
                    return Response()
            return Response(response)

        except Exception as e:
            return Response()


class NoticeViewSet(ModelViewSet):
    queryset = Notice.objects.all().order_by('-createdAt')
    serializer_class = NoticeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class FaqViewSet(ModelViewSet):
    queryset = Faq.objects.all().order_by('-createdAt')
    serializer_class = FaqSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomsSerializer

    def create(self, request):

        chatroom_serializer = ChatRoomsSerializer(data=request.data)
        chatroom_serializer.is_valid(raise_exception=True)
        chatroom_serializer.save()

        participants = request.data['participants']

        user_object = User.objects.get(id=participants[0])
        temp_skipUser = list(user_object.skipUser)
        temp_skipUser.append(participants[1])
        user_serializer = UserSerializer(
            user_object, data={'skipUser': temp_skipUser})
        user_serializer.is_valid()
        user_serializer.save()

        user_object = User.objects.get(id=participants[1])
        temp_skipUser = list(user_object.skipUser)
        temp_skipUser.append(participants[0])
        user_serializer = UserSerializer(
            user_object, data={'skipUser': temp_skipUser})
        user_serializer.is_valid()
        user_serializer.save()

        return Response(chatroom_serializer.data)


class ChatViewSet(ModelViewSet):
    queryset = Chats.objects.all()
    serializer_class = ChatSerializer


class CharmViewSet(ModelViewSet):
    queryset = Charm.objects.all().order_by('-createdAt')
    serializer_class = CharmSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all().order_by('-createdAt')
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all().order_by('-createdAt')
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
