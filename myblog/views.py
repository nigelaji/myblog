from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Post, MDExampleModel
from .forms import LoginForm, ArticleForm, MarkdownForm, TestForm
from .tools.markdown_to_html import md_to_html
from django.utils.safestring import mark_safe


def test(request):
    content = MDExampleModel.objects.all().get()
    content = md_to_html(content.content)

    return render(
        request,
        'myblog/test.html',
        {'pagedata':
             {'content': content}
        }
    )

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(
            request,
            'myblog/login.html',
            {'pagedata':
                 {'form': form},
            }
        )
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username, password = form.cleaned_data.values()
            user = auth.authenticate(request, username=username, password=password)
            if user != None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponseRedirect(reverse('article_list'))
            else:
                return render(
                    request,
                    'myblog/login.html',
                    {'pagedata':
                         {'form': form},
                    }
                )
        else:
            return render(
                request,
                'myblog/login.html',
                {'pagedata':
                     {'form': form},
                }
            )

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    post_list = Post.objects.all()
    return render(
        request,
        'myblog/index.html',
        {'pagedata':
             {'post_list':post_list}
        }
    )

def article(request, key):
    post = Post.objects.filter(key=key).get()
    return render(
        request,
        'myblog/article.html',
        {'pagedata':
             {'post': post}
        }
    )

@login_required(login_url='login')
def article_list(request):
    post_list = Post.objects.all()
    return render(
        request,
        'myblog/articles_list.html',
        {'pagedata':
             {'post_list': post_list}
        }
    )

@login_required(login_url='login')
def addArticle(request):
    if request.method == 'GET':
        form = ArticleForm()
        return render(
            request,
            'myblog/add_article.html',
            {'pagedata':
                 {'form':form}
            }
        )
    elif request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('article_list'))
        else:
            return render(
                request,
                'myblog/add_article.html',
                {'pagedata':
                     {'form': form}
                }
            )

@login_required(login_url='login')
def modifyArticle(request, key):
    if request.method == 'GET':
        post_list = Post.objects.filter(key=key)
        if len(post_list) == 0:
            return HttpResponse('文章不存在')
        else:
            article_form = ArticleForm(instance=post_list[0])

            return render(
                request,
                'myblog/modify_article.html',
                {'pagedata':
                     {
                        'form':article_form,
                        'post':post_list[0]
                     }
                }
            )
    elif request.method == 'POST':
        key = request.POST['key']
        article_form = ArticleForm(request.POST)
        post = Post.objects.filter(key=key)[0]

        if article_form.is_valid():
            article_form.modify(key=key)
        else:
            return render(
                request,
                'myblog/modify_article.html',
                {'pagedata':
                    {
                        'form': article_form,
                        'post': post
                    }
                }
            )

        return HttpResponseRedirect(reverse('article_list'))

@login_required(login_url='lgoin')
def deleteArticle(request, key):
    if request.method == 'GET':
        post = Post.objects.filter(key=key)[0]

        return render(
            request,
            'myblog/delete_confirm.html',
            {'pagedata':
                 {'post':post}
            }
        )
    elif request.method == 'POST':
        Post.objects.filter(key=key).delete()

        return HttpResponseRedirect(reverse('article_list'))
