from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from django.utils.translation import gettext_lazy as _

from eam.models import Asset, AssetFilterSet



# class AssetSnippetsCreateView(CreateView):
#     template_name = "templates/wagtailsnippets/snippets/create.html"


class AssetSnippetViewSet(SnippetViewSet):
    model = Asset
    # add_view_class = AssetSnippetsCreateView
    menu_label = _("Asset")  # ditch this to use verbose_name_plural from model
    icon = "clipboard-list"  # change as required
    copy_view_enabled = False
    list_display = ("name",
                    "update_time",
                    "sn",
                    "description",
                    "purchase_date",
                    "purchase_prise",
                    "warranty_period",
                    "user",
                    "status",
                    "repair_count",
                    )
    # list_filter = {
    #     "job_title": ["icontains"],
    # }
    list_export = ("name",
                   "update_time",
                   "sn",
                   "description",
                   "purchase_date",
                   "purchase_prise",
                   "warranty_period",
                   "user",
                   "status",
                   "repair_count",
                   )

    filterset_class = AssetFilterSet



class MattersSnippetViewSetGroup(SnippetViewSetGroup):
    menu_label = _("Assets")
    menu_icon = "folder"  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (AssetSnippetViewSet,)


register_snippet(MattersSnippetViewSetGroup)
