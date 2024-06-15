from rest_framework import viewsets
from .models import Form
from .serializers import FormSerializer
from rest_framework.response import Response
from rest_framework import status
from user_app.permissions import BasePermissions, IsAuthenticatedUser
class FormViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedUser,
                          BasePermissions]
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def get_queryset(self):
        return  Form.objects.filter(owner=self.request.user)

    def create(self, request):
        serializer = FormSerializer(data=request.data)
        organization = self.request.user.organization
        if serializer.is_valid():
            serializer.save(owner = self.request.user, organization = organization)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        print('printing', request.user.organization)
        form = self.get_object()
        # form = self.queryset.get(pk=pk)
        serailized_data = FormSerializer(form)
        return Response(serailized_data.data)
    
    # def list(self, request):
    #     print(request.user)
    #     form = self.queryset.filter()
    #     serailized_data = FormSerializer(form, many=True)
    #     return Response(serailized_data.data)

    
    def update(self, request, pk=None):
        try:
            form = self.queryset.get(pk=pk)
        except Form.DoesNotExist:
            return Response({'error': 'Form not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FormSerializer(form, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        item = self.queryset.get(id=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

