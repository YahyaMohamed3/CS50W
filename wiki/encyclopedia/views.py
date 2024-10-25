from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django import forms
from django.shortcuts import redirect, reverse
import random

# Directory for the markdown files
ENTRIES_DIR = 'entries/'

class create_entry(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data.get("title")
        entries = util.list_entries()
        for entry in entries:
            if title.lower()== entry.lower():
                raise forms.ValidationError("There is an entry already with this title")
        return title




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_entry(request, TITLE):
    content = util.get_entry(TITLE)
    if not content:
        return render(request, "encyclopedia/error.html")
    else:
        markdowner = Markdown()
        content = markdowner.convert(content)
        return render(request, "encyclopedia/entry.html", {
            "title": TITLE,
            "content": content
        })

def search_entry(request):
    query = request.GET.get("q")
    if query:
        content = util.get_entry(query)
        if content:
            markdowner = Markdown()
            content = markdowner.convert(content)
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": content
            })
        else:
            matching_entries = []
            entries = default_storage.listdir(ENTRIES_DIR)[1]

            for entry_file in entries:
                if entry_file.endswith('.md'):
                    entry_name = entry_file[:-3]
                    if query.lower() in entry_name.lower():
                        matching_entries.append(entry_name)

            return render(request, 'encyclopedia/search_results.html', {
                'query': query,
                'results': matching_entries,
            })
    else:
        return render(request, 'encyclopedia/search_results.html', {
            'query': '',
            'results': [],
        })


def new_entry(request):
    if request.method == "POST":
        form = create_entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title , content)
            return redirect(reverse('wiki:get_entry', kwargs={'TITLE': title}))
        else:
            return render(request, "encyclopedia/new_entry.html", {"form": form})
    else:
        form = create_entry()
        return render(request, "encyclopedia/new_entry.html", {"form": form})


def edit_entry(request , TITLE):
    if request.method == "GET":
       content = util.get_entry(TITLE)
       return render(request , "encyclopedia/edit_entry.html", {"content" :content , "title" : TITLE})
    else:
        edited_content = request.POST.get("content")
        util.save_entry(TITLE , edited_content)
        return redirect(reverse("wiki:get_entry", kwargs={"TITLE": TITLE}))

def random_page(request):
    if request.method == "GET":
        entries = util.list_entries()
        if entries:
            title = random.choice(entries)
            return redirect(reverse("wiki:get_entry", kwargs={"TITLE": title}))
        else:
            return HttpResponse("There are no entries")
    else:
        return redirect(reverse("wiki:index"))
