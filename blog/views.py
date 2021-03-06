from builtins import StopIteration

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, \
				  PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.db.models import Count
from haystack.query import SearchQuerySet


# Create your views here.
def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    # List of similar posts

    return render(request,'blog/post/list.html',{'page' : page, 'posts': posts})
		    

# 
# POST - requst przechodzi w takiej metodzie gdy formularz jest przeslany
# Czy rozdzelenie tutaj zapisania komentarza do bazy danych ma tutaj sens ? Tak, bo nowy komentarz bedzie mial przypisany post.
#
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
				    status='published',
				    publish__year=year,
				    publish__month = month,
				    publish__day = day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    
    if request.method == 'POST':
	# A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create comment, but not save it in database
            new_comment = comment_form.save(commit=False)
            # Assign commend to post
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,'blog/post/detail.html',{'post': post, 'comments': comments, 'comment_form': comment_form})
    
    
def post_share(request, post_id):
    # Retrieve post by id
    # Class name, first parameter, second parameter. Method to get access to model
    post = get_object_or_404(Post, id=post_id, status='published') 
    sent = False

    if request.method == 'POST':
	# Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
	    # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,post.get_absolute_url,cd['name'],cd['comments'])
            send_mail(subject,message,'tziss85@gmail.com',[cd['to']])
            sent = True
            ## Number of posts share
            post.sharecnt += 1
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html', {'post' : post,'form' : form, 'sent' : sent})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

# Python 3.7 fix - StopIterator exception raised
# PEP 479
def post_search(request):
    try:
        cd = None
        results = None
        total_results = None
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                cd = form.cleaned_data
                results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
                total_results = results.count()
        else:
                form = SearchForm()
        return render(request,
                      'blog/post/search.html',
                      {'form': form,
                       'cd': cd,
                       'results': results,
                       'total_results': total_results})
    except RuntimeError:
        return render(request,
                      'blog/post/search.html',
                      {'form': form,
                       'cd': cd,
                       'results': results,
                       'total_results': total_results})

