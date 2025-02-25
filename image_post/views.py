import json
import cv2
import base64
from django.shortcuts import render, redirect
from .models import ImagePost
from .forms import ImagePostForm
from PIL import Image
import pytesseract
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.base import ContentFile
import numpy as np

def index(request):
    if request.method == "POST":
        form = ImagePostForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save() 
            # Open the image using PIL
            image = Image.open(instance.image)

            # Extract text using Tesseract OCR
            # Step 2: Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            extracted_text = pytesseract.image_to_string(gray_image, lang='lao+eng')
            print('text printed: ', extracted_text)
            # Save the extracted text to the database
            instance.extracted_text = extracted_text
            instance.save()

            return redirect('index')
    else:
        form = ImagePostForm()

    images = ImagePost.objects.all()
    return render(request, 'image_post/index.html', {'form': form, 'images': images})

@csrf_exempt  # Temporarily disable CSRF for testing
def upload_image(request):
    if request.method == 'POST':
        print(request.method)
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            print('data: ', data)
            image_data = data.get('image')

            # Decode the base64 image data
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_file = ContentFile(base64.b64decode(imgstr), name=f'capture.{ext}')

            image_bytes = base64.b64decode(imgstr)

            # Convert bytes to a NumPy array
            nparr = np.frombuffer(image_bytes, np.uint8)

            # Decode the image using OpenCV
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Save the grayscale image to a temporary file (optional, for debugging)
            cv2.imwrite(f'temp_gray.{ext}', gray_image)

            # Convert the grayscale image to a PIL image for Tesseract OCR
            pil_image = Image.fromarray(gray_image)
            # Save the image to a temporary file
            with open(f'temp.{ext}', 'wb') as f:
                f.write(image_file.read())

            # Open the image using PIL
            image = Image.open(f'temp.{ext}')

            # Extract text using Tesseract OCR
            extracted_text = pytesseract.image_to_string(pil_image, lang='lao+eng')

            # Save the image and extracted text to the database
            instance = ImagePost()
            instance.image.save(f'capture.{ext}', image_file)  # Save the image file
            instance.extracted_text = extracted_text  # Save the extracted text
            instance.save()

            # Clean up the temporary file
            import os
            os.remove(f'temp.{ext}')


            return JsonResponse({'status': 'success', 'message': 'Image uploaded successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def camera_view(request):
    return render(request, 'image_post/camera.html')
