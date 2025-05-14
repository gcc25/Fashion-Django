from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile, Wishlist
from .forms import UserProfileForm
from products.models import Product


@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def wishlist_view(request):
    # Get or create wishlist
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'users/wishlist.html', {'wishlist': wishlist})


@login_required
def wishlist_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'info', 'message': 'Product already in wishlist'})
        messages.info(request, "This product is already in your wishlist.")
    else:
        wishlist.products.add(product)
        wishlist.save()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Product added to wishlist'})
        messages.success(request, "Product added to your wishlist.")
    
    next_url = request.GET.get('next', 'products:product_detail')
    if next_url == 'products:product_detail':
        return redirect(next_url, slug=product.slug)
    return redirect(next_url)


@login_required
def wishlist_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Product removed from wishlist'})
        messages.success(request, "Product removed from your wishlist.")
    
    next_url = request.GET.get('next', 'users:wishlist')
    if next_url == 'products:product_detail':
        return redirect(next_url, slug=product.slug)
    return redirect(next_url)