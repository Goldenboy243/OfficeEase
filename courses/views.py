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
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft Word").prefetch_related('lessons')
    return render(request, 'courses/word.html', {'modules': modules})

def excel_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft Excel").prefetch_related('lessons')
    return render(request, 'courses/excel.html', {'modules': modules})

def powerpoint_course(request):
    # Fetch modules and prefetch their lessons to keep it fast
    modules = Module.objects.filter(course__name="Microsoft PowerPoint").prefetch_related('lessons')
    return render(request, 'courses/powerpoint.html', {'modules': modules})


def _unlock_next_step(user, step):
    next_step = (
        Step.objects
        .filter(topic=step.topic, order__gt=step.order)
        .order_by('order')
        .first()
    )
    if next_step:
        progress, _ = UserStepProgress.objects.get_or_create(user=user, step=next_step)
        if progress.status == UserStepProgress.LOCKED:
            progress.status = UserStepProgress.UNLOCKED
            progress.save(update_fields=['status'])
    return next_step


def _progress_summary(user, topic):
    step_ids = list(topic.steps.values_list('id', flat=True))
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
    topics = Topic.objects.filter(module__course=course, is_published=True).prefetch_related(
        Prefetch('steps', queryset=Step.objects.order_by('order').select_related('practice_task'))
    ).order_by('module__order', 'order')

    selected_topic = topics.first()
    topic_id = request.GET.get('topic')
    if topic_id:
        selected_topic = topics.filter(id=topic_id).first() or selected_topic

    steps_payload = []
    progress = {'passed': 0, 'total': 0, 'percent': 0}

    if selected_topic:
        steps = list(selected_topic.steps.all())
        if request.user.is_authenticated and steps:
            first_step = steps[0]
            first_progress, _ = UserStepProgress.objects.get_or_create(user=request.user, step=first_step)
            if first_progress.status == UserStepProgress.LOCKED:
                first_progress.status = UserStepProgress.UNLOCKED
                first_progress.save(update_fields=['status'])

        status_map = {}
        if request.user.is_authenticated:
            status_map = {
                p.step_id: p.status
                for p in UserStepProgress.objects.filter(user=request.user, step__topic=selected_topic)
            }
            progress = _progress_summary(request.user, selected_topic)

        for idx, step in enumerate(steps):
            task = getattr(step, 'practice_task', None)
            rules = []
            if task:
                rules = [
                    {
                        'id': r.id,
                        'name': r.name,
                        'rule_type': r.rule_type,
                        'expected_value': r.expected_value,
                        'is_required': r.is_required,
                    }
                    for r in task.rules.all()
                ]

            steps_payload.append({
                'id': step.id,
                'index': idx + 1,
                'title': step.title,
                'type': step.step_type,
                'content': step.content,
                'status': status_map.get(step.id, UserStepProgress.LOCKED),
                'practice': {
                    'instruction': task.instruction if task else '',
                    'starter_content': task.starter_content if task else '',
                    'success_message': task.success_message if task else '',
                    'rules': rules,
                }
            })

    return render(
        request,
        'courses/structured_course.html',
        {
            'course': course,
            'topics': topics,
            'selected_topic': selected_topic,
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

    if step.step_type not in [Step.THEORY, Step.QUIZ]:
        return JsonResponse({'ok': False, 'error': 'This step must be completed through practice validation.'}, status=400)

    progress, _ = UserStepProgress.objects.get_or_create(user=request.user, step=step)
    if progress.status == UserStepProgress.LOCKED:
        return JsonResponse({'ok': False, 'error': 'Step is still locked.'}, status=400)

    progress.status = UserStepProgress.PASSED
    progress.completed_at = timezone.now()
    progress.save(update_fields=['status', 'completed_at'])

    next_step = _unlock_next_step(request.user, step)
    summary = _progress_summary(request.user, step.topic)

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

    summary = _progress_summary(request.user, step.topic)
    return JsonResponse({
        'ok': True,
        'passed': all_required_passed,
        'rule_results': rule_results,
        'next_step_id': next_step.id if next_step else None,
        'progress': summary,
    })
