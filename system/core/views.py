from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student, Subject, GPA
from django.http import HttpResponseForbidden
from core.models import Student  # Student モデルのインポート
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from datetime import datetime
import locale
from django.db import IntegrityError

# Create your views here.

def home(request):
    host = request.get_host()  # ホスト名を取得
    print(f"Request host: {request.get_host()}")  # ログにホスト名を出力
    return render(request, 'core/home.html')


# #アカウント作成
# def register_student(request):
#     if request.method == 'POST':
#         student_name = request.POST.get('student_name', '').strip()
#         password = request.POST.get('password', '').strip()

#         # 入力値のチェック
#         if not student_name or not password:
#             return render(request, 'core/register_student.html', {
#                 'error': '全ての項目を入力してください。'
#             })

#         # 学生名が重複しないかチェック
#         if Student.objects.filter(student_name=student_name).exists():
#             return render(request, 'core/register_student.html', {
#                 'error': 'この学生名は既に登録されています。'
#             })

#         # ランダムな student_id を生成して Student モデルに登録
#         student_id = str(uuid.uuid4())[:8]  # UUIDの最初の8文字をIDに使用
#         Student.objects.create(student_id=student_id, student_name=student_name, password=password)

#         return redirect('home')  # 登録後はホームへリダイレクト

#     return render(request, 'core/register_student.html')
# アカウント作成
def register_student(request):
    register_error = None

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        password = request.POST.get('password')

        if User.objects.filter(username=student_name).exists():
            register_error = "この名前はすでに使われています"
        else:
            user = User.objects.create_user(username=student_name, password=password)
            Student.objects.create(user=user)  # Student オブジェクトを作成
            login(request, user)  # 登録後に自動ログイン
            return redirect('core:grade_view')  # 成績ページへリダイレクト

    return render(request, 'core/login.html', {'register_error': register_error})

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('student_name')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             login(request, user)
            
#             # next パラメータが存在する場合、そのURLにリダイレクト
#             next_url = request.GET.get('next')
#             if next_url:
#                 return redirect(next_url)
            
#             # next がない場合、デフォルトのリダイレクト先へ
#             return redirect(settings.LOGIN_REDIRECT_URL)
#         else:
#             return render(request, 'core/login.html', {'error': '無効なユーザー名またはパスワードです。'})
    
#     # GETリクエスト時、通常のログインページを表示
#     return render(request, 'core/login.html')

# # ログイン
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['student_name']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             # 学生 ID をセッションに保存（仮の値を使用）
#             request.session['student_id'] = 'A001'
#             print(f"ログイン成功: セッションキー = {request.session.session_key}, student_id = {request.session.get('student_id')}")
#             return redirect('student_home')
#         else:
#             print("ログイン失敗")
#     return render(request, 'core/login.html')

# ログイン・アカウント作成
# def login_view(request):
#     error = None
#     register_error = None

#     if request.method == 'POST':
#         if 'login' in request.POST:
#             student_name = request.POST.get('student_name')
#             password = request.POST.get('password')
#             user = authenticate(request, username=student_name, password=password)
#             if user is not None:
#                 login(request, user)

#                 # Student を取得してセッションに保存
#                 student = Student.objects.get(user=user)
#                 request.session['student_id'] = student.student_id

#                 return redirect('core:student_home')
#             else:
#                 error = "名前またはパスワードが間違っています"

#         elif 'register' in request.POST:
#             student_name = request.POST.get('student_name')
#             password = request.POST.get('password')
#             if User.objects.filter(username=student_name).exists():
#                 register_error = "この名前はすでに使われています"
#             else:
#                 user = User.objects.create_user(username=student_name, password=password)

#                 # Student を作成し、セッションに保存
#                 student = Student.objects.create(user=user)

#                 login(request, user)
#                 request.session['student_id'] = student.student_id

#                 return redirect('core:student_home')

#     return render(request, 'core/login.html', {
#         'error': error,
#         'register_error': register_error
#     })

# ログイン・アカウント作成
def login_view(request):
    error = None
    register_error = None

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        password = request.POST.get('password')

        # ログイン処理
        if 'login' in request.POST:
            user = authenticate(request, username=student_name, password=password)
            if user is not None:
                login(request, user)
                try:
                    student = Student.objects.get(user=user)
                    request.session['student_id'] = student.student_id
                except Student.DoesNotExist:
                    error = "このユーザーに対応するStudent情報が存在しません"
                    return render(request, 'core/login.html', {'error': error})

                return redirect('core:student_home')
            else:
                error = "名前またはパスワードが間違っています"

        # アカウント作成処理
        elif 'register' in request.POST:
            student_name = request.POST.get('student_name')
            password = request.POST.get('password')

            if User.objects.filter(username=student_name).exists():
                register_error = "この名前はすでに使われています"
            else:
                try:
                    # Userを作成
                    user = User.objects.create_user(username=student_name, password=password)

                    # Studentを作成（例外に備える）
                    student = Student.objects.create(user=user)

                    login(request, user)
                    request.session['student_id'] = student.student_id
                    return redirect('core:student_home')
                except IntegrityError:
                    register_error = "Student の作成に失敗しました（重複エラー）"
                    user.delete()  # 必要であればUserも削除して巻き戻す

    return render(request, 'core/login.html', {
        'error': error,
        'register_error': register_error,
    })


# ログアウト
def logout_view(request):
    logout(request)  # ユーザーをログアウト
    request.session.flush()  # セッションを完全にクリア
    return redirect('core:login')  # ログイン画面にリダイレクト

# def student_home(request):
#     host = request.get_host()
#     print(f"Student home page accessed from host: {host}")

#     # セッションから student_id を取得
#     student_id = request.session.get('student_id')
#     print(f"セッション内の student_id: {student_id}")

#     if not student_id:
#         print("セッションが見つからないため、ログインページにリダイレクトします")
#         return redirect('login')

#     try:
#         student = Student.objects.get(student_id=student_id)
#         print(f"取得した学生情報: {student}")
#     except Student.DoesNotExist:
#         print("指定された student_id に一致する学生が見つかりません")
#         return redirect('login')

#     # レンダリング処理に変更
#     return render(
#         request,
#         'core/student_home.html',
#         {'student': student}  # 学生情報をテンプレートに渡す
#     )

@never_cache
def student_home(request):
    session_key = request.session.session_key  # 現在のセッションキー
    print(f"現在のセッションキー: {session_key}")

    student_id = request.session.get('student_id')  # セッションに保存された student_id
    print(f"セッションから取得した student_id: {student_id}")

    if not student_id:
        return redirect('core:login')

    # 学生情報を取得
    student = Student.objects.get(student_id=student_id)

    # 今日の曜日を日本語で取得
    weekday_map = ['月', '火', '水', '木', '金', '土', '日']
    today = datetime.now().weekday() # 0=月曜、6=日曜
    today_str = weekday_map[today]

    # 今日の曜日に対応する履修科目を取得
    today_subjects = Subject.objects.filter(student=student, day_of_week=today_str)

    return render(request, 'core/student_home.html', 
                  {'student': student, 'today_subjects': today_subjects, 'today_str': today_str})

def manage_grades(request):
    host = request.get_host()  # ホスト名を取得
    print(f"Manage grades page accessed from host: {host}")  # ログにホスト名を出力
    return render(request, 'core/manage_grades.html')

@never_cache
@login_required
def subject_register(request):
    print(f"Logged-in user: {request.user}")  # デバッグ用
    print(f"Is authenticated: {request.user.is_authenticated}")  # 認証状態を確認

    debug_info = f"ユーザー: {request.user} | 認証状態: {request.user.is_authenticated}"

    grades = range(1, 6)  # 成績の選択肢（1〜5）

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        grade = request.POST.get('grade')
        #date = request.POST.get('date')
        table = request.POST.get('table')
        day_of_week = request.POST.get('day_of_week')  # ← 追加
        lesson_count = request.POST.get('lesson_count')
        attend_days = request.POST.get('attend_days')

        # 入力チェック
        if not all([name, grade, table, lesson_count, attend_days]):
            return render(request, 'core/subject_register.html', {
                'grades': grades,
                'error': '全ての項目を入力してください。',
                'debug_info': debug_info
            })

        try:
            # Student オブジェクトの取得または作成
            # student, created = Student.objects.get_or_create(student_name=request.user.username)
            # print(f"Student作成: {created}")  # デバッグ用
            # debug_info += f" | Student作成: {created}"
            student, created = Student.objects.get_or_create(user=request.user)
            debug_info += f" | Student取得または作成: {'新規作成' if created else '既存'}"

            # Subject オブジェクトを作成
            Subject.objects.create(
                student=student,
                subject_name=name,
                day_of_week=day_of_week,  # ← 追加
                subject_score=int(grade),
                # date=date,
                table=table,
                # lesson_count=int(lesson_count),
                # attend_days=int(attend_days)
                lesson_count=int(request.POST.get('lesson_count', 0)),
                attend_days=int(request.POST.get('attend_days', 0))
            )

            return redirect('core:student_home')  # 成功時にリダイレクト

        except Exception as e:
            debug_info += f" | エラー: {str(e)}"
            print(f"エラー: {str(e)}")
            return render(request, 'core/subject_register.html', {
                'grades': grades,
                'error': '登録中にエラーが発生しました。',
                'debug_info': debug_info
            })

    # GETリクエスト時
    return render(request, 'core/subject_register.html', {'grades': grades, 'debug_info': debug_info})

def calculate_gpa(student_id):
    # 学生の全ての成績を取得
    subjects = Subject.objects.filter(student_id=student_id)
    if not subjects.exists():
        return 0.0

    # 成績の合計と科目数
    total_grade = sum(subject.grade for subject in subjects)
    gpa = total_grade / subjects.count()
    return round(gpa, 2)  # 小数点以下2桁で丸める

@never_cache
@login_required
@login_required
def grade_view(request):
    host = request.get_host()
    print(f"Grade view page accessed from host: {host}")

    try:
        student = Student.objects.get(student_name=request.user.username)
    except Student.DoesNotExist:
        return render(request, 'core/error.html', {'error_message': 'Student情報が見つかりません。'})

    subjects = Subject.objects.filter(student=student)

    # GPA計算
    total_score = sum(subject.subject_score for subject in subjects)
    gpa = total_score / len(subjects) if subjects else 0

    # GPAメッセージ
    if gpa >= 4.0:
        message = '今の成績を維持しましょう'
    elif 2.5 <= gpa < 4.0:
        low_score_subjects = subjects.filter(subject_score__lt=2)
        if low_score_subjects.exists():
            low_score_names = ', '.join([subject.subject_name for subject in low_score_subjects])
            message = f'成績の改善が必要な科目があります: {low_score_names}'
        else:
            message = '成績の改善が必要な科目があります'
    else:
        message = '履修科目を見直す必要があります'

    return render(request, 'core/grade_view.html', {
        'subjects': subjects,
        'gpa': gpa,
        'message': message
    })

@never_cache
def attendance_plan(request):
    host = request.get_host()  # ホスト名を取得
    print(f"Attendance plan page accessed from host: {host}")  # ログにホスト名を出力
    
    # student_id = request.session.get('student_id')
    # student = Student.objects.get(student_id=student_id)
    student = Student.objects.get(user=request.user)
    subjects = Subject.objects.filter(student=student)

    # 出席率計算
    attendance_data = []
    for subject in subjects:
        if subject.lesson_count == 0:
            attendance_rate = 0  # ゼロ除算を防ぐ
        else:
            attendance_rate = (subject.attend_days / subject.lesson_count) * 100

        if attendance_rate >= 70:
            status = '現状を維持しましょう'
        elif attendance_rate == 70:
            status = '少し危険です'
        else:
            status = '警告！出席率が低下しています'
    
        # ここで追加する
        attendance_data.append({
            'subject_name': subject.subject_name,
            'lesson_count': subject.lesson_count,
            'attend_days': subject.attend_days,
            'attendance_rate': attendance_rate,
            'status': status
        })

    # ✅ 時間割データ構築を追加
    days = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日']
    periods = ['1限目', '2限目', '3限目', '4限目']

    timetable = {period: {day: '' for day in days} for period in periods}

    for subject in subjects:
        day = subject.date
        period = subject.table
        if day in days and period in periods:
            timetable[period][day] = subject.subject_name

    return render(request, 'core/attendance_plan.html', 
                  {'attendance_data': attendance_data, 
                   'timetable': timetable, 'days': days, 
                   'periods': periods})
