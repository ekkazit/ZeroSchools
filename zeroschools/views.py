from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Author, Category, Post
from taggit.models import Tag

module = 'index'

def index(request):
	tags = Tag.objects.all()

	# get catgory and count items on it
	categories = Category.objects.extra(select={
		'post_count': 'select count(*) from blog_post a where a.category_id=blog_category.id'
	}).order_by('-post_count')[:10]

	popular_posts = Post.objects.filter(is_publish=True).order_by('-views')[:3]
	ids = popular_posts.values_list('id', flat=True)

	# get post
	posts = Post.objects.filter(is_publish=True).exclude(id__in=ids)

	# filter posts by category id
	cateid = None
	category = None
	if request.GET.get('cateid'):
		cateid = int(request.GET.get('cateid'))
		posts = posts.filter(category_id=cateid)
		category = get_object_or_404(Category, id=cateid)

	# filter posts by author id
	author = None
	authorid = None
	if request.GET.get('authorid'):
		authorid = int(request.GET.get('authorid'))
		posts = posts.filter(author=authorid)
		author = get_object_or_404(Author, id=authorid)

	# filter posts by tag id
	tag = None
	tagid = None
	if request.GET.get('tagid'):
		tagid = int(request.GET.get('tagid'))
		posts = posts.filter(tags=tagid)
		tag = get_object_or_404(Tag, id=tagid)

	# reorder posts by 'updated' with descending
	posts = posts.order_by('-created')
	paginator = Paginator(posts, 10)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'index.html', {
		'module': module,
		'categories': categories,
		'posts': posts,
		'cateid': cateid,
		'category': category,
		'author': author,
		'tag': tag,
		'tags': tags,
		'popular_posts': popular_posts,
	})



def detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	if post:
		post.views += 1
		post.save()

	# get related posts
	ids = post.tags.values_list('id', flat=True)
	related_posts = Post.objects.filter(tags__in=ids).distinct().exclude(id=post.id)[:5]

	return render(request, 'detail.html', {
		'module': module,
		'post': post,
		'related_posts': related_posts
	})
