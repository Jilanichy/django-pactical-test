from random import choices
from rest_framework import serializers
from customers.models import SubscriptionInfo, PLAN_CHOICES, COMPANY_CHOICES
from django.contrib.auth.models import User

'''
    'SubscriptionInfo' has reverse relationship on the User model, 
    it'll not be included by default when using the ModelSerializer class, 
    that's why an explicit field has been added
'''
class UserSerializer(serializers.ModelSerializer):
    SubscriptionInfo = serializers.PrimaryKeyRelatedField(many=True, queryset=SubscriptionInfo.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'SubscriptionInfo']


class SubscriptionInfoSerializer(serializers.ModelSerializer):
    admin = serializers.ReadOnlyField(source='admin.username')

    class Meta:
        model = SubscriptionInfo
        fields = ['id', 'admin', 'subscriber_name', 'primary_phone_number', 'other_phone_number', 
            'plan_type', 'subscription_price', 'subscribed_company', 'phone_number_owner', 
            'contract_initiated']
 

    def create(self, validated_data):
        """
        Create and return a new `SubscriptionInfo` instance, given the validated data.
        """
        return SubscriptionInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `SubscriptionInfo` instance, given the validated data.
        """
        instance.plan_type = validated_data.get('plan_type', instance.plan_type)
        instance.other_phone_number = validated_data.get('other_phone_number', instance.other_phone_number)
        instance.subscribed_company = validated_data.get('subscribed_company', instance.subscribed_company)
        instance.save()
        return instance
