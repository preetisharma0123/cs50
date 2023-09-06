from django.shortcuts import render
import markdown2
from markdown2 import Markdown
from . import util
import random


def index(request):
    entries = util.list_entries()   

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def md_to_html(title):
    entry = util.get_entry(title)
    markdowner = Markdown()

    if entry == None:
        return None
    else:
        return markdowner.convert(entry)

def greet(request,title):

    if md_to_html(title) == None:
        return render(request, "encyclopedia/error.html",{
        "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/greet.html",{
            "title":title,
            "entry": md_to_html(title)  
            })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        if md_to_html(entry_search) is not None:
            return render(request, "encyclopedia/greet.html",{
                "title": entry_search,
                "entry": md_to_html(entry_search )  
            })

        else:
            entries_names = util.list_entries()
            output = []
            for entry in entries_names:
                if entry_search.lower() in entry.lower():
                    output.append(entry)
            return render(request,"encyclopedia/search.html",{
            "output": output  
            })

def new_entry(request):
    if request.method == "GET":
        return render(request,"encyclopedia/new_entry.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
                return render(request,"encyclopedia/error.html",{
            "message": "Entry already Exists"  
            }) 
        else:
            util.save_entry(title,content)
            return render(request, "encyclopedia/greet.html",{
            "title": title,
            "entry": md_to_html(title)
            })           
    
def edit(request):

    if request.method =="POST":
        title   = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
            })    
    
def save_edit(request):
    if request.method =="POST":
        title   = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        return render(request, "encyclopedia/greet.html",{
            "title": title,
            "entry": md_to_html(title)
            })    

def random_page(request):
    entires = util.list_entries()
    rand_entry = random.choice(entires)
    
    return  render(request,"encyclopedia/greet.html",{
            "title": rand_entry,
            "entry": md_to_html(rand_entry)
            })    

    



