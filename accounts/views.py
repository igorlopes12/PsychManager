from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful! Welcome to your account.')
            return redirect('home_view')  # Redirect to home page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserCreationForm()
    
    # Add Bootstrap classes to form fields safely
    for field_name, field in user_form.fields.items():
        field.widget.attrs['class'] = 'form-control'
    
    return render(request, 'register.html', {'user_form': user_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home_view')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')