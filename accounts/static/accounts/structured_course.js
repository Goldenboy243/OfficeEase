(function () {
  const dataNode = document.getElementById('steps-data');
  if (!dataNode) return;

  const steps = JSON.parse(dataNode.textContent || '[]');
  if (!steps.length) return;

  const els = {
    topicSelect: document.getElementById('topic-select'),
    stepsList: document.getElementById('steps-list'),
    stepBadge: document.getElementById('step-badge'),
    stepTitle: document.getElementById('step-title'),
    stepContent: document.getElementById('step-content'),
    practicePanel: document.getElementById('practice-panel'),
    practiceInstruction: document.getElementById('practice-instruction'),
    practiceInput: document.getElementById('practice-input'),
    runTestsBtn: document.getElementById('run-tests-btn'),
    ruleResults: document.getElementById('rule-results'),
    prevStepBtn: document.getElementById('prev-step-btn'),
    nextStepBtn: document.getElementById('next-step-btn'),
    progressBar: document.getElementById('progress-bar'),
    progressText: document.getElementById('progress-text')
  };

  if (els.progressBar) {
    const initialProgress = Number(els.progressBar.dataset.progress || '0');
    els.progressBar.style.width = `${initialProgress}%`;
  }

  let currentIndex = Math.max(steps.findIndex((s) => s.status !== 'locked'), 0);

  function getCsrfToken() {
    const cookie = document.cookie
      .split(';')
      .map((c) => c.trim())
      .find((c) => c.startsWith('csrftoken='));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
  }

  function renderStepsList() {
    els.stepsList.innerHTML = steps
      .map((step, index) => {
        const isActive = index === currentIndex;
        const isLocked = step.status === 'locked';
        const statusColor = step.status === 'passed'
          ? 'text-emerald-600'
          : step.status === 'unlocked'
            ? 'text-blue-600'
            : 'text-slate-400';

        return `
          <button data-index="${index}" ${isLocked ? 'disabled' : ''}
            class="step-item w-full rounded-xl border px-3 py-3 text-left transition-all ${
              isActive
                ? 'border-blue-200 bg-blue-50'
                : 'border-slate-200 bg-white hover:bg-slate-50'
            } ${isLocked ? 'cursor-not-allowed opacity-60' : ''}">
            <div class="flex items-center justify-between">
              <p class="text-xs font-bold uppercase tracking-widest ${statusColor}">Step ${step.index}</p>
              <i class="fa-solid ${
                step.status === 'passed'
                  ? 'fa-circle-check text-emerald-500'
                  : isLocked
                    ? 'fa-lock text-slate-300'
                    : 'fa-circle text-blue-500'
              }"></i>
            </div>
            <h4 class="mt-1 text-sm font-semibold text-slate-800">${step.title}</h4>
            <p class="mt-1 text-xs text-slate-500 capitalize">${step.type}</p>
          </button>
        `;
      })
      .join('');

    document.querySelectorAll('.step-item').forEach((btn) => {
      btn.addEventListener('click', () => {
        const idx = Number(btn.dataset.index);
        if (!Number.isNaN(idx)) {
          currentIndex = idx;
          render();
        }
      });
    });
  }

  function renderStepDetail() {
    const step = steps[currentIndex];
    els.stepBadge.innerText = `Step ${step.index} • ${step.type}`;
    els.stepTitle.innerText = step.title;
    els.stepContent.innerHTML = step.content || '<p>No content yet for this step.</p>';

    const isPractice = step.type === 'practice';
    if (isPractice) {
      els.practicePanel.classList.remove('hidden');
      els.practiceInstruction.innerText = step.practice.instruction || 'Complete the exercise and run tests.';
      if (!els.practiceInput.value && step.practice.starter_content) {
        els.practiceInput.value = step.practice.starter_content;
      }
      els.nextStepBtn.disabled = step.status !== 'passed';
      els.nextStepBtn.classList.toggle('opacity-50', step.status !== 'passed');
      els.nextStepBtn.classList.toggle('cursor-not-allowed', step.status !== 'passed');
    } else {
      els.practicePanel.classList.add('hidden');
      els.nextStepBtn.disabled = false;
      els.nextStepBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }

    els.prevStepBtn.disabled = currentIndex === 0;
    els.prevStepBtn.classList.toggle('opacity-50', currentIndex === 0);
  }

  function updateProgress(summary) {
    if (!summary) return;
    els.progressText.innerText = `${summary.passed}/${summary.total} steps complete`;
    els.progressBar.style.width = `${summary.percent}%`;
  }

  async function completeTheoryStep(step) {
    const response = await fetch(`/steps/${step.id}/complete-theory/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      },
    });

    const data = await response.json();
    if (!response.ok || !data.ok) {
      alert(data.error || 'Could not complete step.');
      return;
    }

    step.status = 'passed';
    const next = steps.find((s) => s.id === data.next_step_id);
    if (next && next.status === 'locked') next.status = 'unlocked';
    updateProgress(data.progress);

    if (currentIndex < steps.length - 1) {
      currentIndex += 1;
    }
    render();
  }

  async function submitPracticeStep(step) {
    const body = new FormData();
    body.append('submission', els.practiceInput.value || '');

    const response = await fetch(`/steps/${step.id}/submit-practice/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      },
      body,
    });

    const data = await response.json();
    if (!response.ok || !data.ok) {
      alert(data.error || 'Could not validate practice step.');
      return;
    }

    els.ruleResults.innerHTML = (data.rule_results || []).map((r) => `
      <div class="rounded-xl border px-3 py-2 ${r.passed ? 'border-emerald-200 bg-emerald-50 text-emerald-700' : 'border-red-200 bg-red-50 text-red-700'}">
        <p class="text-sm font-semibold">${r.name}</p>
        ${r.passed ? '' : `<p class="text-xs mt-1">${r.failure_reason}</p>`}
      </div>
    `).join('');

    if (data.passed) {
      step.status = 'passed';
      const next = steps.find((s) => s.id === data.next_step_id);
      if (next && next.status === 'locked') next.status = 'unlocked';
      updateProgress(data.progress);
      alert('All tests passed. You can continue.');
    }

    render();
  }

  function bindEvents() {
    if (els.topicSelect) {
      els.topicSelect.addEventListener('change', (event) => {
        const url = new URL(window.location.href);
        url.searchParams.set('topic', event.target.value);
        window.location.href = url.toString();
      });
    }

    els.prevStepBtn.addEventListener('click', () => {
      if (currentIndex > 0) {
        currentIndex -= 1;
        render();
      }
    });

    els.nextStepBtn.addEventListener('click', async () => {
      const step = steps[currentIndex];
      if (step.type === 'practice') {
        if (currentIndex < steps.length - 1 && step.status === 'passed') {
          currentIndex += 1;
          render();
        }
        return;
      }
      await completeTheoryStep(step);
    });

    els.runTestsBtn.addEventListener('click', async () => {
      const step = steps[currentIndex];
      if (step.type !== 'practice') return;
      await submitPracticeStep(step);
    });
  }

  function render() {
    renderStepsList();
    renderStepDetail();
  }

  bindEvents();
  render();
})();
