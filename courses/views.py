import re

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (
    Course,
    Module,
    PracticeSubmission,
    Step,
    Topic,
    UserStepProgress,
    ValidationRule,
)

def word_course(request):
    return structured_word_course(request)

def excel_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft Excel").prefetch_related('lessons')
    return render(request, 'courses/excel.html', {'modules': modules})

def powerpoint_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft PowerPoint").prefetch_related('lessons')
    return render(request, 'courses/powerpoint.html', {'modules': modules})


def _ordered_course_steps(course):
    return list(
        Step.objects
        .filter(topic__module__course=course, topic__is_published=True)
        .select_related('topic', 'topic__module')
        .order_by('topic__module__order', 'topic__order', 'order', 'id')
    )


def _unlock_next_step(user, step):
    ordered_steps = _ordered_course_steps(step.topic.module.course)
    next_step = None
    for idx, candidate in enumerate(ordered_steps):
        if candidate.id == step.id and idx + 1 < len(ordered_steps):
            next_step = ordered_steps[idx + 1]
            break

    if next_step:
        progress, _ = UserStepProgress.objects.get_or_create(user=user, step=next_step)
        if progress.status == UserStepProgress.LOCKED:
            progress.status = UserStepProgress.UNLOCKED
            progress.save(update_fields=['status'])
    return next_step


def _progress_summary(user, course):
    step_ids = list(
        Step.objects
        .filter(topic__module__course=course, topic__is_published=True, is_required=True)
        .values_list('id', flat=True)
    )
    total = len(step_ids)
    if total == 0:
        return {'passed': 0, 'total': 0, 'percent': 0}

    passed = UserStepProgress.objects.filter(
        user=user,
        step_id__in=step_ids,
        status=UserStepProgress.PASSED
    ).count()
    percent = int((passed / total) * 100)
    return {'passed': passed, 'total': total, 'percent': percent}


def structured_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = list(
        Module.objects.filter(course=course)
        .prefetch_related(
            Prefetch(
                'topics',
                queryset=Topic.objects.filter(is_published=True).prefetch_related(
                    Prefetch('steps', queryset=Step.objects.order_by('order'))
                ).order_by('order')
            )
        )
        .order_by('order')
    )

    module_entries = []
    for module in modules:
        module_steps = []
        for topic in module.topics.all():
            module_steps.extend(list(topic.steps.all()))
        module_entries.append({'module': module, 'steps': module_steps})

    status_map = {}
    if request.user.is_authenticated:
        status_map = {
            p.step_id: p.status
            for p in UserStepProgress.objects.filter(user=request.user, step__topic__module__course=course)
        }

    def is_module_completed(entry):
        required_step_ids = [s.id for s in entry['steps'] if s.is_required]
        if not required_step_ids:
            return False
        return all(status_map.get(step_id) == UserStepProgress.PASSED for step_id in required_step_ids)

    previous_completed = True
    for entry in module_entries:
        entry['is_completed'] = is_module_completed(entry)
        entry['is_unlocked'] = previous_completed
        previous_completed = previous_completed and entry['is_completed']

    selected_module_entry = module_entries[0] if module_entries else None
    selected_module_id = request.GET.get('module')
    if selected_module_id:
        candidate = next((e for e in module_entries if str(e['module'].id) == selected_module_id), None)
        if candidate and candidate['is_unlocked']:
            selected_module_entry = candidate
    else:
        selected_module_entry = next((e for e in module_entries if e['is_unlocked']), selected_module_entry)

    steps_payload = []
    if selected_module_entry:
        selected_steps = selected_module_entry['steps']

        previous_required_passed = True
        for idx, step in enumerate(selected_steps):
            status = status_map.get(step.id, UserStepProgress.LOCKED)
            if status != UserStepProgress.PASSED:
                if selected_module_entry['is_unlocked'] and previous_required_passed:
                    status = UserStepProgress.UNLOCKED

            if request.user.is_authenticated:
                progress_obj, _ = UserStepProgress.objects.get_or_create(user=request.user, step=step)
                if status == UserStepProgress.UNLOCKED and progress_obj.status == UserStepProgress.LOCKED:
                    progress_obj.status = UserStepProgress.UNLOCKED
                    progress_obj.save(update_fields=['status'])
                status = progress_obj.status

            if step.is_required and status != UserStepProgress.PASSED:
                previous_required_passed = False

            steps_payload.append({
                'id': step.id,
                'index': idx + 1,
                'title': step.title,
                'type': step.step_type,
                'content': step.content,
                'status': status,
                'quiz': {
                    'question': step.quiz_question,
                    'options': [step.quiz_option_1, step.quiz_option_2],
                },
            })

    progress = {'passed': 0, 'total': 0, 'percent': 0}
    if request.user.is_authenticated:
        progress = _progress_summary(request.user, course)

    return render(
        request,
        'courses/structured_course.html',
        {
            'course': course,
            'modules': module_entries,
            'selected_module': selected_module_entry['module'] if selected_module_entry else None,
            'steps_payload': steps_payload,
            'progress': progress,
        }
    )


def structured_word_course(request):
    course = get_object_or_404(Course, name='Microsoft Word')
    return structured_course(request, course.id)


def structured_excel_course(request):
    course = get_object_or_404(Course, name='Microsoft Excel')
    return structured_course(request, course.id)


def structured_powerpoint_course(request):
    course = get_object_or_404(Course, name='Microsoft PowerPoint')
    return structured_course(request, course.id)


@login_required
@require_POST
def complete_theory_step(request, step_id):
    step = get_object_or_404(Step, id=step_id)

    if step.step_type == Step.PRACTICE:
        return JsonResponse({'ok': False, 'error': 'Practice IDE steps are disabled in the current curriculum.'}, status=400)

    if step.step_type not in [Step.THEORY, Step.QUIZ, Step.WORKSHOP]:
        return JsonResponse({'ok': False, 'error': 'Unsupported step type.'}, status=400)

    progress, _ = UserStepProgress.objects.get_or_create(user=request.user, step=step)
    if progress.status == UserStepProgress.LOCKED:
        return JsonResponse({'ok': False, 'error': 'Step is still locked.'}, status=400)

    if step.step_type == Step.QUIZ:
        selected_option = request.POST.get('selected_option', '').strip()
        if selected_option not in ['0', '1']:
            return JsonResponse({'ok': False, 'error': 'Please choose one answer before continuing.'}, status=400)
        if not step.quiz_correct_answer or selected_option != step.quiz_correct_answer:
            return JsonResponse({'ok': False, 'error': 'Incorrect answer. Please review and try again.'}, status=400)

    progress.status = UserStepProgress.PASSED
    progress.completed_at = timezone.now()
    progress.save(update_fields=['status', 'completed_at'])

    next_step = _unlock_next_step(request.user, step)
    summary = _progress_summary(request.user, step.topic.module.course)

    return JsonResponse({
        'ok': True,
        'next_step_id': next_step.id if next_step else None,
        'progress': summary,
    })


def _evaluate_rule(rule, submission_html, plain_text):
    expected = (rule.expected_value or '').strip()
    if not expected:
        return False, 'Rule missing expected value.'

    if rule.rule_type == ValidationRule.CONTAINS_TEXT:
        ok = expected.lower() in plain_text.lower()
        return ok, f"Expected text '{expected}' not found."

    if rule.rule_type == ValidationRule.BOLD_TEXT:
        pattern = rf"<(strong|b)[^>]*>\s*{re.escape(expected)}\s*</(strong|b)>"
        ok = re.search(pattern, submission_html, flags=re.IGNORECASE) is not None
        return ok, f"Expected bold text '{expected}' was not found in bold formatting."

    return False, 'Unsupported validation rule.'


@login_required
@require_POST
def submit_practice_step(request, step_id):
    step = get_object_or_404(Step.objects.select_related('practice_task'), id=step_id)
    if step.step_type != Step.PRACTICE or not hasattr(step, 'practice_task'):
        return JsonResponse({'ok': False, 'error': 'This is not a practice step.'}, status=400)

    progress, _ = UserStepProgress.objects.get_or_create(user=request.user, step=step)
    if progress.status == UserStepProgress.LOCKED:
        return JsonResponse({'ok': False, 'error': 'Step is still locked.'}, status=400)

    submission_html = request.POST.get('submission', '')
    plain_text = re.sub('<[^<]+?>', ' ', submission_html)

    rule_results = []
    all_required_passed = True
    for rule in step.practice_task.rules.all():
        passed, failure_reason = _evaluate_rule(rule, submission_html, plain_text)
        if rule.is_required and not passed:
            all_required_passed = False
        rule_results.append({
            'rule_id': rule.id,
            'name': rule.name,
            'passed': passed,
            'failure_reason': '' if passed else failure_reason,
        })

    PracticeSubmission.objects.create(
        user=request.user,
        step=step,
        submitted_content=submission_html,
        is_passed=all_required_passed,
        result_snapshot={'rules': rule_results}
    )

    if all_required_passed:
        progress.status = UserStepProgress.PASSED
        progress.completed_at = timezone.now()
        progress.save(update_fields=['status', 'completed_at'])
        next_step = _unlock_next_step(request.user, step)
    else:
        next_step = None

    summary = _progress_summary(request.user, step.topic.module.course)
    return JsonResponse({
        'ok': True,
        'passed': all_required_passed,
        'rule_results': rule_results,
        'next_step_id': next_step.id if next_step else None,
        'progress': summary,
    })
