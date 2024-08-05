from django.shortcuts import render, redirect
from django import forms
from . import util
import markdown2
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title")
    content = forms.CharField(widget=forms.Textarea, label="Page Content")

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Edit Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is  None:
        return render(request, "encyclopedia/error.html", {
             "message": "Oops... this page was not found."         
        })

    else:
        html_content = markdown2.markdown(entry_content)
        return render(request,"encyclopedia/entry.html" , {
        "title": title, 
        "content": html_content
    })

def search(request):
    query = request.GET.get('q', '')
   
    if query:
        entries = util.list_entries()
        if query.lower() in [entry.lower() for entry in entries]:
         return redirect('entry', title=query)
        
        else:
            results = [entry for entry in entries if query.lower() in entry.lower()]
            return render(request, "encyclopedia/search_results.html", {
                "query": query,
                "results": results
            })
        
    else:
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": []
            })
    
def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": "An entry with that title already exists."
                })
            
            content = f"# {title}\n\n{content}"
            util.save_entry(title, content)
            return redirect("entry", title=title)
    
    else:
        form = NewPageForm()

    return render(request, "encyclopedia/create.html", {"form": form})



def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("entry", title=title)
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form            
            })

    else:
            content = util.get_entry(title)
            form = EditPageForm(initial={'content': content})
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })
    
def random_page(request):
    entries = util.list_entries()
    selected_entry = random.choice(entries)
    return redirect('entry', title=selected_entry)
