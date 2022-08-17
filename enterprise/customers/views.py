from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from customers.models import SubscriptionInfo
from django.contrib.auth.models import User




@api_view(['GET', 'POST'])
def subscription_list(request, format=None):
    """
    List all subscriptions, or create a new subscription.
    """
    if request.method == 'GET':
        subscriptions = SubscriptionInfo.objects.all()
        serializer = SubscriptionInfoSerializer(subscriptions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SubscriptionInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def subscription_detail(request, pk, format=None):
    """
    Retrieve, update or delete a subscription
    """
    try:
        subscriber = SubscriptionInfo.objects.get(pk=pk)
    except SubscriptionInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubscriptionInfoSerializer(subscriber)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubscriptionInfoSerializer(subscriber, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subscriber.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)