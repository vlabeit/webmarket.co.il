from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'lawyer/index.html')
def about(request):
	return render(request, 'lawyer/about.html')
def blog(request):
	return render(request, 'lawyer/blog.html')
def contact(request):
	return render(request, 'lawyer/contact.html')
def won(request):
	return render(request, 'lawyer/won.html')
def practice(request):
	return render(request, 'lawyer/practice.html')