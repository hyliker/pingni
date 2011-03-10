#coding: utf-8
# Create your views here.
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from show.models import Show
from commentit.models import Comment
from commentit.forms import CommentForm

def add_comment(request):
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({"success": False, "errors": u"你还没有登陆, 请登陆后再发表评论"}))

    form = CommentForm(request.POST or None)
    if form.is_valid():
        content_type_id = request.POST.get("content_type_id", 0)
        content_type = ContentType.objects.get(pk=content_type_id)
        object_id = request.POST.get("object_id", "")
        content = request.POST.get("content", "")
        ip_address = request.META.get("REMOTE_ADDR", None)
        human = True
        if request.user.is_authenticated():
            author = request.user
        else:
            author = None
        try:
            comment = Comment(
                author = author,
                content = content,
                ip_address = ip_address,
                content_type = content_type,
                object_id = object_id
            )
            comment.save()
        except Exception,e:
            success = False
        else:
            success = True
    else:
        success = False
        human = False

    if request.is_ajax():
        return HttpResponse(json.dumps({"success": success}))
    else:
        referer = request.META.get("HTTP_REFERER", None)
        if referer:
            referer = "%s#submit-comment" % referer
        else:
            referer = "/"
        return HttpResponseRedirect(referer)


def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.author == request.user:
        try:
            comment.delete()
            is_success = True
        except:
            is_success = False
    if request.is_ajax():
        res = {"success": is_success}
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
