from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.models import MedicalCenter
from user.permissions import HasSubscription
from user.serializers import MedicalCenterSerializer
from django_filters import rest_framework as filters


class MedicalCenterFilter(filters.FilterSet):
    speciality = filters.CharFilter(field_name='doctors__specialist__name',
                                    lookup_expr='icontains')
    free = filters.BooleanFilter(field_name='center_services__is_free', lookup_expr="exact")
    city = filters.CharFilter(field_name='addresses__city', lookup_expr='icontains')
    province = filters.CharFilter(field_name='addresses__state_province', lookup_expr='icontains')
    country = filters.CharFilter(field_name='addresses__country', lookup_expr='icontains')

    class Meta:
        model = MedicalCenter
        fields = ['speciality', 'city', 'province', 'country' , 'free']


class MedicalCenterListApiView(generics.ListCreateAPIView):
    serializer_class = MedicalCenterSerializer
    permission_classes = (IsAuthenticated, HasSubscription)
    queryset = MedicalCenter.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicalCenterFilter
