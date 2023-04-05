
from rest_framework import viewsets, permissions
from cuentas.models import Account
from .serializers import AccountSerializer

class AccountVisiblesViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'options', 'head','put','patch']

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user,status="visible").order_by("order", "-pk")
