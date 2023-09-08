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


# from django.http import JsonResponse
# from django.views import View
# from django.core.files.storage import FileSystemStorage
# from django.conf import settings
# import os
# import cv2
# import numpy as np

# class UploadImageView(View):
#     def post(self, request, *args, **kwargs):
#         image = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(image.name, image)
#         file_path = fs.path(filename)

#         # OpenCV 로직
#         image = cv2.imread(file_path)

#         if image is not None:
#             hex_color = request.POST.get('hex_color', 'FFFFFF')
#             color = int(hex_color, 16)
#             r = color % 0x100
#             g = color // 0x100 % 0x100
#             b = color // 0x10000 % 0x100

#             image[0:50, 0:50] = [b, g, r]

#             # 저장할 파일의 상대 경로
#             relative_output_path = os.path.join('modified_images', 'output.jpg')

#             # 저장할 파일의 절대 경로
#             output_path = os.path.join(settings.MEDIA_ROOT, relative_output_path)

#             # 이미지 저장
#             cv2.imwrite(output_path, image)

#             # 저장된 이미지의 URL
#             image_url = os.path.join(settings.MEDIA_URL, relative_output_path)

#             # return JsonResponse({'message': f'Modified image saved to {output_path}', 'image_url': image_url})
#             return JsonResponse({'message': f'Modified image saved to {output_path}', 'image_url': f'/media/{output_path}'})
#         else:
#             return JsonResponse({'message': 'Failed to load the image. Please check the file path.'}, status=400)




# from django.http import JsonResponse
# from django.views import View
# from django.core.files.storage import FileSystemStorage
# import cv2
# import numpy as np

# class UploadImageView(View):
#     def post(self, request, *args, **kwargs):
#         image = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(image.name, image)
#         file_path = fs.path(filename)

#         # OpenCV 로직
#         image = cv2.imread(file_path)

#         if image is not None:
#             hex_color = request.POST.get('hex_color', 'FFFFFF')  # 프론트엔드에서 전달된 색상 코드
#             color = int(hex_color, 16)
#             r = color % 0x100
#             g = color // 0x100 % 0x100
#             b = color // 0x10000 % 0x100

#             image[0:50, 0:50] = [b, g, r]

#             output_path = "output.jpg"
#             cv2.imwrite(output_path, image)

#             return JsonResponse({'message': f'Modified image saved to {output_path}'})
#         else:
#             return JsonResponse({'message': 'Failed to load the image. Please check the file path.'}, status=400)
