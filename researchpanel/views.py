from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ResearchPost, Collaboration
from .forms import ResearchPostForm
from studentpanel.models import Message
from accounts.models import CustomUser

# ==========================================
# 1. DECORATOR
# ==========================================
def researcher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role != 'researcher':
            return redirect('studentpanel:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# ==========================================
# 2. DASHBOARD & RESEARCH CRUD VIEWS
# ==========================================
@researcher_required
def dashboard(request):
    posts = ResearchPost.objects.filter(researcher=request.user)
    total_views = sum(p.views_count for p in posts)
    pending_collabs = Collaboration.objects.filter(researcher=request.user, status='pending').count()
    unread_messages = Message.objects.filter(receiver=request.user, is_read=False).count()
    recent_posts = posts.order_by('-created_at')[:5]
    
    context = {
        'total_posts': posts.count(),
        'published_posts': posts.filter(status='published').count(),
        'total_views': total_views,
        'pending_collabs': pending_collabs,
        'unread_messages': unread_messages,
        'recent_posts': recent_posts,
    }
    return render(request, 'researchpanel/dashboard.html', context)

@researcher_required
def my_research(request):
    posts = ResearchPost.objects.filter(researcher=request.user)
    return render(request, 'researchpanel/my_research.html', {'posts': posts})

@researcher_required
def create_research(request):
    if request.method == 'POST':
        form = ResearchPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.researcher = request.user
            post.save()
            messages.success(request, 'Research post created!')
            return redirect('researchpanel:my_research')
    else:
        form = ResearchPostForm()
    return render(request, 'researchpanel/create_research.html', {'form': form})

@researcher_required
def edit_research(request, pk):
    post = get_object_or_404(ResearchPost, pk=pk, researcher=request.user)
    if request.method == 'POST':
        form = ResearchPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Research updated!')
            return redirect('researchpanel:my_research')
    else:
        form = ResearchPostForm(instance=post)
    return render(request, 'researchpanel/create_research.html', {'form': form, 'edit': True})

@researcher_required
def delete_research(request, pk):
    post = get_object_or_404(ResearchPost, pk=pk, researcher=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Research deleted.')
        return redirect('researchpanel:my_research')
    return render(request, 'researchpanel/confirm_delete.html', {'post': post})

def research_detail(request, pk):
    post = get_object_or_404(ResearchPost, pk=pk, status='published')
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    already_requested = False
    if request.user.is_authenticated and request.user.role == 'student':
        # FIX: 'research' theke soriye 'researcher' kora holo
        already_requested = Collaboration.objects.filter(
            researcher=post.researcher, 
            student=request.user,
            status__in=['pending', 'accepted']
        ).exists()
        
    return render(request, 'researchpanel/research_detail.html', {'post': post, 'already_requested': already_requested})


# ==========================================
# 3. COLLABORATION VIEWS
# ==========================================
@researcher_required
def collaborations(request):
    collabs = Collaboration.objects.filter(researcher=request.user).select_related('student')
    return render(request, 'researchpanel/collaborations.html', {'collabs': collabs})

@researcher_required
def update_collab(request, pk, action):
    collab = get_object_or_404(Collaboration, pk=pk, researcher=request.user)
    
    if action == 'accept':
        collab.status = 'accepted'
        collab.save()
        
        # Automatic Dashboard a research post create (Draft hisabe)
        ResearchPost.objects.create(
            researcher=request.user,
            title=collab.topic,
            abstract=f"Collaborative project initiated by student: {collab.student.get_full_name()}.",
            content=collab.message,
            field="General",
            status="draft" 
        )
        
        # Student ke auto notification pathano
        Message.objects.create(
            sender=request.user,
            receiver=collab.student,
            content=f"Great news! Your collaboration request for '{collab.topic}' was ACCEPTED. Let's start working!"
        )
        messages.success(request, f"Accepted {collab.student.first_name}'s request. A draft research post was created.")
        
    elif action == 'reject':
        collab.status = 'rejected'
        collab.save()
        
        Message.objects.create(
            sender=request.user,
            receiver=collab.student,
            content=f"Sorry, your collaboration request for '{collab.topic}' was declined."
        )
        messages.warning(request, f"Rejected {collab.student.first_name}'s request.")
        
    return redirect('researchpanel:collaborations')

@login_required
def request_collaboration(request, pk):
    post = get_object_or_404(ResearchPost, pk=pk, status='published')
    if request.user.role != 'student':
        messages.error(request, 'Only students can request collaboration.')
        return redirect('researchpanel:research_detail', pk=pk)
        
    msg = request.POST.get('message', '')
    # FIX: 'research' field nai, 'researcher' ebang 'topic' use kora holo
    _, created = Collaboration.objects.get_or_create(
        researcher=post.researcher, 
        student=request.user, 
        defaults={
            'topic': post.title,
            'message': msg
        }
    )
    
    if created:
        messages.success(request, 'Collaboration request sent!')
    else:
        messages.info(request, 'You already requested a collaboration with this researcher.')
    return redirect('studentpanel:search_research')


# ==========================================
# 4. MESSAGES & NOTIFICATIONS
# ==========================================
@researcher_required
def messages_view(request):
    students = CustomUser.objects.filter(role='student')
    
    # FIX: GET theke na pele POST theke nibe
    selected_user_id = request.GET.get('user') or request.POST.get('user_id')
    selected_user = None
    conversation = []

    if selected_user_id:
        selected_user = get_object_or_404(CustomUser, pk=selected_user_id)
        conversation = Message.objects.filter(
            Q(sender=request.user, receiver=selected_user) |
            Q(sender=selected_user, receiver=request.user)
        ).order_by('created_at') # Add order_by for chronological messages
        Message.objects.filter(sender=selected_user, receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST' and selected_user:
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=request.user, receiver=selected_user, content=content)
        return redirect(f'{request.path}?user={selected_user.id}')

    context = {
        'students': students,
        'selected_user': selected_user,
        'conversation': conversation,
    }
    return render(request, 'researchpanel/messages.html', context)

@researcher_required
def notifications(request):
    unread = Message.objects.filter(receiver=request.user, is_read=False).select_related('sender')
    return render(request, 'researchpanel/notifications.html', {'messages_list': unread})

@researcher_required
def search_researchers(request):
    query = request.GET.get('q', '')
    results = ResearchPost.objects.filter(status='published')
    if query:
        results = results.filter(Q(title__icontains=query) | Q(abstract__icontains=query) | Q(field__icontains=query))
    return render(request, 'researchpanel/search_research.html', {'results': results, 'query': query})