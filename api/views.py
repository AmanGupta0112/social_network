from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return Response(self.get_serializer(user).data)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("query", "")
        users = User.objects.filter(
            Q(email__iexact=query) | Q(username__icontains=query)
        )
        page = self.paginate_queryset(users)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    @action(detail=False, methods=["post"])
    def send_request(self, request):
        to_user_id = request.data.get("to_user")
        to_user = User.objects.get(id=to_user_id)
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=request.user, to_user=to_user, defaults={"status": "pending"}
        )
        return Response(self.get_serializer(friend_request).data)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.status = "accepted"
        friend_request.save()
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.to_user.friends.add(friend_request.from_user)
        return Response(self.get_serializer(friend_request).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        friend_request = self.get_object()
        friend_request.status = "rejected"
        friend_request.save()
        return Response(self.get_serializer(friend_request).data)

    @action(detail=False, methods=["get"])
    def list_friends(self, request):
        friends = request.user.friends.all()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def pending_requests(self, request):
        pending_requests = FriendRequest.objects.filter(
            to_user=request.user, status="pending"
        )
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data)
