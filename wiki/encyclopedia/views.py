from django.shortcuts import render
from markdown2 import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
import logging # import the logging library
from django import forms

from . import util

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CreateNew_Form (forms.Form):
    title = forms.CharField(label = "Title")
    MD = forms.CharField(widget = forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.get_list_entries()
    })

def entry(request, title):
    entry_md_content = util.get_entry(title)

    if not entry_md_content:
        return render(request, "encyclopedia/error.html", {
            "error_string":  f"\"{title}\" entry doesn't exist"
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry_html_content": markdown(entry_md_content)
    })

def search(request):
    if request.method == "GET":
        search_string = request.GET.get("q")
        logger.error(f"search_string = {search_string}")

        if search_string:
            list_all_entries = util.get_list_entries()
            logger.error(f"list_all_entries = {list_all_entries}")

            if [s for s in list_all_entries if search_string.lower() == s.lower()]:
                return HttpResponseRedirect(reverse("entry", kwargs={'title': search_string}))

            list_finded_entrys = [s for s in list_all_entries if search_string.lower() in s.lower()]
            logger.error(f"list_finded_entrys = {list_finded_entrys}")

            if list_finded_entrys:
                return render(request, "encyclopedia/search.html", {
                    "entries": list_finded_entrys    
                })

    return render(request, "encyclopedia/error.html", {
        "error_string":  f"can't find \"{search_string}\""
    })

def create(request):
    if request.method == "POST":
        form = CreateNew_Form(request.POST)
        if form.is_valid():
            # check for existed title in entries
            # check for correct MD format
            #util.save_entry(r)
            pass

        return render(request, "encyclopedia/error.html", {
            "error_string":  f"Error with POST create new entry"
        })

    return render(request, "encyclopedia/create.html", {
        'form': CreateNew_Form()
    })
   