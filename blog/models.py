from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PublishingPanel
from wagtail.search import index
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalManyToManyField


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    # Category name e.g "Betting Tips", "Match Previews"

    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text='URL friendly version e.g betting-tips'
    )

    description = models.TextField(
        blank=True,
        help_text='Optional short description of this category'
    )

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
    template = 'blog/blog_index_page.html'

    subpage_types = ['blog.BlogDetailPage']
    # only blog posts can be created under blog index

    parent_page_types = ['bookings.HomePage']
    # ✅ references bookings.HomePage not blog.HomePage
    # since HomePage lives in bookings app

    intro = models.TextField(blank=True)
    # ... rest of the model unchanged

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
    template = 'blog/blog_detail_page.html'

    # restrict: no child pages can be created under a blog post
    subpage_types = []
    # empty list: means NO page types can be created under BlogDetailPage
    # prevents creating posts under posts

    # restrict: BlogDetailPage can only be created under BlogIndexPage
    parent_page_types = ['blog.BlogIndexPage']
    # prevents creating a blog post anywhere other than under the blog index

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
            features=[
                'h2', 'h3', 'h4',
                'bold', 'italic',
                'underline',
                'strikethrough',
                'ol', 'ul',
                'hr',
                'link',
                'image',
                'embed',
                'blockquote',
                'code',
            ],
            help_text='Add your main text content here'
        )),
        ('image', ImageChooserBlock(
            help_text='Insert a full width standalone image'
        )),
        ('quote', blocks.BlockQuoteBlock(
            help_text='Add a highlighted pull quote'
        )),
        ('embed', blocks.URLBlock(
            help_text='Paste a YouTube, Twitter or video URL to embed'
        )),
        ('raw_html', blocks.RawHTMLBlock(
            help_text='Add custom HTML if needed',
            required=False
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
