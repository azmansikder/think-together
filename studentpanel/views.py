from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project, SavedResearch, Message
from .forms import ProjectForm, MessageForm
from researchpanel.models import ResearchPost, Collaboration
from accounts.models import CustomUser

# ==========================================
# 1. DECORATOR
# ==========================================
def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role != 'student':
            return redirect('researchpanel:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# ==========================================
# 2. COLLABORATION VIEWS
# ==========================================
@student_required
def browse_researchers(request):
    researchers = CustomUser.objects.filter(role='researcher')
    return render(request, 'studentpanel/browse_researchers.html', {'researchers': researchers})

@student_required
def request_collaboration(request, researcher_id):
    researcher = get_object_or_404(CustomUser, pk=researcher_id, role='researcher')
    if request.method == 'POST':
        topic = request.POST.get('topic', '')
        message = request.POST.get('message', '')
        
        # Check jodi already pending request thake
        if Collaboration.objects.filter(researcher=researcher, student=request.user, status='pending').exists():
            messages.warning(request, 'You already have a pending request for this researcher.')
        else:
            Collaboration.objects.create(
                researcher=researcher,
                student=request.user,
                topic=topic,
                message=message
            )
            messages.success(request, f'Request sent to {researcher.first_name}!')
            return redirect('studentpanel:my_collaborations')
            
    return render(request, 'studentpanel/request_collaboration.html', {'researcher': researcher})

@student_required
def my_collaborations(request):
    # Sothik query: Ekhane shudhu 'researcher' thakbe
    collabs = Collaboration.objects.filter(student=request.user).select_related('researcher')
    return render(request, 'studentpanel/my_collaborations.html', {'collabs': collabs})


# ==========================================
# 3. DASHBOARD & PROJECT VIEWS
# ==========================================
@student_required
def dashboard(request):
    projects = Project.objects.filter(student=request.user)[:5]
    recent_research = ResearchPost.objects.all().order_by('-created_at')[:6]
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False).count()
    saved_count = SavedResearch.objects.filter(student=request.user).count()
    context = {
        'projects': projects,
        'recent_research': recent_research,
        'unread_messages': unread_messages,
        'saved_count': saved_count,
        'total_projects': Project.objects.filter(student=request.user).count(),
    }
    return render(request, 'studentpanel/dashboard.html', context)

@student_required
def my_projects(request):
    projects = Project.objects.filter(student=request.user)
    return render(request, 'studentpanel/my_projects.html', {'projects': projects})

@student_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = request.user
            project.save()
            messages.success(request, 'Project created successfully!')
            return redirect('studentpanel:my_projects')
    else:
        form = ProjectForm()
    return render(request, 'studentpanel/create_project.html', {'form': form})

@student_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, student=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated!')
            return redirect('studentpanel:my_projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'studentpanel/create_project.html', {'form': form, 'edit': True})

@student_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, student=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
        return redirect('studentpanel:my_projects')
    return render(request, 'studentpanel/confirm_delete.html', {'project': project})


# ==========================================
# 4. RESEARCH POST VIEWS
# ==========================================
@student_required
def search_research(request):
    query = request.GET.get('q', '')
    field = request.GET.get('field', '')
    results = ResearchPost.objects.all()
    if query:
        results = results.filter(Q(title__icontains=query) | Q(abstract__icontains=query) | Q(tags__icontains=query))
    if field:
        results = results.filter(field__icontains=field)
    return render(request, 'studentpanel/search_research.html', {'results': results, 'query': query, 'field': field})

@student_required
def save_research(request, pk):
    research = get_object_or_404(ResearchPost, pk=pk)
    _, created = SavedResearch.objects.get_or_create(student=request.user, research=research)
    if created:
        messages.success(request, 'Research saved!')
    else:
        messages.info(request, 'Already saved.')
    return redirect('studentpanel:search_research')

@student_required
def saved_research(request):
    saved = SavedResearch.objects.filter(student=request.user).select_related('research')
    return render(request, 'studentpanel/saved_research.html', {'saved': saved})


# ==========================================
# 5. MESSAGES & NOTIFICATIONS
# ==========================================
@student_required
def messages_view(request):
    researchers = CustomUser.objects.filter(role='researcher')
    # GET ba POST jekonotai hok, user_id niche
    selected_user_id = request.GET.get('user') or request.POST.get('user_id')
    selected_user = None
    conversation = []

    if selected_user_id:
        selected_user = get_object_or_404(CustomUser, pk=selected_user_id)
        
        # Sothik filter: student pathaise emon message OR researcher pathaise emon message
        conversation = Message.objects.filter(
            Q(sender=request.user, receiver=selected_user) |
            Q(sender=selected_user, receiver=request.user)
        ).order_by('created_at') # Somoy onujayi sajano
        
        # Unread message-ke read mark kora
        Message.objects.filter(sender=selected_user, receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST' and selected_user:
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user, 
                receiver=selected_user, 
                content=content
            )
        return redirect(f'{request.path}?user={selected_user.id}')

    context = {
        'researchers': researchers,
        'selected_user': selected_user,
        'conversation': conversation,
    }
    return render(request, 'studentpanel/messages.html', context)
@student_required
def notifications(request):
    unread = Message.objects.filter(receiver=request.user, is_read=False).select_related('sender')
    return render(request, 'studentpanel/notifications.html', {'messages_list': unread})