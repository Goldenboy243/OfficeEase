(function () {
  'use strict';

  const THEORY_FIELDS = ['content'];
  const QUIZ_FIELDS = [
    'quiz_question',
    'quiz_option_1',
    'quiz_option_2',
    'quiz_option_3',
    'quiz_option_4',
    'quiz_correct_answer'
  ];
  const WORKSHOP_FIELDS = [
    'workshop_required_text',
    'workshop_min_words'
  ];

  function toggleField(container, fieldName, visible) {
    const selectors = [
      `.field-${fieldName}`,
      `[class*="field-${fieldName}"]`
    ];
    container.querySelectorAll(selectors.join(',')).forEach((el) => {
      el.style.display = visible ? '' : 'none';
    });
  }

  function updateInlineBlock(container) {
    if (!container) return;

    const selectEl = container.querySelector('select[name$="-step_type"]');
    if (!selectEl) return;

    const stepType = selectEl.value;

    if (stepType === 'theory') {
      THEORY_FIELDS.forEach((f) => toggleField(container, f, true));
      QUIZ_FIELDS.forEach((f) => toggleField(container, f, false));
      WORKSHOP_FIELDS.forEach((f) => toggleField(container, f, false));
    } else if (stepType === 'quiz') {
      THEORY_FIELDS.forEach((f) => toggleField(container, f, false));
      QUIZ_FIELDS.forEach((f) => toggleField(container, f, true));
      WORKSHOP_FIELDS.forEach((f) => toggleField(container, f, false));
    } else if (stepType === 'workshop') {
      // Workshop keeps content (instructions block) + workshop specific config
      THEORY_FIELDS.forEach((f) => toggleField(container, f, true));
      QUIZ_FIELDS.forEach((f) => toggleField(container, f, false));
      WORKSHOP_FIELDS.forEach((f) => toggleField(container, f, true));
    } else {
      // Fallback
      THEORY_FIELDS.forEach((f) => toggleField(container, f, true));
      QUIZ_FIELDS.forEach((f) => toggleField(container, f, true));
      WORKSHOP_FIELDS.forEach((f) => toggleField(container, f, true));
    }
  }

  function initAllInlines() {
    const inlineContainers = document.querySelectorAll('.inline-related, tr.has_original, tr.empty-form');
    inlineContainers.forEach((container) => updateInlineBlock(container));
  }

  function setupListeners() {
    initAllInlines();

    document.addEventListener('change', (e) => {
      if (e.target && e.target.name && e.target.name.endsWith('-step_type')) {
        const container = e.target.closest('.inline-related') || e.target.closest('tr');
        if (container) {
          updateInlineBlock(container);
        }
      }
    });

    if (window.django && window.django.jQuery) {
      window.django.jQuery(document).on('formset:added', (event, $row) => {
        if ($row && $row.length) {
          updateInlineBlock($row[0]);
        }
      });
    }

    // Additional observer to catch dynamically inserted inline DOM nodes
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1) {
            if (node.matches && (node.matches('.inline-related') || node.matches('tr'))) {
              updateInlineBlock(node);
            } else if (node.querySelectorAll) {
              const children = node.querySelectorAll('.inline-related, tr');
              children.forEach((c) => updateInlineBlock(c));
            }
          }
        });
      });
    });

    const targetNode = document.getElementById('inline-group') || document.querySelector('#content-main form');
    if (targetNode) {
      observer.observe(targetNode, { childList: true, subtree: true });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupListeners);
  } else {
    setupListeners();
  }
})();
