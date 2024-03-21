from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .utils import process_file
import json
import logging

logger = logging.getLogger(__name__)  #
# Initialize logger for debugging and error logging


class FileUploadView(APIView):
    parser_classes = (
        MultiPartParser,
        FormParser,
    )  # For handling 'multipart/form-data' and 'application/x-www-form-urlencoded' content types

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "GET request received. Please POST a file to upload."},
            status=status.HTTP_200_OK,
        )  # Respond to GET requests with a message to use POST for uploading files

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(
            data=request.data
        )  # Deserialize the incoming data to a Python object

        if file_serializer.is_valid():
            uploaded_file = request.FILES.get(
                "file"
            )  # Extract the file from the request for processing

            try:
                # Process the uploaded file and load the result into a Python dictionary
                result = process_file(uploaded_file)
                data = json.loads(result)
                return Response(data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Log the exception details if file processing fails
                logger.error(f"Error processing file upload: {e}", exc_info=True)
                return Response(
                    {"error": "An error occurred during file processing."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            # Return validation errors if the serializer is invalid
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
