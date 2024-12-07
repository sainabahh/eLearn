from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password  
import time  # For simulating splash duration

from .models import LoginTable, Course, Video, UserProgress

# Create your views here.

def splash_screen(request):
    time.sleep(3)  
    return render(request, 'splash.html')  

def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html') 

    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = LoginTable.objects.get(username=username)

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('course_list')  
            else:
                return render(request, 'login.html', {'error': 'Invalid username or password!'})

        except LoginTable.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username or password!'})


# Logout View
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # Remove user session
    return redirect('splash') 



def signup_view(request):
    if request.method == "GET":
        return render(request, 'signup.html')  

    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')  
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match!'})

        if LoginTable.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists!'})

        if LoginTable.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists!'})

        hashed_password = make_password(password)

        user = LoginTable(username=username, email=email, password=hashed_password)
        user.save()

        return redirect('login')


def course_list_view(request):
    if 'user_id' not in request.session:
        return redirect('login') 

    courses = Course.objects.all()
    if not courses:
        return render(request, 'course_list.html', {'message': 'No courses available.'})
    return render(request, 'course_list.html', {'courses': courses})


def select_course(request):
    if 'user_id' not in request.session:
        return redirect('login')  

    user_id = request.session['user_id']
    user = get_object_or_404(LoginTable, id=user_id)

    if request.method == 'POST':

        course_id = request.POST.get('course_id')  
        if course_id:
            course = get_object_or_404(Course, id=course_id) 

            videos = Video.objects.filter(course=course).order_by('order')
            
            # Fetch user progress for each video
            video_progress = []
            for video in videos:
                progress, created = UserProgress.objects.get_or_create(user=user, video=video)

                if video.order == 1:
                    # First video is always unlocked
                    video_progress.append({
                        'video': video,
                        'is_watched': progress.is_watched,
                        'is_locked': False,  # Unlock first video
                    })
                else:
                    previous_video = Video.objects.filter(course=course, order=video.order - 1).first()
                    previous_progress = UserProgress.objects.filter(user=user, video=previous_video).first()

                    if previous_progress and previous_progress.is_watched:
                        video_progress.append({
                            'video': video,
                            'is_watched': progress.is_watched,
                            'is_locked': not progress.is_watched,  # Lock video if not watched
                        })
                    else:
                        video_progress.append({
                            'video': video,
                            'is_watched': progress.is_watched,
                            'is_locked': True,  
                        })

            return render(request, 'course_videos.html', {'course': course, 'video_progress': video_progress})

    courses = Course.objects.all()
    return render(request, 'course_selection.html', {'courses': courses})



def video_screen(request, video_id):
    if 'user_id' not in request.session:
        return redirect('login')

    video = get_object_or_404(Video, id=video_id)
    user_id = request.session['user_id']
    user = get_object_or_404(LoginTable, id=user_id)
    
    progress, created = UserProgress.objects.get_or_create(user=user, video=video)
    if not progress.is_watched:
        progress.is_watched = True
        progress.save()

    prev_video = Video.objects.filter(course=video.course, order=video.order - 1).first()
    if prev_video:
        prev_progress = UserProgress.objects.filter(user=user, video=prev_video).first()
        if prev_progress and not prev_progress.is_watched:
            return redirect('course_videos', course_id=video.course.id)

    return render(request, 'video_screen.html', {'video': video})


def profile_view(request):
    if 'user_id' not in request.session:
        return redirect('login')  

    user_id = request.session['user_id']
    user = LoginTable.objects.get(id=request.session['user_id']) 

    return render(request, 'profile.html', {'user': user})

