import logging

from cbng_interface.forms import PreferencesForm
from cbng_interface.models import Preferences
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tastypie.models import ApiKey

logger = logging.getLogger(__name__)


def bad_request(request):
    return render(request, 'cbng_interface/errors/400.html')


def permission_denied(request):
    return render(request, 'cbng_interface/errors/403.html')


def four_oh_four(request):
    return render(request, 'cbng_interface/errors/404.html')


def five_hundred(request):
    return render(request, 'cbng_interface/errors/500.html')


def signup(request):
    return render(request, 'cbng_interface/auth/signup.html')


@login_required
def profile(request):
    prefs = Preferences.objects.get(user=request.user)
    form = PreferencesForm()
    form.next_on_review = prefs.next_on_review

    if request.method == 'POST' and request.user.is_authenticated():
        form = PreferencesForm(request.POST)
        if form.is_valid():
            prefs.next_on_review = form.cleaned_data['next_on_review']
            prefs.save()
            messages.add_message(request, messages.SUCCESS, 'Preferences updated')

    data = {'form': form}
    try:
        data['api_key'] = ApiKey.objects.get(user=request.user).key
    except ApiKey.DoesNotExist:
        logger.warn('User %s does not have an API key', request.user)

    return render(request, 'cbng_interface/auth/profile.html', data)
