from rest_framework import serializers
from .models import UserAccount, MedicalCenter, TeamMember, Address, Specialty, Favorite, Plan


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'


class MedicalCenterSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=True)
    specialties = SpecialtySerializer(many=True)

    class Meta:
        model = MedicalCenter
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
