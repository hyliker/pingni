#coding: utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from person.forms import ProfileForm 
from person.models import Profile
from django.db.models import F
from person.models import Follow
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
# Create your views here.

@login_required
def settings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile, initial={"email": request.user.email})
    if form.is_valid():
        profile = form.save()
        profile.save()
        profile.user.email = form.cleaned_data.get("email")
        profile.user.save()
        form.success = True
    return render_to_response("person/settings.xhtml", {
        "form": form,
    }, context_instance=RequestContext(request))

def register(request):
    from person.forms import RegisterForm
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        password = form.cleaned_data.get("password")
        from django.contrib.auth import authenticate
        user = authenticate(username=user.username, password=password)
        from django.contrib.auth import login
        login(request, user)

        profile, created = Profile.objects.get_or_create(user=request.user)

        return HttpResponseRedirect("/")
    return render_to_response("person/register_form.html", {
       "site": u"PingNi.com",
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def password_change(request):
    from django.contrib.auth.forms import PasswordChangeForm
    form = PasswordChangeForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")
    return render_to_response("person/password_change.html", {
        "form": form,
    }, context_instance=RequestContext(request))


@login_required
def following(request, user_pk, undo=False):
    followee = get_object_or_404(User, pk=user_pk)

    if undo:
        try:
            follow = Follow.objects.get(follower=request.user, followee=followee)
        except Follow.DoesNotExist, e:
            return HttpResponse("Not Exist")
        else:
            follow.delete()
    else: #create follow
        follow, created = Follow.objects.get_or_create(follower=request.user, followee=followee)

    if request.is_ajax():
        res = {"success": True}
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

def follower(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    profile = user.get_profile()
    profile.visit_count = F("visit_count") + 1
    profile.save()

    follow_list = user.followers.all()

    if request.user.is_authenticated():
        is_following = Follow.objects.filter(follower=request.user, followee=user).exists()
    else:
        is_following = False

    page = int(request.GET.get("page", 1))

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(follow_list, 30)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("person/follower.html", {
        "follow_list": follow_list,
        "show_user": user,
        "pages": pages,
        "is_following": is_following,
    }, context_instance=RequestContext(request))


def followee(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    profile = user.get_profile()
    profile.visit_count = F("visit_count") + 1
    profile.save()

    follow_list = user.followees.all()

    if request.user.is_authenticated():
        is_following = Follow.objects.filter(follower=request.user, followee=user).exists()
    else:
        is_following = False

    page = int(request.GET.get("page", 1))

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(follow_list, 30)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string

    return render_to_response("person/followee.html", {
        "follow_list": follow_list,
        "show_user": user,
        "pages": pages,
        "is_following": is_following,
    }, context_instance=RequestContext(request))
