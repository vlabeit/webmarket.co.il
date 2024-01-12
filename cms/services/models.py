from django import forms
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalManyToManyField

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.images.edit_handlers import ImageChooserPanel

from cms.base.blocks import BaseStreamBlock

from django.utils.translation import gettext as _

@register_snippet
class Country(models.Model):
    """
    A Django model to store set of countries of origin.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/services/country/) In the ServicePage
    model you'll see we use a ForeignKey to create the relationship between
    Country and ServicePage. This allows a single relationship (e.g only one
    Country can be added) that is one-way (e.g. Country will have no way to
    access related ServicePage objects).
    """

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Countries")


@register_snippet
class ServiceProvider(models.Model):
    """
    Standard Django model that is displayed as a snippet within the admin due
    to the `@register_snippet` decorator. We use a new piece of functionality
    available to Wagtail called the ParentalManyToManyField on the ServicePage
    model to display this. The Wagtail Docs give a slightly more detailed example
    https://docs.wagtail.io/en/latest/getting_started/tutorial.html#categories
    """
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Service Providers')


@register_snippet
class ServiceType(models.Model):
    """
    A Django model to define the service type
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI. In the ServicePage model you'll see we use a ForeignKey
    to create the relationship between ServiceType and ServicePage. This allows a
    single relationship (e.g only one ServiceType can be added) that is one-way
    (e.g. ServiceType will have no way to access related ServicePage objects)
    """

    title = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("Service types")


class ServicePage(Page):
    """
    Detail view for a specific service
    """
    introduction = models.TextField(
        help_text=_('Text to describe the page'),
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Landscape mode only; horizontal width between 1000px and 3000px.')
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name=_("Page body"), blank=True
    )
    origin = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # We include related_name='+' to avoid name collisions on relationships.
    # e.g. there are two FooPage models in two different apps,
    # and they both have a FK to service_type, they'll both try to create a
    # relationship called `foopage_objects` that will throw a valueError on
    # collision.
    service_type = models.ForeignKey(
        'services.ServiceType',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    providers = ParentalManyToManyField('ServiceProvider', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('origin'),
        FieldPanel('service_type'),
        MultiFieldPanel(
            [
                FieldPanel(
                    'providers',
                    widget=forms.CheckboxSelectMultiple,
                ),
            ],
            heading=_("Additional Metadata"),
            classname=_("collapsible collapsed")
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    parent_page_types = ['ServicesIndexPage']


class ServicesIndexPage(Page):
    """
    Index page for services.

    This is more complex than other index pages on the bakery demo site as we've
    included pagination. We've separated the different aspects of the index page
    to be discrete functions to make it easier to follow
    """

    introduction = models.TextField(
        help_text=_('Text to describe the page'),
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Landscape mode only; horizontal width between 1000px and '
        '3000px.')
    )

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]

    # Can only have ServicePage children
    subpage_types = ['ServicePage']

    # Returns a queryset of ServicePage objects that are live, that are direct
    # descendants of this index page with most recent first
    def get_services(self):
        return ServicePage.objects.live().descendant_of(
            self).order_by('-first_published_at')

    # Allows child objects (e.g. ServicePage objects) to be accessible via the
    # template. We use this on the HomePage to display child items of featured
    # content
    def children(self):
        return self.get_children().specific().live()

    # Pagination for the index page. We use the `django.core.paginator` as any
    # standard Django app would, but the difference here being we have it as a
    # method on the model rather than within a view function
    def paginate(self, request, *args):
        page = request.GET.get('page')
        paginator = Paginator(self.get_services(), 12)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    # Returns the above to the get_context method that is used to populate the
    # template
    def get_context(self, request):
        context = super(ServicesIndexPage, self).get_context(request)

        # ServicePage objects (get_services) are passed through pagination
        services = self.paginate(request, self.get_services())

        context['services'] = services

        return context
