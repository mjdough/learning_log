from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log """
    return render(request, 'learning_logs/index.html')
    
def topics(request):
    """Show all topics """
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
    
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
    
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        #No data submitted; create blank form
        form = TopicForm()
    else:
        #POST data submitted; process data
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
            
    content = {'form': form}
    return render(request, 'learning_logs/new_topic.html', content)
    
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        #No data submitted; create blank form
        form = EntryForm()
    else:
        #POST data submitted; process data
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
            
    content = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', content)
    
def edit_entry(request, entry_id):
    """Edit an exiting entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
        
    if request.method != 'POST':
        #Initial request; pre-fill form with current entry
        form = EntryForm(instance=entry)
    else:
        #POST data submitted; process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
                
    content = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', content)
    