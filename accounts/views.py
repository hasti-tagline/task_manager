from .models import User
from django.shortcuts import render
from rest_framework_simplejwt.views import (TokenObtainPairView)
from .serializers import (CustomLoginSerializer,RegisterSerializer,UserListSerializer,UserDetailSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (CreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView)
from .permissions import (IsAdminUserRole)
from rest_framework.permissions import AllowAny
from  rest_framework.response import Response
from .pagination import CustomPagination
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from tasks.models import Task
from tasks.serializers import TaskSerializer


# RegisterAPI View
class RegisterAPIView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


#LoginAPI View
class LoginAPIView(TokenObtainPairView):

    def get_serializer_class(self):
        return CustomLoginSerializer



# UserDetailAPI View
class UserDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        user = serializer.save()
        role = self.request.data.get("role")

        if role == "admin":
            user.is_superuser = True
            user.is_staff = True
            user.role = "admin"
        else:
            user.is_superuser = False
            user.is_staff = False
            user.role = role

        user.save()



# UserListAPIView
class UserListAPIView(ListAPIView):

    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        
        user = self.request.user
        # Base queryset according to role
        if user.role == "admin":
            queryset = User.objects.filter(
                 Q(role="employee") | Q(role="manager") | Q(id=user.id)
            )

        elif user.role == "manager":
            queryset = User.objects.filter(
                Q(role="employee") | Q(id=user.id))
            
    
        else:
            queryset = User.objects.filter(id=user.id)

        # Search
        search = self.request.GET.get("search", "")
        if search:
            queryset = queryset.filter(
                username__icontains=search
            )

        # Role filter
        valid_roles = [
            "admin",
            "manager",
            "employee",
        ]
      
        role = self.request.GET.get("role", "")

        if role and role not in valid_roles:
                raise ValidationError({
                    "detail": ["Invalid status value"]
                })

        if role:
            queryset = queryset.filter(role=role)

        return queryset



class UserTaskListAPIView(ListAPIView):

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user_id = self.kwargs["user_id"]

        return Task.objects.filter(
            assigned_to__id=user_id
        ).distinct()





# Normal Django View For render user datail page
def user_detail_page(request):
    
    return render(request, "user-detail.html")


# chat page 
def chat_page(request):
    return render(request, "chat.html")

