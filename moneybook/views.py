from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MoneyBook, MoneyBookLog
from .serializers import MoneyBookSerializer
from .serializers import MoneyBookLogSerializer, MoneyBookLogListSerializer


class MoneyBookLogAPIView(APIView):
    """
    MoneyBookLog 모델 LIST, CREATE APIView
    URI: {service_root}/moneybook/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        user_moneybook = MoneyBook.objects.get(user=user_id)
        user_moneybook_log = MoneyBookLog.objects.filter(moneybook=user_moneybook.id)

        return Response(
            {
                "userMoneybook": MoneyBookSerializer(user_moneybook).data,
                "logList": MoneyBookLogListSerializer(user_moneybook_log, many=True).data
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        user_id = request.user.id
        user_moneybook = MoneyBook.objects.get(user=user_id)
        log_id = user_moneybook.latest_log_id + 1
        request_data = request.data
        request_data["log_id"] = log_id
        request_data["moneybook"] = user_moneybook.id
        serializer = MoneyBookLogSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_moneybook.latest_log_id += 1
            cash = serializer.data.get("cash")

            if serializer.data.get("log_status") == "IC":
                user_moneybook.cash_amount += cash
            else:
                user_moneybook.cash_amount -= cash

            user_moneybook.save()

            return Response({"msg": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)


class MoneyBookLogDetailAPIView(APIView):
    """
    MoneyBookLog 모델 RETRIEVE, UPDATE APIView
    URI: {service_root}/moneybook/<int:log_id>/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, log_id):
        user = request.user
        user_moneybook = MoneyBook.objects.get(user=user)
        user_moneybook_log = MoneyBookLog.objects.get(
            moneybook=user_moneybook, log_id=log_id
        )

        return Response(
            {"detailLog": MoneyBookLogSerializer(user_moneybook_log).data},
            status=status.HTTP_200_OK,
        )

    def put(self, request, log_id):
        user = request.user
        user_moneybook = MoneyBook.objects.get(user=user)
        user_moneybook_log = MoneyBookLog.objects.get(
            moneybook=user_moneybook, log_id=log_id
        )
        current_cash_amount = user_moneybook.cash_amount
        current_cash = user_moneybook_log.cash

        if user_moneybook_log.log_status == "IC":
            current_cash_amount -= current_cash
        else:
            current_cash_amount += current_cash

        serializer = MoneyBookLogSerializer(
            user_moneybook_log, data=request.data, partial=True
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            change_cash = serializer.data.get("cash")

            if serializer.data.get("log_status") == "IC":
                current_cash_amount += change_cash
            else:
                current_cash_amount -= change_cash

            user_moneybook.cash_amount = current_cash_amount
            user_moneybook.save()

            return Response(
                {"msg": "기록 수정 성공", "detailLog": serializer.data},
                status=status.HTTP_200_OK
            )

    def delete(self, request, log_id):
        user = request.user
        user_moneybook = MoneyBook.objects.get(user=user)
        user_moneybook_log = MoneyBookLog.objects.get(
            moneybook=user_moneybook, log_id=log_id
        )
        cash = user_moneybook_log.cash

        if user_moneybook_log.log_status == "IC":
            user_moneybook.cash_amount -= cash
        else:
            user_moneybook.cash_amount += cash

        user_moneybook.latest_log_id -= 1
        user_moneybook.save()
        user_moneybook_log.delete()

        return Response({"msg": "기록 삭제 성공"}, status=status.HTTP_200_OK)
