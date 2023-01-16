from rest_framework import serializers
from .models import MoneyBook, MoneyBookLog


class MoneyBookSerializer(serializers.ModelSerializer):
    """
    model: MoneyBook
    LIST 사용
    """

    class Meta:
        model = MoneyBook
        fields = ["cash_amount"]


class MoneyBookLogSerializer(serializers.ModelSerializer):
    """
    model: MoneyBookLog
    CREATE, RETRIEVE 사용
    """

    class Meta:
        model = MoneyBookLog
        fields = "__all__"


class MoneyBookLogListSerializer(serializers.ModelSerializer):
    """
    model: MoneyBookLog
    LIST 사용
    """

    class Meta:
        model = MoneyBookLog
        fields = ["log_id", "log_status", "cash", "created_at"]
