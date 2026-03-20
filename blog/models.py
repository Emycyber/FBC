from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
# PromotePanels are already built into Wagtail's Page model
# no extra import needed


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]

    class Meta:
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogIndexPage(Page):
    intro = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        category_slug = request.GET.get('category')
        blog_posts = self.get_children().live().order_by('-first_published_at')
        if category_slug:
            blog_posts = blog_posts.filter(
                blogdetailpage__categories__slug=category_slug
            )
        context['blog_posts'] = blog_posts
        context['categories'] = BlogCategory.objects.all()
        context['selected_category'] = category_slug
        return context


class BlogDetailPage(Page):
    date = models.DateField(auto_now_add=True)
    intro = models.CharField(max_length=300)

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    body = StreamField([
        ('heading', blocks.CharBlock(
            form_classname='title',
            help_text='Add a heading or subheading'
        )),
        ('paragraph', blocks.RichTextBlock(
            features=['bold', 'italic', 'link', 'ol', 'ul', 'hr'],
            help_text='Add your main text content here'
        )),
        ('image', ImageChooserBlock(
            help_text='Insert an image anywhere in the post'
        )),
        ('quote', blocks.BlockQuoteBlock(
            help_text='Add a highlighted quote or key point'
        )),
    ], use_json_field=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner_image'),
        MultiFieldPanel([
            FieldPanel('categories'),
        ], heading='Categories'),
        FieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        related_posts = BlogDetailPage.objects.live().exclude(
            pk=self.pk
        ).filter(
            categories__in=self.categories.all()
        ).distinct().order_by('-first_published_at')[:3]

        if not related_posts:
            related_posts = BlogDetailPage.objects.live().exclude(
                pk=self.pk
            ).order_by('-first_published_at')[:3]

        context['related_posts'] = related_posts
        return context