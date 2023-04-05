#serializers que sirven para dar salida a datos en la rest
#en esta app no hay modelos
from rest_framework import serializers
from cuentas.models import Account


class AccountSerializer(serializers.ModelSerializer):
    have_transactions = serializers.SerializerMethodField(read_only=True)

    def get_have_transactions(self,obj):
        return obj.total_transactions()>0

    class Meta:
        model = Account
        fields = ["pk","name","user","balance","type_account","order","status","created","comments","have_transactions"] 
        read_only_fields = ["have_transactions"]

