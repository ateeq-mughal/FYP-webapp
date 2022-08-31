from django.shortcuts import render
from django.http import HttpResponse

from django.core.files.storage import FileSystemStorage
from .conventional import processConventionalContouring
from .healthCheck import predictHealth
from .cropClassification import classify


# Create your views here.


def index(request):
    print(request.FILES.dict())
    if request.method == "POST":
        if request.FILES["conventional"]:
            conventional = request.FILES["conventional"]
            print(conventional)

            fs = FileSystemStorage()
            filename = fs.save(
                "conventional/input." + conventional.name.split(".")[-1], conventional
            )
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            processConventionalContouring(uploaded_file_url[1:])
            return render(
                request,
                "contour/result.html",
                {"uploaded_file_url": "media/conventional/output.png"},
            )

    return render(request, "contour/index.html")


def healthCheck(request):
    print(request.FILES.dict())
    if request.method == "POST":
        if request.FILES["healthCheck"]:
            healthCheck = request.FILES["healthCheck"]
            print(healthCheck)

            fs = FileSystemStorage()
            filename = fs.save(
                "health/input." + healthCheck.name.split(".")[-1], healthCheck
            )
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            result = predictHealth(uploaded_file_url[1:])
            return render(
                request,
                "contour/healthCheck.html",
                {"uploaded_file_url": uploaded_file_url[1:], "result": result},
            )
    return HttpResponse("Hello")


def cropClassify(request):
    print(request.FILES.dict())
    if request.method == "POST" and request.FILES["crop-classify"]:
        crop = request.FILES["crop-classify"]
        print(crop)
        fs = FileSystemStorage()
        filename = fs.save("cropClassification/input." + crop.name.split(".")[-1], crop)

        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        result = classify(uploaded_file_url[1:])

        crop_image = (
            "static/Canola.gif" if result == "Canola" else "static/Sugarcane.gif"
        )

    return render(
        request,
        "contour/cropClassification.html",
        {"result": result, "crop_image": crop_image},
    )
