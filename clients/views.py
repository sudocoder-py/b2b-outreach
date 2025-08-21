from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.serializers import (
    LoginSerializer, CompanyRegistrationSerializer, UserRegistrationSerializer, UserUpdateSerializer
)
from .models import SubscribedCompany
from django.contrib.auth.decorators import login_not_required


@login_not_required
def home_view(request):
    """Feedback and feature requests page"""
    return render(request, "home/landing.html")


# Template Views
@login_not_required
def login_view(request):
    """Login page template"""
    return render(request, 'auth/login.html')

@login_not_required
def login_submit(request):
    """Handle login form submission"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.first_name:
                        messages.success(request, f'Welcome back, {user.first_name}!')
                        return redirect('overall_dashboard')
                    else:
                        messages.success(request, 'Welcome back!')
                        return redirect('account_settings')
                else:
                    messages.error(request, 'Your account is disabled.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter both username and password.')

    return render(request, 'auth/login.html')


def logout_view(request):
    """Logout page template"""
    logout(request)
    return redirect('home')


def company_registration_view(request):
    """Company registration page template"""
    return render(request, 'auth/company_registration.html')


def user_registration_view(request):
    """User registration page template"""
    company_data = request.session.get('company_data', {})
    return render(request, 'auth/user_registration.html', {'company_data': company_data})



# API Views
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """API endpoint for user login"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'redirect_url': reverse('products')
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """API endpoint for user logout"""
    logout(request)
    return Response({
        'success': True,
        'message': 'Logout successful',
        'redirect_url': reverse('login')
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_company_registration(request):
    """API endpoint for company registration (step 1)"""
    serializer = CompanyRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Store company data in session
        request.session['company_data'] = serializer.validated_data
        return Response({
            'success': True,
            'message': 'Company information saved',
            'redirect_url': reverse('user_registration')
        }, status=status.HTTP_200_OK)

    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_user_registration(request):
    """API endpoint for user registration (step 2)"""
    # Check if company data exists in session
    if 'company_data' not in request.session:
        return Response({
            'success': False,
            'message': 'Please complete company registration first.',
            'redirect_url': reverse('company_registration')
        }, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Create company first
            company_data = request.session['company_data']
            company = SubscribedCompany.objects.create(**company_data)

            # Create user and associate with company
            user = serializer.save()
            user.subscribed_company = company
            user.save()

            # Clear session data
            del request.session['company_data']

            # Log the user in
            login(request, user)

            return Response({
                'success': True,
                'message': 'Account created successfully! Welcome to Instantly.',
                'redirect_url': reverse('overall_dashboard')
            }, status=status.HTTP_201_CREATED)

        except Exception:
            # If company was created but user creation failed, clean up
            if 'company' in locals():
                company.delete()
            return Response({
                'success': False,
                'message': 'An error occurred during registration. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)












from django.contrib.auth import get_user_model

User = get_user_model()

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # only allow updating the logged-in user
        return self.request.user
    

class UpdateCompanyInfoView(generics.UpdateAPIView):
    queryset = SubscribedCompany.objects.all()
    serializer_class = CompanyRegistrationSerializer

    def get_object(self):
        # only allow updating the logged-in user
        return self.request.user.subscribed_company