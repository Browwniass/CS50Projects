from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
import random

from . import util

def search(request):    
    if request.method == "GET":
        title = request.GET.get('q')
        if util.get_entry(title):        
            return render(request, "encyclopedia/page.html", {
                "title": title, "content": markdown2.markdown(util.get_entry(title))
            })
        else:      
            res=[string for string in util.list_entries() if title.casefold() in string.casefold()]
            return render(request, "encyclopedia/search.html", {
            "entries": res
            })

def edit(request):
    if request.GET.get('edit_input'):       
        pre_title = request.GET.get('edit_input')
        pre_content = util.get_entry(pre_title)
        return render(request, "encyclopedia/edit.html", {
                "title": pre_title, "content": pre_content})
    if request.method == "POST":
        content = request.POST.get('create_entries')
        title = request.POST.get('title_input')
        util.save_entry(title, content)
        return HttpResponseRedirect(f"/wiki/{title}")           

def add(request):
    #print(request.POST.get('create_entries'))
    if request.method == "POST":
               
        content = request.POST.get('create_entries')
        title = request.POST.get('title_input')
        if not util.get_entry(title):
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            messages.error(request, "Page with this name already exist")

    return render(request, "encyclopedia/add.html")
             
def index(request):
    if request.method == "GET":
        print(random.choice(util.list_entries()))
        title = random.choice(util.list_entries())
        return render(request, "encyclopedia/page.html", {
            "title": title, "content": markdown2.markdown(util.get_entry(title))
        })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random_page(request):   
    print(random.choice(util.list_entries()))
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/page.html", {
        "title": title, "content": markdown2.markdown(util.get_entry(title))
    })
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    if util.get_entry(title):
            return render(request, "encyclopedia/page.html", {
        "title": title, "content": markdown2.markdown(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/error.html")

