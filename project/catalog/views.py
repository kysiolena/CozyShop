from django.http import HttpRequest, HttpResponse


def catalog_page(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<html><body><h1>Catalog Page</h1></body></html>')


def product_page(request: HttpRequest) -> HttpResponse:
    return HttpResponse('<html><body><h1>Product Page</h1></body></html>')
