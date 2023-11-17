from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.validators import ValidationError

from .models import Server,  Channel, Category
from .serializers import ServerSerializer


class ServerListViewSet(ViewSet):
    authentication_classes = [SessionAuthentication]
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get('category')
        quantity = request.query_params.get('quantity')

        by_user = request.query_params.get('by_user') == 'true'
        by_server_id = request.query_params.get('by_server_id')

        if by_user or by_server_id and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if quantity:
            self.queryset = self.queryset[: int(quantity)]

        if by_server_id:
            try:
                self.queryset = self.queryset.filter(id=by_server_id)
                if not self.queryset.exists():
                    raise ValidationError(detail=f'Сервер с идентификатором {by_server_id} не найден!')
            except ValueError:
                raise ValidationError(detail=f'Ошибка значения сервера!')

        serializer = ServerSerializer(self.queryset, many=True)
        return Response(serializer.data)
