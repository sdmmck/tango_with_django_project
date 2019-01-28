from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed
    # to the template engine.

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    #{'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    # Render response and send it back
    return render(request, 'rango/index.html', context=context_dict)
        # HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")


def about(request):
    context_dict = {'boldmessage': "Sarah!"}
    return render(request, 'rango/about.html', context=context_dict)
        # HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        if category:
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
# PAGE 91 OF TANGO WITH DJANGO
