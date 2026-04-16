from wagtail import hooks
from wagtail.admin import messages as wagtail_messages
from django.shortcuts import redirect


@hooks.register('before_delete_page')
def prevent_blog_index_deletion(request, page):
    from blog.models import BlogIndexPage

    if isinstance(page, BlogIndexPage):
        # prevent deletion of the blog index page
        # it should always exist as the parent of all blog posts
        wagtail_messages.error(
            request,
            'The Blog Index Page cannot be deleted. '
            'It is the parent page for all blog posts. '
            'Unpublish it instead if needed.'
        )
        return redirect('wagtailadmin_explore', page.get_parent().id)
        # redirect back to parent page in admin
        # instead of deleting


@hooks.register('construct_page_chooser_queryset')
def restrict_page_types(pages, request):
    from blog.models import BlogIndexPage, BlogDetailPage
    # this hook controls which page types can be created
    # under each parent page type
    return pages