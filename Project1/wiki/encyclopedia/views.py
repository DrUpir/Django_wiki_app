from django.shortcuts import render
from markdown2 import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound

from . import util

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.get_list_entries()
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
    if request.method == "GET":
        search_string = request.GET.get("q")
        logger.error(f"search_string = {search_string}")

        if search_string:
            list_all_entries = util.get_list_entries()
            logger.error(f"list_all_entries = {list_all_entries}")

            if search_string in list_all_entries:
                return HttpResponseRedirect(reverse("entry", kwargs={'title': request.GET.get("q")}))

            list_finded_entrys = [title for title in list_all_entries if search_string.lower() in title.lower()]
            logger.error(f"list_finded_entrys = {list_finded_entrys}")

            if list_finded_entrys:
                return render(request, "encyclopedia/search.html", {
                    "entries": list_finded_entrys    
                })

    return HttpResponseNotFound('<h1>Error in search view</h1>')
   