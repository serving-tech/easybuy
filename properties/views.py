
from django.shortcuts import render, redirect, get_object_or_404
from properties.forms import CustomerForm
from properties.models import Customer, Property, Partners, Testimonials
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal, InvalidOperation
from django.db.models import Q
from django.contrib import messages



# View for the About page
def about(request):
    return render(request, 'about.html')


# View to display all agents
def agents(request):
    agents = Partners.objects.all()
    return render(request, 'agents.html', {'agents': agents})


# View for the contact form
def contact(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been sent successfully.')
            return redirect('contact')  # Redirect to the same page or another page
    else:
        form = CustomerForm()
    return render(request, 'contact.html', {'form': form})


# Home page or landing page
def index(request):
    agents = Partners.objects.all()
    testimonials = Testimonials.objects.all()
    featured = Property.objects.filter(is_featured=True)
    context = {
        'agents': agents,
        'testimonials': testimonials,
        'featured': featured
    }
    return render(request, 'index.html', context)


def properties(request):
    properties_list = Property.objects.all()
    valid_properties = []

    for property in properties_list:
        try:
            if property.price not in (None, ''):
                property.price = Decimal(property.price)
            if property.area not in (None, ''):
                property.area = Decimal(property.area)
            valid_properties.append(property)
        except (InvalidOperation, TypeError):
            property.price = Decimal(0.0)
            property.area = Decimal(0.0)
            valid_properties.append(property)

    # Pagination logic
    page = request.GET.get('page', 1)  # Get the current page number from the request
    paginator = Paginator(valid_properties, 10)  # Show 10 properties per page

    try:
        paginated_properties = paginator.page(page)
    except PageNotAnInteger:
        paginated_properties = paginator.page(1)  # Default to the first page
    except EmptyPage:
        paginated_properties = paginator.page(paginator.num_pages)  # Default to the last page

    context = {'properties': paginated_properties}
    return render(request, 'properties.html', context)



# View for displaying a single property details
def propertysingle(request, property_id):
    single_property = get_object_or_404(Property, id=property_id)
    context = {'single': single_property}
    return render(request, 'propertysingle.html', context)


# View for service details
def servicedetails(request):
    return render(request, 'servicedetails.html')


# View for displaying services offered
def services(request):
    return render(request, 'services.html')

def search(request):
    query = request.GET.get('query', '')
    if query:
        searched = Property.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(status__icontains=query) |
            Q(price__icontains=query) |
            Q(area__icontains=query) |
            Q(baths__icontains=query) |
            Q(garage__icontains=query) |
            Q(key__icontains=query) |
            Q(propertytyp__icontains=query)
        ).order_by('title')  # Explicitly order the QuerySet
        if not searched.exists():
            messages.warning(request, 'No results found for your search query.')
    else:
        searched = Property.objects.none()  # Return empty queryset if no query
        messages.info(request, 'Please enter a search query.')

    paginator = Paginator(searched, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {'searched': searched, 'page_obj': page_obj, 'query': query})

# Custom 404 page not found view
def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

