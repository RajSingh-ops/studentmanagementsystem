# student_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Student
from .forms import StudentForm, LoginForm

# --- Session & Auth Views ---

def login_view(request):
    """
    Handles user login.
    DEMONSTRATES: Sessions
    We manually set a session variable 'is_logged_in' upon a "successful"
    (dummy) login. In a real app, you'd use Django's auth system.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Dummy authentication:
            # In a real app, you'd check request.POST['username'] and password
            # against a database.
            # We'll just assume 'admin' / 'password' is correct.
            if (form.cleaned_data['username'] == 'admin' and
                form.cleaned_data['password'] == 'password'):
                
                # *** DEMONSTRATING SESSIONS ***
                # Set a session variable to mark the user as logged in
                request.session['is_logged_in'] = True
                request.session['username'] = form.cleaned_data['username']
                return redirect('student_list')
            else:
                # Invalid login
                form.add_error(None, "Invalid username or password. (Try admin/password)")
    else:
        form = LoginForm()
        
    # If the user is already logged in, redirect them to the list
    if request.session.get('is_logged_in', False):
        return redirect('student_list')
        
    return render(request, 'student_app/login.html', {'form': form})

def logout_view(request):
    """
    Logs the user out.
    DEMONSTRATES: Sessions
    We clear the session data (flush) to log the user out.
    """
    # *** DEMONSTRATING SESSIONS ***
    request.session.flush()
    return redirect('login')


# --- Student CRUD & List Views ---

def student_list_view(request):
    """
    Displays the list of students.
    DEMONSTRATES: Filtering, Sorting, and Cookies.
    """
    # Session Check: Redirect to login if not authenticated
    if not request.session.get('is_logged_in', False):
        return redirect('login')

    students = Student.objects.all()

    # --- DEMONSTRATING FILTERING (from URL query params) ---
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(roll_number__icontains=search_query) |
            Q(major__icontains=search_query)
        )

    # --- DEMONSTRATING SORTING & COOKIES ---
    # Get sort_by from URL param, or from cookie, or default to 'last_name'
    default_sort = 'last_name'
    sort_by = request.GET.get('sort_by', request.COOKIES.get('last_sort', default_sort))
    
    # Validate sort_by to prevent arbitrary sorting on invalid fields
    valid_sort_fields = ['first_name', 'last_name', 'roll_number', 'grade', 'major']
    if sort_by.replace('-', '') not in valid_sort_fields:
        sort_by = default_sort

    students = students.order_by(sort_by)

    context = {
        'students': students,
        'search_query': search_query,
        'current_sort': sort_by,
        'username': request.session.get('username', 'Guest'),
    }
    
    # Create the response
    response = render(request, 'student_app/student_list.html', context)
    
    # *** DEMONSTRATING COOKIES ***
    # Save the user's last sort preference in a cookie
    response.set_cookie('last_sort', sort_by, max_age=3600*24*7) # Cookie lasts 1 week

    return response

def student_add_view(request):
    """
    Handles adding a new student.
    """
    if not request.session.get('is_logged_in', False):
        return redirect('login')
        
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'student_app/student_form.html', {'form': form, 'action': 'Add'})

def student_update_view(request, pk):
    """
    Handles updating an existing student.
    DEMONSTRATES: URL Parameters (pk)
    """
    if not request.session.get('is_logged_in', False):
        return redirect('login')
        
    # *** DEMONSTRATING URL PARAMETERS ***
    # Get the specific student object or return a 404 error
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'student_app/student_form.html', {'form': form, 'action': 'Update'})

def student_delete_view(request, pk):
    """
    Handles deleting a student.
    DEMONSTRATES: URL Parameters (pk)
    """
    if not request.session.get('is_logged_in', False):
        return redirect('login')
        
    # *** DEMONSTRATING URL PARAMETERS ***
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    
    # For a GET request, show a confirmation (or just redirect)
    # A real app should have a confirmation page, but for simplicity:
    return redirect('student_list')