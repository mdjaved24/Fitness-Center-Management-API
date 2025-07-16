from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from fitness_app.models import FitnessCenter
from fitness_app.serializers import UserRegistrationSerializer, FitnessCenterSerializer

User = get_user_model()

class RegisterView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FitnessCenterListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        centers = FitnessCenter.objects.all()

        # Filtering
        min_fee = request.query_params.get('min_fee')
        if min_fee:
            centers = centers.filter(monthly_fee__gte=min_fee)  # greater than or equal to
        max_fee = request.query_params.get('max_fee')
        if max_fee:
            centers = centers.filter(monthly_fee__lte=max_fee)  # less than or equal to
        facilities = request.query_params.get('facilities')
        if facilities:
            centers = centers.filter(facilities__icontains=facilities)   # contains (search)
        is_verified = request.query_params.get('is_verified')
        if is_verified:
            centers = centers.filter(is_verified=is_verified)

        # Ordering
        ordering = request.query_params.get('ordering')
        if ordering:
            centers = centers.order_by(ordering)

        serializer = FitnessCenterSerializer(centers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = FitnessCenterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FitnessCenterDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_center(self, pk):
        try:
            return FitnessCenter.objects.get(pk=pk)
        except FitnessCenter.DoesNotExist:
            return None

    def get(self, request, pk):
        center = self.get_center(pk)
        if not center:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = FitnessCenterSerializer(center)
        return Response(serializer.data)
    

    def put(self, request, pk):
        center = self.get_center(pk=pk)
        if not center:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if center.owner != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = FitnessCenterSerializer(center, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        center = self.get_center(pk=pk)
        if not center:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if center.owner != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = FitnessCenterSerializer(center, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        center = self.get_center(pk=pk)
        if not center:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if center.owner != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        center.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FitnessCenterCategoryView(APIView):

    def get(self, request, category):
        center = FitnessCenter.objects.filter(category=category)
        serializer = FitnessCenterSerializer(center, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
