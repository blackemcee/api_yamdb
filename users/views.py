from django.conf import settings
from django.core.mail import send_mail
from django.http.response import JsonResponse
from django.utils.crypto import get_random_string
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings as config
from users.models import CustomUser
from .permissions import UserPermision
from .serializers import EmailSerializer, TokenSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (UserPermision,)
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    queryset = CustomUser.objects.all()
    search_fields = ('username',)
    lookup_field = 'username'

    def preform_update(self, request, username=None):
        if username == 'me':
            username = request.user.username
        user = get_object_or_404(CustomUser, username=username)
        if not user.is_admin:
            role = user.role
        self.serializer.save(role=role)
        return Response(self.serializer.data)

    def destroy(self, request, username=None):
        if self.kwargs.get('username') == 'me':
            response = {'message': 'Delete function is not offered.'}
            return Response(response, status=405)
        instance = self.get_object()
        instance.delete()
        return Response(status=204)

    def get_object(self):
        username = self.kwargs.get('username')
        if username == 'me':
            username = self.request.user.username
        user = get_object_or_404(CustomUser, username=username)
        self.check_object_permissions(self.request, user)
        return user


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirm_code(request):
    serializer = EmailSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(
            data=serializer.errors, status=400
        )
    email = serializer.validated_data.get('email')
    conf_code = get_random_string(length=32)
    queryset = CustomUser.objects.filter(email=email)
    if queryset.exists():
        user = queryset.first()
    else:
        user = CustomUser(email=email, username=email, role=config.USER_ROLE)
    user.confirmation_code = conf_code
    user.save()
    send_mail(
        subject='Yamdb confirmation_code',
        message=f'Yamdb confirmation code : {conf_code}',
        from_email=f'{settings.ADMIN_EMAIL}',
        recipient_list=[f'{email}'],
        fail_silently=False,
    )
    return JsonResponse(serializer.validated_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(
            data=serializer.errors, status=400
        )
    user = serializer.validated_data
    refresh = RefreshToken.for_user(user)
    data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    status = 200
    return JsonResponse(data=data, status=status)
