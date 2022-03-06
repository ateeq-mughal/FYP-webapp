from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .conventional import process


# Create your views here.

def index(request):
    print(request.FILES.dict())
    if request.method == 'POST':
        if request.FILES['conventional']:
            conventional = request.FILES['conventional']
            print(conventional)
            
            fs = FileSystemStorage()
            filename = fs.save("input."+conventional.name.split('.')[-1], conventional)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            process(uploaded_file_url[1:])
            return render(request, 'contour/result.html', {
                'uploaded_file_url': "media/output.png"
            })
            

    return render(request, 'contour/index.html')