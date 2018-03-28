from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    # import pdb
    # pdb.set_trace()
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    return render(request, 'home.html', {'new_item_text': request.POST.get('item_text', '')})
