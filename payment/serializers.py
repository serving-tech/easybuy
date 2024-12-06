from rest_framework import serializers

from visitor.models import Profile


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name','email','phone']