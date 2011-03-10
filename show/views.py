#coding: utf-8
import urllib2
import urllib
import json
import time
from person.models import Follow
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import F
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from show.models import Show, ShowImage

# Create your views here.

def index(request):
    return HttpResponseRedirect(reverse("show_hot"))

    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))

    show_list = Show.objects.all().order_by("-like_count", "-comment_count", "-dtcreated")
    if q:
        show_list = show_list.filter(title__icontains=q)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(show_list, 5)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("show/index.xhtml", locals(), context_instance=RequestContext(request))

def show_new(request):
    """最新的Show"""
    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))

    show_list = Show.objects.filter(is_valid=True).order_by("-dtcreated", "-like_count", "-comment_count")
    #show_list = Show.objects.filter(is_valid=True).select_related().extra(
        #select = {
            ##"popularity": '(like_count - 1) / POW(TIMESTAMPDIFF(HOUR, dtcreated, CURRENT_TIMESTAMP()) + 2, 1.5)',
            ##如果不对like_count 强制数据类型转换, 由int型转为decimal， 当0 -1 的时候，得到的結果不是 -1 而是2^64 -1
            #"popularity": '(CAST(hits AS DECIMAL) - 1) / POW(TIMESTAMPDIFF(HOUR, dtcreated, CURRENT_TIMESTAMP()) + 2, 1.5)',
        #},
        #order_by = ['-popularity', "-hits", "-dtcreated"]
    #)
    if q:
        show_list = show_list.filter(title__icontains=q)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(show_list, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("show/index.xhtml", locals(), context_instance=RequestContext(request))

def show_hot(request):
    """最热门的Show"""
    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))

    #show_list = Show.objects.all().order_by("-like_count", "-comment_count", "-dtcreated")
    #流行度的计算参考如下链接
    #http://stackoverflow.com/questions/1965341/implementing-a-popularity-algorithm-in-django

    show_list = Show.objects.filter(is_valid=True).select_related().extra(
        select = {
            #"popularity": '(like_count - 1) / POW(TIMESTAMPDIFF(HOUR, dtcreated, CURRENT_TIMESTAMP()) + 2, 1.5)',
            #如果不对like_count 强制数据类型转换, 由int型转为decimal， 当0 -1 的时候，得到的結果不是 -1 而是2^64 -1
            "popularity": '(CAST(like_count AS DECIMAL) - 1) / POW(TIMESTAMPDIFF(HOUR, dtcreated, CURRENT_TIMESTAMP()) + 2, 1.5)',
        },
        order_by = ['-popularity', "-hits", "-dtcreated"]
    )
    if q:
        show_list = show_list.filter(title__icontains=q)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(show_list, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("show/index.xhtml", locals(), context_instance=RequestContext(request))

def show_user(request, user_pk=None):
    """某个用户Show Space"""
    if user_pk is None:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_pk)

        profile = user.get_profile()
        profile.visit_count = F("visit_count") + 1
        profile.save()

    if request.user.is_authenticated():
        is_following = Follow.objects.filter(follower=request.user, followee=user).exists()
    else:
        is_following = False

    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))

    show_list = user.show_set.all()
    if q:
        show_list = show_list.filter(title__icontains=q)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(show_list, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("show/show_user.html", {
        "pages": pages,
        "show_user": user,
        "is_following": is_following,
    }, context_instance=RequestContext(request))

def show_user_likes(request, user_pk):
    """用户喜欢，收藏"""
    user = get_object_or_404(User, pk=user_pk)

    profile = user.get_profile()
    profile.visit_count = F("visit_count") + 1
    profile.save()

    if request.user.is_authenticated():
        is_following = Follow.objects.filter(follower=request.user, followee=user).exists()
    else:
        is_following = False

    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))

    show_list = user.likes.all()
    if q:
        show_list = show_list.filter(title__icontains=q)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(show_list, 10)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("show/show_user_likes.html", {
        "pages": pages,
        "show_user": user,
        "is_following": is_following,
    }, context_instance=RequestContext(request))

@login_required
def add_show(request):
    """添加Show"""
    from show.forms import ShowForm 
    form = ShowForm(request.POST or None, request.FILES or None)
    #print form
    if form.is_valid():
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
        photo.tags = request.POST.get("tags", None)
        #print photo
        return HttpResponseRedirect(reverse("show", args=[photo.pk]))
    return render_to_response("show/add-show.xhtml", locals(), context_instance=RequestContext(request))

@login_required
def edit_show(request, show_pk):
    """编辑Show"""
    from show.forms import ShowForm 
    photo = get_object_or_404(Show, pk=show_pk)
    if photo.user != request.user:
        return HttpResponseForbidden("Not Allow")
    form = ShowForm(request.POST or None, request.FILES or None, instance=photo)
    if form.is_valid():
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
        photo.tags = request.POST.get("tags", None)
        return HttpResponseRedirect(reverse("show", args=[photo.pk]))
    return render_to_response("show/edit_show.html", locals(), context_instance=RequestContext(request))

def show(request, show_pk):
    """显示某个Show页面"""
    show = Show.objects.get(pk=show_pk)

    profile = show.user.get_profile()
    profile.visit_count = F("visit_count") + 1
    profile.save()

    show_session = "show" + show_pk
    if not request.session.get(show_session, False):
        request.session[show_session] = True
        show.read_count = F("read_count") + 1
        show.save()
        show = Show.objects.get(pk=show_pk)#reload the actual value after saved
    comments = show.comments.all()
    content_type = ContentType.objects.get_for_model(show)
    from commentit.forms import CommentForm
    form = CommentForm()
    return render_to_response("show/show.xhtml", locals(), context_instance=RequestContext(request))


def show_like(request, show_pk):
    """用户喜欢收藏某个Show"""
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({"success": False}))
    show = get_object_or_404(Show, pk=show_pk)
    undo = request.GET.get("undo", False)
    if undo:
        show.likes.remove(request.user)
    else:
        show.likes.add(request.user)
    show.like_count = show.likes.count()
    show.save()

    profile = request.user.get_profile()
    profile.like_count = request.user.likes.count()
    profile.save()

    res = {"success": True, "data": {"likit_count": show.likes.count()}, "undo": undo}
    return HttpResponse(json.dumps(res))


def show_tag(request, tagname):
    """显示某个Tagname的Show列表"""
    page = int(request.GET.get("page", 1))

    #show_list = Show.objects.all().order_by("-like_count", "-comment_count", "-dtcreated")
    #流行度的计算参考如下链接
    #http://stackoverflow.com/questions/1965341/implementing-a-popularity-algorithm-in-django
    from tagging.models import TaggedItem
    show_tag_list = TaggedItem.objects.get_by_model(Show, tagname)
    show_list = show_tag_list.filter(is_valid=True).select_related().extra(
        select = {
            #"popularity": '(like_count - 1) / POW(TIMESTAMPDIFF(HOUR, dtcreated, CURRENT_TIMESTAMP()) + 2, 1.5)',
            #如果不对like_count 强制数据类型转换, 由int型转为decimal， 当0 -1 的时候，得到的結果不是 -1 而是2^64 -1
            "popularity": '(CAST(like_count AS DECIMAL) - 1) / POW(TIMESTAMPDIFF(HOUR, dtcreated, CURRENT_TIMESTAMP()) + 2, 1.5)',
        },
        order_by = ['-popularity', "-dtcreated"]
    )

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(show_list, 5)
    pages.cur_page = pages.page(page)
    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("show/index.xhtml", locals(), context_instance=RequestContext(request))

def show_tags(request):
    """显示Show tags """
    page = int(request.GET.get("page", 1))

    #show_list = Show.objects.all().order_by("-like_count", "-comment_count", "-dtcreated")
    #流行度的计算参考如下链接
    #http://stackoverflow.com/questions/1965341/implementing-a-popularity-algorithm-in-django
    from tagging.models import Tag
    tag_list = Tag.objects.cloud_for_model(Show)

    query_string = request.META.get("QUERY_STRING", u"")
    query_part = query_string.split("&")
    new_query_parts = []
    for qp in query_part:
        if not qp.startswith("page="):
            new_query_parts.append(qp)
    no_page_query_string = u"&".join(new_query_parts)

    pages = Paginator(tag_list, 200)
    pages.cur_page = pages.page(page)

    #增加tag count 分等级段，　以便以tag cloud 形式展示不同tag 显示大小
    import math
    tag_level_num = 7
    tag_max_count = max([t.count for t in pages.cur_page.object_list])
    tag_step = math.ceil(float(tag_max_count) / tag_level_num)

    for t in pages.cur_page.object_list:
        tag_level = t.count / int(tag_step) 
        setattr(t, "level", tag_level)

    pages.page_prefix_link = request.path + "?"+ no_page_query_string
    return render_to_response("show/tags.html", locals(), context_instance=RequestContext(request))

def create_sign(param,app_secret):
    import md5
    _param_list = []
    for k,v in sorted(param.items()):
        if k != "" and v != "":
            _param_list.append("%s%s" % (k,v))
    sign = app_secret + ''.join(_param_list)
    return md5.new(sign).hexdigest().upper()

@login_required
def add_by_poster(request):
    """通过taobao 画报API来发表Show"""
    if request.method == "POST":
        url = request.POST.get("taobao_huabao_url")
        import re
        url_match = re.match("http://huabao.taobao.com/\w+/d-(?P<poster_id>\d+).htm.*", url)
        if not url_match:
            return HttpResponse("URL unmatch")
        poster_id = url_match.group("poster_id")

        from settings import TAOBAO_APP_KEY, TAOBAO_APP_SECRET
        t = time.localtime()
        paramArray = {
            'app_key': TAOBAO_APP_KEY,
            'method':'taobao.huabao.poster.get',
            'format':'json',
            'v':'2.0',
            'timestamp':time.strftime('%Y-%m-%d %X', t),
            'poster_id': poster_id
        }
        # generate sign
        sign = create_sign(paramArray, TAOBAO_APP_SECRET)
        paramArray["sign"] = sign
        form_data = urllib.urlencode(paramArray)
        try:
            urlopen = urllib2.urlopen('http://gw.api.taobao.com/router/rest', form_data)
            res = urlopen.read();
            res = res.decode('utf-8')
            res_dict  = json.loads(res, strict=False)
        except:
            return HttpResponseRedirect("/show/add_by_poster")
        #print res_dict
        try:
            poster  = res_dict["huabao_poster_get_response"]["poster"]
            poster_pic_list = res_dict["huabao_poster_get_response"]["pics"]["poster_picture"]
        except Exception ,e:
            return HttpResponse(e)
        else:
            new_show, created = Show.objects.get_or_create(
                user = request.user,
                title = poster.get("title"),
                image_url = poster.get("image_url", ""),
                is_valid = True,
                quote = url,
            )
            new_show.tags = poster.get("tags")

            for p in poster_pic_list:
                image = ShowImage.objects.create(
                    show = new_show,
                    description = p.get("desc"),
                    image_url = p.get("url",""),
                )
            return HttpResponseRedirect(reverse("show", args=[new_show.pk]))
    return render_to_response("show/add_by_poster.html", locals(), context_instance=RequestContext(request))

@cache_page(60*60)
def show_sitemap(request):
    show_list = Show.objects.all()
    return render_to_response("show/sitemap.html", locals(), context_instance=RequestContext(request))
