import json

from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.http.response import JsonResponse
from django.utils.crypto import get_random_string
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser

from .permissions import UserPermision
from .serializers import UserSerializer


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
        if user.role != 'admin':
            role = user.role
        serializer = UserSerializer(user)
        if serializer.is_valid(raise_exception=True):
            serializer.save(role=role)
            return Response(serializer.data)

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


def get_tokens_for_user(request):
    email = ''
    if request.content_type == 'multipart/form-data':
        email = request.POST.get('email')
        confirmation_code = request.POST.get('confirmation_code')
    elif request.content_type == 'application/json':
        body = json.loads(request.body.decode('utf-8'))
        email = body.get('email')
        confirmation_code = body.get('confirmation_code')
    user = get_object_or_404(CustomUser, email=email)
    data = {'answer': 'confirmation_code is not valid'}
    status = 400
    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        status = 200
    return JsonResponse(data=data, status=status)


def get_confirm_code(request):
    email = ''
    if request.content_type == 'multipart/form-data':
        email = request.POST.get('email')
    elif request.content_type == 'application/json':
        body = json.loads(request.body.decode('utf-8'))
        email = body.get('email')
    try:
        EmailValidator()(email)
    except Exception as message:
        return JsonResponse(
            data={'error': str(message)}, status=400
        )
    conf_code = get_random_string(length=32)
    queryset = CustomUser.objects.filter(email=email)
    if queryset.count():
        user = queryset.first()
    else:
        user = CustomUser(email=email, username=email, role='user')
    user.confirmation_code = conf_code
    user.save()
    send_mail(
        'Yamdb confirmation_code',
        f'Yamdb confirmation code : {conf_code}',
        'Yamdb',
        [f'{email}'],
        fail_silently=False,
    )
    return JsonResponse(
        data={'email': email}
    )
