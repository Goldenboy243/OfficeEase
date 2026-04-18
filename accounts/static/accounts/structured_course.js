(function () {
  const dataNode = document.getElementById('steps-data');
  if (!dataNode) return;

  const steps = JSON.parse(dataNode.textContent || '[]');
  if (!steps.length) return;

  const els = {
    moduleSelect: document.getElementById('module-select'),
    stepsList: document.getElementById('steps-list'),
    stepBadge: document.getElementById('step-badge'),
    stepTitle: document.getElementById('step-title'),
    stepContent: document.getElementById('step-content'),
    quizPanel: document.getElementById('quiz-panel'),
    quizQuestion: document.getElementById('quiz-question'),
    quizOptions: document.getElementById('quiz-options'),
    workshopPanel: document.getElementById('workshop-panel'),
    workshopNote: document.getElementById('workshop-note'),
    workshopFile: document.getElementById('workshop-file'),
    submitWorkshopBtn: document.getElementById('submit-workshop-btn'),
    workshopResult: document.getElementById('workshop-result'),
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

  function selectedQuizOption(stepId) {
    const checked = document.querySelector(`input[name=\"quiz-${stepId}\"]:checked`);
    return checked ? checked.value : '';
  }

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

    const isQuiz = step.type === 'quiz' || Boolean(step.quiz && step.quiz.question);
    const isWorkshop = step.type === 'workshop';

    if (isQuiz) {
      els.stepContent.innerHTML = '<p>Read the question below and choose one answer to continue.</p>';
    } else if (isWorkshop) {
      els.stepContent.innerHTML = step.content || '<p>Complete the workshop activity described below.</p>';
    } else {
      els.stepContent.innerHTML = step.content || '<p>Review this step and click Next to continue.</p>';
    }

    els.quizPanel.classList.toggle('hidden', !isQuiz);
    els.workshopPanel.classList.toggle('hidden', !isWorkshop);

    if (isQuiz) {
      els.quizQuestion.innerText = step.quiz.question || 'Answer the question to continue.';
      const options = (step.quiz.options || []).filter(Boolean);
      els.quizOptions.innerHTML = options.map((opt, idx) => `
        <label class="flex items-start gap-3 rounded-xl border border-indigo-200 bg-white p-3 text-sm text-slate-700">
          <input type="radio" name="quiz-${step.id}" value="${idx}" class="mt-1" ${step.status === 'passed' ? 'disabled' : ''}>
          <span>${opt}</span>
        </label>
      `).join('');
    }

    if (isWorkshop) {
      const minWords = (step.workshop && step.workshop.min_words) || 20;
      const requiredText = step.workshop && step.workshop.required_text
        ? `Required text: "${step.workshop.required_text}".`
        : '';
      els.workshopNote.innerText = `Create the task in Microsoft Word and upload a .docx file. Minimum ${minWords} words. ${requiredText}`.trim();
      if (els.workshopResult) {
        els.workshopResult.innerText = step.status === 'passed' ? 'Workshop already passed.' : '';
      }
    }

    const isLocked = step.status === 'locked';
    els.nextStepBtn.disabled = isLocked;
    els.nextStepBtn.classList.toggle('opacity-50', isLocked);
    els.nextStepBtn.classList.toggle('cursor-not-allowed', isLocked);

    els.prevStepBtn.disabled = currentIndex === 0;
    els.prevStepBtn.classList.toggle('opacity-50', currentIndex === 0);
  }

  async function submitWorkshopStep(step) {
    const file = els.workshopFile && els.workshopFile.files ? els.workshopFile.files[0] : null;
    if (!file) {
      alert('Please choose a .docx file to upload.');
      return;
    }

    const body = new FormData();
    body.append('workshop_file', file);

    const response = await fetch(`/steps/${step.id}/submit-workshop/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      },
      body,
    });

    const data = await response.json();
    if (!response.ok || !data.ok) {
      alert(data.error || 'Could not validate workshop file.');
      return;
    }

    if (els.workshopResult) {
      els.workshopResult.innerText = data.feedback || '';
    }

    if (data.passed) {
      step.status = 'passed';
      const next = steps.find((s) => s.id === data.next_step_id);
      if (next && next.status === 'locked') next.status = 'unlocked';
      updateProgress(data.progress);
      render();
    }
  }

  function updateProgress(summary) {
    if (!summary) return;
    els.progressText.innerText = `${summary.passed}/${summary.total} steps complete`;
    els.progressBar.style.width = `${summary.percent}%`;
  }

  async function completeTheoryStep(step, payload) {
    const body = new FormData();
    if (payload && payload.selected_option !== undefined) {
      body.append('selected_option', payload.selected_option);
    }

    const response = await fetch(`/steps/${step.id}/complete-theory/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
      },
      body,
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

  function bindEvents() {
    if (els.moduleSelect) {
      els.moduleSelect.addEventListener('change', (event) => {
        const url = new URL(window.location.href);
        url.searchParams.set('module', event.target.value);
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
      if (step.status === 'locked') {
        return;
      }

      if (step.type === 'workshop' && step.status !== 'passed') {
        alert('Upload and pass the workshop file first.');
        return;
      }

      if (step.status === 'passed') {
        if (currentIndex < steps.length - 1) {
          currentIndex += 1;
          render();
        }
        return;
      }

      const payload = {};
      if (step.type === 'quiz') {
        payload.selected_option = selectedQuizOption(step.id);
      }
      await completeTheoryStep(step, payload);
    });

    if (els.submitWorkshopBtn) {
      els.submitWorkshopBtn.addEventListener('click', async () => {
        const step = steps[currentIndex];
        if (step.type !== 'workshop') {
          return;
        }
        if (step.status === 'locked') {
          alert('This workshop is locked. Complete previous steps first.');
          return;
        }
        await submitWorkshopStep(step);
      });
    }
  }

  function render() {
    renderStepsList();
    renderStepDetail();
  }

  bindEvents();
  render();
})();
