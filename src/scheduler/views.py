from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TimeSlot, Infra, FacultyUnavailability, Occupancy
from .serializers import TimeSlotSerializer, InfraSerializer, FacultyUnavailabilitySerializer, OccupancySerializer
from api.permissions import RoleBasedAccessPermission
from users.models import User

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [RoleBasedAccessPermission]

class InfraViewSet(viewsets.ModelViewSet):
    queryset = Infra.objects.all()
    serializer_class = InfraSerializer
    permission_classes = [RoleBasedAccessPermission]

class FacultyUnavailabilityViewSet(viewsets.ModelViewSet):
    queryset = FacultyUnavailability.objects.all()
    serializer_class = FacultyUnavailabilitySerializer
    permission_classes = [RoleBasedAccessPermission]

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        """
        HOD can approve a pending FacultyUnavailability.
        """
        unavail = self.get_object()
        if request.user.role != 'HOD':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        unavail.status = "approved"
        unavail.save()
        return Response({"status": "approved"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject(self, request, pk=None):
        """
        HOD can reject a pending FacultyUnavailability.
        """
        unavail = self.get_object()
        if request.user.role != 'HOD':
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        unavail.status = "rejected"
        unavail.save()
        return Response({"status": "rejected"}, status=status.HTTP_200_OK)

class OccupancyViewSet(viewsets.ModelViewSet):
    queryset = Occupancy.objects.all()
    serializer_class = OccupancySerializer
    permission_classes = [RoleBasedAccessPermission]

    @action(detail=False, methods=['post'], url_path='scheduler-update')
    def scheduler_update(self, request):
        """
        Endpoint for AI scheduler (CPSAT / OptaPlanner) to update Occupancy.
        Only callable by HOD or Scheduler service (token-based auth can be added).
        """
        # Here you would implement bulk occupancy updates from scheduler
        # For now, we just accept a payload and update Occupancy objects
        # Example payload: [{"id": 1, "faculty": 3, "subject": 5, "room": 2, "timeslot": 7, "status": "booked"}]

        if not request.user.role in ['HOD', 'Admin']:  # Admin can also trigger
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        updates = request.data
        updated_objs = []
        for item in updates:
            try:
                occ = Occupancy.objects.get(id=item.get('id'))
                for field in ['faculty', 'subject', 'room', 'timeslot', 'status']:
                    if field in item:
                        setattr(occ, field, item[field])
                occ.save()
                updated_objs.append(OccupancySerializer(occ).data)
            except Occupancy.DoesNotExist:
                continue

        return Response({"updated": updated_objs}, status=status.HTTP_200_OK)
