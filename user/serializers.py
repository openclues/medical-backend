from rest_framework import serializers
from .models import UserAccount, MedicalCenter, TeamMember, Address, Specialty, Favorite, Plan, MedicalCenterSpecialty, \
    Doctor, Service


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


class MedicalCenterSpecialtySerializer(serializers.ModelSerializer):
    speciality = SpecialtySerializer()

    class Meta:
        model = MedicalCenterSpecialty
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    specialist = SpecialtySerializer()
    class Meta:
        model = Doctor
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class MedicalCenterSerializer(serializers.ModelSerializer):
    # speciality = serializers.SerializerMethodField()
    doctors = DoctorSerializer(many=True)

    center_services = ServiceSerializer(many=True)

    addresses = serializers.SerializerMethodField()

    class Meta:
        model = MedicalCenter
        fields = '__all__'

    @staticmethod
    def get_speciality(obj):
        return MedicalCenterSpecialtySerializer(obj.center_speciality_information, many=True).data

    @staticmethod
    def get_addresses(obj):
        return AddressSerializer(obj.addresses, many=True).data


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
