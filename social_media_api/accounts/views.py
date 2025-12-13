from django.shortcuts import render
# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response

CustomUser = get_user_model()


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)
        return Response(
            {"detail": "User followed successfully"},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": "User unfollowed successfully"},
            status=status.HTTP_200_OK
        )
