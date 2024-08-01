from django.utils import timezone
# from django.contrib import messages
from django.db import models

# Create your models here.

# from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
# from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.admin.panels import (
    FieldPanel,
    # FieldRowPanel,
    # InlinePanel,
    # MultiFieldPanel,
    PublishingPanel,
)
from wagtail.admin.filters import WagtailFilterSet
# from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
# from wagtail.contrib.settings.models import (
#     BaseGenericSetting,
#     BaseSiteSetting,
#     register_setting,
# )
# from wagtail.fields import RichTextField, StreamField
from wagtail.models import (
    # Collection,
    DraftStateMixin,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    WorkflowMixin,
)
from wagtail.search import index
# from wagtail.contrib.routable_page.models import RoutablePageMixin, route

# from taggit.models import Tag, TaggedItemBase




class Asset(
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    PreviewableMixin,
    index.Indexed,
    TranslatableMixin,
    ClusterableModel,
):

    ASSETS_STATUS = (
        ('normal', _('正常')),
        ('scrap', _('报废')),
        ('repair', _('维修')),
        ('depreciation', _('折旧')),
        ('other', _('其他')),
    )
    name = models.CharField(max_length=255, verbose_name=_("名称"))
    update_time = models.DateTimeField(verbose_name=_("更新时间"), default=timezone.now())
    sn = models.CharField(max_length=100, unique=True, verbose_name=_("序列号"))
    description = models.TextField(verbose_name=_("描述"))
    purchase_date = models.DateField(verbose_name=_("采购日期"), default=timezone.now())
    purchase_prise = models.DecimalField(default=0, decimal_places=2, verbose_name=_("采购价格"), max_digits=64)
    warranty_period = models.DateField(verbose_name=_("质保期"), default=timezone.now()+timezone.timedelta(days=365))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='asset_user', verbose_name=_("用户"))
    on_move = models.BooleanField(default=False, verbose_name=_("转交中"))
    move_to = models.OneToOneField(User, on_delete=models.CASCADE, related_name='moving_user', verbose_name=_("转交"))
    status = models.CharField(
        max_length=100,
        choices=ASSETS_STATUS,
        default='normal',
        verbose_name=_("资产状态"))

    repair_count = models.IntegerField(default=0, verbose_name=_("维修次数"))

    # translation_key = ''
    # locale = ''

    panels = [
        
        FieldPanel("name"),
        FieldPanel("update_time"),
        FieldPanel("sn"),
        FieldPanel("description"),
        FieldPanel("purchase_date"),
        FieldPanel("purchase_prise"),
        FieldPanel("warranty_period"),
        FieldPanel("user"),
        FieldPanel("on_move"),
        FieldPanel("move_to"),
        FieldPanel("status"),
        FieldPanel("repair_count"),
        PublishingPanel(),
    ]

    search_fields = [
        index.SearchField("name"),
        index.FilterField("user"),
    ]

    class Meta(TranslatableMixin.Meta):
        verbose_name = _("Asset")
        verbose_name_plural = _("Asset")


class AssetFilterSet(WagtailFilterSet):
    class Meta:
        model = Asset
        fields = ['name', 'purchase_date', 'status']


# 加一个page 前台显示当前用户的资产表格


class AssetPage(Page):
    introduction = models.TextField(help_text="Text to describe the page", blank=True)
