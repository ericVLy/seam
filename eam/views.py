# pylint: disable=R0901,protected-access
# from django.shortcuts import render
import json
import logging
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.apps import apps
from django.db.models import F
from django.contrib.auth import logout


from eam.models import Asset

log = logging.getLogger('django')

# Create your views here.

# 前台用户提交修改 post view

class LogoutView(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

class EamUserView(LoginRequiredMixin, generic.FormView):
    model = Asset

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def get_verbose_name(self, model=None):
        if model is None:
            model = self.model

    def getmodelfield(self):
        modelobj = apps.get_model(self.model._meta.app_label, self.model._meta.model_name)
        field_dic={}
        for field in modelobj._meta.fields:
            field_dic[field.name] = field.verbose_name
        return field_dic

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            print("unauthenticated request")
            return HttpResponseForbidden()
        current_user_name = self.model.objects.filter(user=request.user).values("id", "name", "sn", "description", "user__username", "on_move","status")
        current_user_response = self.model.objects.filter(move_to=request.user, on_move=True).values("id", "name", "sn", "description", "move_to__username", "on_move","status")
        verbose_name = self.getmodelfield()
        verbose_name["user__username"] = verbose_name["user"]
        verbose_name["move_to__username"] = verbose_name["move_to"]
        return JsonResponse({"current_user_name": list(current_user_name),
                             "current_user_response": list(current_user_response),
                             "field_dic": verbose_name
                             })


class EamChangeView(LoginRequiredMixin, generic.UpdateView):
    model = Asset

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        data = json.loads(request.body.decode(encoding="utf-8"))
        try:
            log.info(data)
            move_to = int(data["move_to"])
        except:
            log.info("can not make 'move_to' field to int")
            move_to = None
            return HttpResponseForbidden()
        log.info("filter table by sn")
        current = self.model.objects.filter(sn=data["sn"])
        current_value = current.values("id", "name", "sn", "user", "on_move", "status")
        if current_value[0]["user"] == request.user.id:
            log.info("update table")
            current.update(on_move=True, move_to=move_to)
            return JsonResponse(self.model.objects.filter(sn=data["sn"]).values("id",
                                                                                "name", 
                                                                                "sn", 
                                                                                "user__username", 
                                                                                "on_move", 
                                                                                "move_to__username", 
                                                                                "status")[0])
        return HttpResponseForbidden()


class EamCommitView(LoginRequiredMixin, generic.UpdateView):
    model = Asset

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        data = json.loads(request.body.decode(encoding="utf-8"))
        current = self.model.objects.filter(sn=data["sn"])
        current_value = current.values("id", "name", "sn", "user", "on_move", "move_to", "status")[0]
        if current_value["move_to"] == request.user.id and current_value["on_move"]:
            current.update(on_move=False, user=request.user)
            return JsonResponse(self.model.objects.filter(sn=data["sn"]).values("id",
                                                                                "name", 
                                                                                "sn", 
                                                                                "user__username", 
                                                                                "on_move", 
                                                                                "move_to__username", 
                                                                                "status")[0])
        return HttpResponseForbidden()


class EamRefuseView(LoginRequiredMixin, generic.UpdateView):
    model = Asset

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        data = json.loads(request.body.decode(encoding="utf-8"))
        current = self.model.objects.filter(sn=data["sn"])
        current_value = current.values("id", "name", "sn", "user", "on_move", "move_to", "status")[0]
        if current_value["move_to"] == request.user.id and current_value["on_move"]:
            current.update(on_move=False, user=current_value["user"])
            return JsonResponse(self.model.objects.filter(sn=data["sn"]).values("id",
                                                                                "name", 
                                                                                "sn", 
                                                                                "user__username", 
                                                                                "on_move", 
                                                                                "move_to__username", 
                                                                                "status")[0])
        return HttpResponseForbidden()


class GetUsersView(LoginRequiredMixin, generic.FormView):
    model = User

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return HttpResponseForbidden()

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> JsonResponse:
        data = self.model.objects.filter().values(user_id=F("id"), user_name=F("username"))
        return JsonResponse({"users": list(data)})
