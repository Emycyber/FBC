from .models import FooterLink

def footer_links(request):
    # context processor: automatically adds footer_links
    # to every template across the entire site
    # without needing to add it to every view manually
    links = FooterLink.objects.filter(is_active=True)
    # filter(is_active=True): only shows active links
    return {'footer_links': links}