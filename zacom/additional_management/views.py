from django.shortcuts import render

# Create your views here.
from .models import Banner,PromotionBanner

def homepage(request):

    return render(request, "admin_templates/homepage.html")


def banner1(request):
    instance=Banner.objects.get(id=1)
    print(instance.title)
    context={"instance":instance}

    if request.method == 'POST':
        Title=request.POST['video_title']   
        video = request.FILES.get('video_file')  
        image1 = request.FILES.get('image1')  
        image2 = request.FILES.get('image2') 
        print(image1)

        if Title is not None:
            instance.title = Title
        if video is not None:
            instance.video = video
        if image1 is not None:
            instance.image1 = image1
        if image2 is not None:
            instance.image2 = image2
        instance.save()

    return render(request, "admin_templates/banner1.html",context)
    
def banner2(request):
    
    instance=PromotionBanner.objects.first()
   
    context={"instance":instance}

    if request.method == 'POST':
        Title1=request.POST['text_field_1']   
        Title2=request.POST['text_field_2']   
        Title3=request.POST['text_field_3']   
        Image = request.FILES.get('image_field')  
       
        print(Title1,Title2)

        if Title1 is not None:
            instance.title1 = Title1
        if Title2 is not None:
            instance.title2 = Title2
        if Title3 is not None:
            instance.title3 = Title3
        if Image is not None:
            instance.image = Image
        instance.save()

    
    return render(request, "admin_templates/banner2.html",context)

    