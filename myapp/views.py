from django.http import JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np

class UploadImageView(View):
    def post(self, request, *args, **kwargs):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_path = fs.path(filename)

        # OpenCV 로직
        image = cv2.imread(file_path)

        if image is not None:
            hex_color = request.POST.get('hex_color', 'FFFFFF')  # 프론트엔드에서 전달된 색상 코드
            color = int(hex_color, 16)
            r = color % 0x100
            g = color // 0x100 % 0x100
            b = color // 0x10000 % 0x100

            image[0:50, 0:50] = [b, g, r]

            output_path = "output.jpg"
            cv2.imwrite(output_path, image)

            return JsonResponse({'message': f'Modified image saved to {output_path}'})
        else:
            return JsonResponse({'message': 'Failed to load the image. Please check the file path.'}, status=400)
