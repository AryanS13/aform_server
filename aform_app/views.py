from rest_framework import viewsets
from .models import Form
from .serializers import FormSerializer
from rest_framework.response import Response
from rest_framework import status

class FormViewSet(viewsets.ViewSet):
    queryset = Form.objects.all()

    def create(self, request):
        serializer = FormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        form = self.queryset.get(pk=pk)
        serailized_data = FormSerializer(form)
        return Response(serailized_data.data)

    def list(self, request):
        serializer = FormSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
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

