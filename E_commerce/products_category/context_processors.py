from . models import catogary

def menu_links(request):
    links = catogary.objects.all()
    return dict(links=links)