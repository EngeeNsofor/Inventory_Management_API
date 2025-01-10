from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets, filters, generics
from .models import InventoryItem, InventoryLog
from .serializers import InventoryItemSerializer, InventoryLogSerializer
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from dotenv import load_dotenv # type: ignore
import os
load_dotenv()



def home(request):
    return HttpResponse("Welcome to the Inventory Management System!")

### --- API LOGIC --- ###

# API Registration (returns tokens with message)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 8:
        return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'Registration successful.',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


# API Login (returns tokens with message)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


### --- UI LOGIC --- ###

# UI Registration (renders HTML form)
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'inventory/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return render(request, 'inventory/register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'inventory/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login_page')

    return render(request, 'inventory/register.html')


# UI Login (renders HTML form)
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'inventory/login.html')

# Inventory API CRUD (ViewSet)
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'price', 'quantity', 'name']
    ordering_fields = ['name', 'price', 'quantity', 'date_added']
    search_fields = ['name', 'category']

    def get_queryset(self):
        return InventoryItem.objects.filter(managed_by=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = 'Item successfully created'
        return response
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the item being updated
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Validate data
        serializer.is_valid(raise_exception=True)

        # Check for changes
        changes_made = False
        for field, value in serializer.validated_data.items():
            if getattr(instance, field) != value:
                changes_made = True
                break

        if not changes_made:
            return Response(
                {"detail": "No changes were made."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Perform update if changes exist
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Item successfully updated'
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        item_name = instance.name
        change_reason = request.data.get('change_reason', 'unwanted')
        InventoryLog.objects.create(
            item=None,  # Set to None after deletion
            item_name=item_name, 
            changed_by=self.request.user,
            change_type='DELETE',
            quantity_before=instance.quantity,
            quantity_after=0,
            change_reason=change_reason
        )
        self.perform_destroy(instance)
        return Response({'message': 'Item successfully deleted'}, status=204)

    def perform_create(self, serializer):
        instance = serializer.save(managed_by=self.request.user)
        item_name = instance.name
        InventoryLog.objects.create(
            item=instance,
            item_name=item_name,
            changed_by=self.request.user,
            change_type='CREATE',
            quantity_before=0,
            quantity_after=instance.quantity,
            change_reason='new-item'
        )

    def perform_update(self, serializer):
        instance = serializer.instance
        old_quantity = instance.quantity
        new_quantity = serializer.validated_data.get('quantity', old_quantity)
        item_name = instance.name
        change_reason = self.request.data.get('change_reason')

        # Detect quantity change and validate change_reason
        if new_quantity != old_quantity:
            if change_reason not in ['sold', 'restock', 'damaged']:
                raise ValidationError({
                    "change_reason": "When quantity changes, `change_reason` must be added to the request body and the reason must be one of 'sold', 'restock', or 'damaged'."
                })
        
        # Save item changes
        serializer.save()
        new_quantity = serializer.instance.quantity

        # Create inventory log for update
        InventoryLog.objects.create(
            item=serializer.instance,
            item_name=item_name,
            changed_by=self.request.user,
            change_type='UPDATE',
            quantity_before=old_quantity,
            quantity_after=new_quantity,
            change_reason=change_reason if new_quantity != old_quantity else 'rebrand'
        )
        if instance.quantity < 5: # Low stock alert triggered when inventory item is less than 5
            send_mail(
                f'Low Stock Alert: {instance.name}',
                f'{instance.name} has only {instance.quantity} left.\n Please try to restock {instance.name} as soon as possible.\n',
                'no-reply@inventorymanagement.com',
                [instance.managed_by.email, os.getenv('ALERT_EMAIL') ], 
            )

class InventoryLogListView(generics.ListAPIView):
    serializer_class = InventoryLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        item_id = self.kwargs.get('item_id', None)  # Get item_id if provided

        # If item_id is passed, filter logs for that specific item
        if item_id:
            return InventoryLog.objects.filter(item_id=item_id, changed_by=user).order_by('-timestamp')
        
        # If no item_id, return all logs for the user
        return InventoryLog.objects.filter(changed_by=user).order_by('-timestamp')
