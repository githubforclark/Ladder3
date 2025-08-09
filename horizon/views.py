from django.shortcuts import render

# Create your views here.
def indexView(request):
    print(request,'11')
    return render(request,'index.html')
