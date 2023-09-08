from django.http import JsonResponse, HttpResponse
from PIL import Image
import numpy as np
import cv2
import io
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import cv2
import numpy as np

class UploadImageView(View):
    def post(self, request, *args, **kwargs):
        image = request.FILES['image'].read()
        image = np.asarray(bytearray(image), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        if image is not None:
            hex_color = request.POST.get('hex_color', 'FFFFFF')
            color = int(hex_color, 16)
            r = color % 0x100
            g = color // 0x100 % 0x100
            b = color // 0x10000 % 0x100

            image[0:50, 0:50] = [b, g, r]

            # Convert the image back to JPEG
            _, img_encoded = cv2.imencode('.jpg', image)
            response = HttpResponse(img_encoded.tostring(), content_type='image/jpeg')
            return response

        else:
            return JsonResponse({'message': 'Failed to load the image. Please check the file path.'}, status=400)


