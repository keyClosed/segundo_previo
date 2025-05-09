from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Rating, Trip, Vehicle
from .serializers import (
    RatingSerializer,
    TripSerializer,
    UserSerializer,
    VehicleSerializer,
)

User = get_user_model()

class HomeView(TemplateView):
    template_name = 'rides/home.html'


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='toggle-availability')
    def toggle_availability(self, request, pk=None):
        vehicle = self.get_object()
        vehicle.is_available = not vehicle.is_available
        vehicle.save()
        return Response({'is_available': vehicle.is_available}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='models-summary')
    def models_summary(self, request):
        summary = self.get_queryset().values('model').annotate(count=Count('id'))
        return Response(summary)


class TripViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['driver']

    @action(detail=False, methods=['get'], url_path='active-count')
    def active_count(self, request):
        pending_count = Trip.objects.filter(status='PENDING').count()
        ongoing_count = Trip.objects.filter(status='ONGOING').count()
        return Response({
            "pending": pending_count,
            "ongoing": ongoing_count
        }, status=status.HTTP_200_OK)


class DriverViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_driver=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='trending')
    def trending(self, request):
        top_drivers = (
            User.objects.filter(is_driver=True)
            .annotate(average_score=Avg('received_ratings__score'))
            .order_by('-average_score')[:5]
        )
        data = [
            {
                "id": driver.id,
                "name": driver.get_full_name(),
                "average_score": round(driver.average_score or 0, 2)
            }
            for driver in top_drivers
        ]
        return Response(data)


class RatingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]


class PassengerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_passenger=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='trips')
    def trips(self, request, pk=None):
        trips = Trip.objects.filter(passenger__id=pk)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
