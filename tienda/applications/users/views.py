from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import auth
from rest_framework import status

from applications.users.models import User
from applications.users.serializer import LoginSocialSerializer


# Create your views here.
# Use api view
# desencriptar token
# metodo initial carga algo cuando el serialziador se carga
class LoginView(APIView):
    serializer_class = LoginSocialSerializer

    def post(self, request):
        # serializamos la data enviada por el usuario
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # token = serializer.validated_data['token']
        token = serializer.data.get('token')

        decoded_token = auth.verify_id_token(token)

        email = decoded_token['email']
        name = decoded_token['name']
        avatar = decoded_token['picture']
        verified = decoded_token['email_verified']

        user, created = User.objects.get_or_create(
                email = email,
                defaults= {
                    'full_name': name,
                    'email': email,
                    'is_active': True
                }
        )

        if created:
            token = Token.objects.create(user=user)

        token = Token.objects.get(user=user)

        userReponse = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            # 'email': user.email,
            'is_active': user.is_active,
            # 'verified': verified,

        }

        return Response({
            'user': userReponse,
            'token': token.key,
        })


