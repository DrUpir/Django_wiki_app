from django.shortcuts import render
from markdown2 import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_md_content = util.get_entry(title)
    if not entry_md_content:
        entry_md_content = f"##**{title}** entry doesn't exist"
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry_html_content": markdown(entry_md_content)
    })

def search(request):
    if request.method == "GET" and request.GET.get("q"):
        return HttpResponseRedirect(reverse("entry", kwargs={'title': request.GET.get("q")}))
    return HttpResponseNotFound('<h1>Error in search view</h1>')
   