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

