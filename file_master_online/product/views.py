# from django.shortcuts import render
from django.utils import timezone
from .models import Product
from django.shortcuts import render, get_object_or_404
import json
from .forms import ProductForm
from django.http import HttpResponse

from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Max

# Python logging package
import logging
# Standard instance of a logger with __name__
stdlogger = logging.getLogger(__name__)


def product_detail(request, pk):
    stdlogger.info("        +++ [info] Call to PRODUCT_DETAIL method")

    product = get_object_or_404(Product, pk=pk)
    data =product.data
    prod_name = product.name
    prod_pk = pk
    stdlogger.debug("       *** [debug] product name: "+ prod_name)
    
    try:
        lista = data['data']
        stdlogger.debug("       *** [debug] product data: {}".format(lista))
    except:
        import traceback
        print traceback.format_exc()
        lista = { }
    return render(request, 'product/product_detail.html', {'list': lista, 'prod_name': prod_name, 'prod_pk':prod_pk})    
    # return render(request, 'product/product_detail.html')


def product_list(request):

    products = Product.objects.raw('''
        select *
        from (
        select id, 
                name,
                revision,
                max(revision) over (partition by name) as max_thing
        from "product_product"
        ) t
        where revision = max_thing
    ''')


    return render(request, 'product/product_list.html', {'products': products})


def product_new(request):
    print(request.GET)
    print(request.POST)
    if request.method == "POST":
        my_name = request.POST.get('name')
        my_data = request.POST.get('data')
        my_rev = request.POST.get('revision')
        if(my_rev):
            print("revision -> "+my_rev)
        else:
            my_rev = 0
        d = json.loads(my_data)
        Product.objects.create(name=my_name, data=d, revision=my_rev )
            # redirect to HOME
        return HttpResponseRedirect("/")

    return render(request, "product/product_new.html")

def product_delete(request, pk):
    product = Product.objects.filter(pk=pk) 
    # product = get_object_or_404(pk=pk)
    if product.exists():
        # Standard Django delete
        product.delete()

    # redirect to HOME
    return HttpResponseRedirect("/")

def product_update(request, pk):
    stdlogger.info("        +++ [info] Call to PRODUCT_UPDATE method")
    # import pdb; pdb.set_trace()
    product = get_object_or_404(Product, pk=pk)
    data =product.data
    prod_name = product.name
    prod_pk = pk
    rev = product.revision
    # stdlogger.debug("       *** [debug] product name: "+ prod_name)
    
    try:
        lista = data['data']
        # stdlogger.debug("       *** [debug] product data: {}".format(lista))
        
    except:
        import traceback
        print traceback.format_exc()
        lista = { }

    return render(request, 'product/product_update.html', {'list': lista, 'prod_name': prod_name, 'prod_pk':prod_pk, 'prod_rev':rev})   
    # # redirect to HOME
    # return HttpResponseRedirect("/")