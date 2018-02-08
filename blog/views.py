from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import PostForm, CommentForm
from .models import Post


# Create your views here.
def post_list(request):
	posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	queryset_list=Post.objects.all().order_by('-published_date')

	query=request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(text__icontains=query)|
			Q(author__username__icontains=query)
			).distinct()
		

	paginator = Paginator(queryset_list, 4)
	page = request.GET.get('page')
	try:
	    posts = paginator.page(page)
	except PageNotAnInteger:
	    
	    posts = paginator.page(1)
	except EmptyPage:
	    
	    posts = paginator.page(paginator.num_pages)



	return render(request, 'blog/post_list.html',{'posts':posts})


def post_detail(request, pk):
	post=get_object_or_404(Post,pk=pk)
	return render(request, 'blog/post_details.html', {'post':post})

def post_new(request):
	if request.method =='POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post=form.save(commit=False)
			# print(post.image)
			# print(form.cleaned_data['image'])
			# post.image = form.cleaned_data['image']
			post.author=request.user
			post.published_date=timezone.now()
			#handle_uploaded_file(request.FILES['file'])
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form=PostForm()
	
	return render(request,'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None ,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})




def add_comment(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post=post 
			comment.save()
			return redirect('post_detail', pk=post.pk)
		else:
			form = commentForm()
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment.html', {'form':form})