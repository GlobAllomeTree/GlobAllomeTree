from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from .models import LinkBox

class LinkBoxPlugin(CMSPluginBase):
    model = LinkBox
    name = _("Link box")
    
    
    def render(self, context, instance, placeholder):
        if instance.url:
            link = instance.url
        elif instance.page_link:
            link = instance.page_link.get_absolute_url()
        else:
            link = ""
        context.update({
            'object':instance, 
            'placeholder':placeholder,
            'link':link
        })

        return context 
 
    def get_render_template(self, context, instance, placeholder ):
        return instance.template

plugin_pool.register_plugin(LinkBoxPlugin)