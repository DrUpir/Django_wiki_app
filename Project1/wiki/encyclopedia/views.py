from django.shortcuts import render
from markdown2 import markdown

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

