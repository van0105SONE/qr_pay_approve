from django.shortcuts import render, redirect
from .models import ImagePost
from .forms import ImagePostForm


def index(request):

    if request.method == "POST":
        form = ImagePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the uploaded file to the database
            return redirect('index')
    else:
        form = ImagePostForm()

    images = ImagePost.objects.all()
    print( images[1])
    return render(request, 'image_post/index.html', {'form': form, 'images': images})

