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
    # Main blog listing page e.g surecodes24.com/blog/
    # Shows all published blog posts as cards

    intro = models.TextField(
        blank=True,
        help_text='Intro text shown at top of blog listing page'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        category_slug = request.GET.get('category')
        # reads ?category= from URL for filtering

        blog_posts = self.get_children().live().order_by('-first_published_at')
        # get_children(): all child pages under this Blog Index Page
        # .live(): published posts only, no drafts
        # order_by: newest posts first

        if category_slug:
            blog_posts = blog_posts.filter(
                blogdetailpage__categories__slug=category_slug
            )
            # filters posts by selected category slug

        context['blog_posts'] = blog_posts
        context['categories'] = BlogCategory.objects.all()
        context['selected_category'] = category_slug
        return context


class BlogDetailPage(Page):
    # Individual blog post page e.g surecodes24.com/blog/my-post/

    date = models.DateField(
        auto_now_add=True
        # automatically sets date when post is first created
    )

    intro = models.CharField(
        max_length=300,
        help_text='Short summary shown on blog listing page'
    )

    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Main image shown at top of post and on listing cards'
    )

    categories = ParentalManyToManyField(
        'blog.BlogCategory',
        blank=True,
        help_text='Select categories for this post'
    )

    body = StreamField([
        ('heading', blocks.CharBlock(
            form_classname='title',
            help_text='Add a heading or subheading'
        )),
        # heading: single line text for section headings

        ('paragraph', blocks.RichTextBlock(
            features=[
                'h2', 'h3', 'h4',
                # heading levels
                'bold', 'italic',
                # basic formatting
                'underline',
                # underline text
                'strikethrough',
                # strikethrough text
                'ol', 'ul',
                # ordered and unordered lists
                'hr',
                # horizontal divider line
                'link',
                # hyperlinks
                'image',
                # insert images inline within paragraph
                'embed',
                # embed YouTube videos and other media
                'blockquote',
                # styled blockquote
                'code',
                # inline code formatting
            ],
            help_text='Add your main text content here'
        )),
        # paragraph: full rich text editor with all formatting tools

        ('image', ImageChooserBlock(
            help_text='Insert a full width standalone image'
        )),
        # image: picks from Wagtail image library or uploads new

        ('quote', blocks.BlockQuoteBlock(
            help_text='Add a highlighted pull quote'
        )),
        # quote: styled blockquote for key statements

        ('embed', blocks.URLBlock(
            help_text='Paste a YouTube, Twitter or video URL to embed'
        )),
        # embed: paste any URL to embed external content

        ('raw_html', blocks.RawHTMLBlock(
            help_text='Add custom HTML if needed',
            required=False
        )),
        # raw_html: for custom HTML embeds or widgets

    ], use_json_field=True)
    # use_json_field=True: required in Wagtail 4+ for StreamField

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        # makes intro and body searchable in Wagtail admin
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner_image'),
        MultiFieldPanel([
            FieldPanel('categories'),
        ], heading='Categories'),
        # MultiFieldPanel groups categories under a heading
        FieldPanel('body'),
    ]

def get_context(self, request):
    context = super().get_context(request)

    related_posts = (
        BlogDetailPage.objects
        .live()
        .exclude(pk=self.pk)                  # exclude current page
        .order_by('-first_published_at')      # newest first
        [:3]                                  # limit to 3
    )

    context['related_posts'] = related_posts
    return context