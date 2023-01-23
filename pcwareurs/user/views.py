'''
User views
'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from user.models import Address
from checkout.models import Order
from product.models import Review

from user.forms import AddressForm

# Create your views here.
@login_required
def user_overview(request):
    '''
    User overview
    '''
    address_list = Address.objects.filter(user=request.user, is_active=True)
    order_list = Order.objects.filter(user=request.user)
    review_list = Review.objects.filter(user=request.user)

    template = 'user/user_overview.html'
    context = {
        'address_list': address_list,
        'order_list': order_list,
        'review_list': review_list
    }
    return render(request, template, context)


@login_required
def add_address(request):
    '''
    Adds address
    '''
    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            
            Address.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                street=form.cleaned_data['street'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zip=form.cleaned_data['zip'],
                country=form.cleaned_data['country']
            )
            messages.success(request, "Address has been added")
            return redirect('user_overview')

        messages.error(request, f"Form data invalid: {form.errors}")
    return render(request, 'user/add_address.html')


@login_required
def edit_address(request, address_id):
    '''
    Edit Address
    '''
    address = get_object_or_404(Address, pk=address_id)

    if address.user == request.user:

        if request.method == 'POST':

            form = AddressForm(request.POST)

            if form.is_valid():
                if address.is_used:
                    Address.objects.create(
                        user=request.user,
                        full_name=form.cleaned_data['full_name'],
                        street=form.cleaned_data['street'],
                        city=form.cleaned_data['city'],
                        state=form.cleaned_data['state'],
                        zip=form.cleaned_data['zip'],
                        country=form.cleaned_data['country']
                    )
                else:
                    address.full_name = form.cleaned_data['full_name']
                    address.street = form.cleaned_data['street']
                    address.city = form.cleaned_data['city']
                    address.state = form.cleaned_data['state']
                    address.zip = form.cleaned_data['zip']
                    address.country = form.cleaned_data['country']
                    address.save()

                messages.success(request, "Address has been edited")
                return redirect('user_overview')

            messages.error(request, "Invalid input")

        return render(request, 'user/edit_address.html', {'address': address})

    messages.error(request, "This address does not belong to you")
    return redirect('user_overview')


@login_required
def delete_address(request, address_id):
    '''
    Delete address
    '''
    address = get_object_or_404(Address, pk=address_id)

    if address.user == request.user:
        if request.method == 'POST':
            # Check if address is used
            # If it is used only set it to inactive
            # is_used refers to an order
            if address.is_used:
                address.is_active = False
                address.save()
            else:
                address.delete()
            messages.success(request, "Address has been deleted")
    else:
        messages.error(request, "Not your address")
    return redirect('user_overview')
