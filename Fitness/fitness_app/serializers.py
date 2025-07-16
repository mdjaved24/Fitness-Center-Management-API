from rest_framework import serializers
from fitness_app.models import FitnessCenter
from datetime import datetime, date

from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']

class FitnessCenterSerializer(serializers.ModelSerializer):
    price_per_session = serializers.SerializerMethodField()

    class Meta:
        model = FitnessCenter
        fields = '__all__'
        read_only_fields = ['owner','created_at','updated_at']

    def get_price_per_session(self, obj):
        return obj.monthly_fee / obj.total_sessions
    
    def validate_monthly_fee(self, value):
        if value<500:
            raise serializers.ValidationError('Monthly Fee must be greater than or equal to 500')
        return value
    
    def validate_total_sessions(self, value):
        if value<4:
            raise serializers.ValidationError('Total sessions must be greater than or equal to 4')
        return value
    
    def validate_established_date(self, value):
        if value>date.today():
            raise serializers.ValidationError('Date cannot be in future')
        return value
    