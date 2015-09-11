from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin, Page

class LinkBox(CMSPlugin):
    """
    A Link Box
    """

    TARGET_CHOICES = (
        ('_blank',  'Opens in a new window'),
        ('_self', 'Opens in the same window')
        )

    TEMPLATE_CHOICES = (
        ('cms/plugins/link_box.html',  'BOX - Link box with a clickable button'),
        ('cms/plugins/link_image.html', 'IMAGE - Featured image with no button (for logos etc...)')
        )

    title = models.CharField("Title", max_length=255)
    image = models.ImageField("Image", upload_to='linkbox', blank=True, null=True)
    link_text = models.CharField("Link/Button text", max_length=255, blank=True, null=True, help_text=_("Text to use for the link."))
    page_link = models.ForeignKey(
        Page, 
        verbose_name=_("page"), 
        help_text=_("If set the link will automatically goto this page"), 
        blank=True, 
        null=True, 
        limit_choices_to={'publisher_is_draft': True}
    )
    url = models.CharField("Link", max_length=255, blank=True, null=True, help_text=_("If present image will be clickable."))
    url_target =  models.CharField("Link Target", max_length=255, blank=True, null=True, choices=TARGET_CHOICES, help_text="If present image will be clickable.")
    description = models.TextField("Description", blank=True, null=True, default="<p></p>")
    template =  models.CharField("Template", max_length=255, default='cms/plugins/link_box.html', choices=TEMPLATE_CHOICES, help_text="Template that will be used to display this link")


    def __unicode__(self):
        return self.title
            

    search_fields = ('description',)
