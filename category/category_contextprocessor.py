from .models import Category
def category_link(request):
    link=Category.objects.all()
    return dict(link=link)