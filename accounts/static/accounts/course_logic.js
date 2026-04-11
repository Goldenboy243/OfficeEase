// tracking variables
let currentIdx = 0;
let completedLessons = []; // Stores IDs of finished lessons

function loadLesson(idx) {
    if (idx < 0 || idx >= dbLessons.length) return;
    
    currentIdx = idx;
    const l = dbLessons[idx];
    
    // 1. Update Text & Theory
    document.getElementById('module-label').innerText = "Module " + l.moduleIndex + " • Lesson " + l.label;
    document.getElementById('lesson-title').innerText = l.title;
    document.getElementById('lesson-theory').innerHTML = l.theory;
    
    // 2. Update Iframe
    const frame = document.getElementById('word-frame');
    if (frame) frame.src = l.embed_url || "";

    // 3. Render Quiz
    const quizContainer = document.getElementById('quiz-container');
    if (quizContainer) {
        quizContainer.innerHTML = l.questions.map((q, i) => `
            <div class="bg-white border border-slate-200 rounded-xl overflow-hidden mb-2">
                <button onclick="toggleAcc(${i})" class="w-full text-left p-4 font-bold text-sm flex justify-between items-center hover:bg-slate-50">
                    Q${i+1}: ${q.q} <i id="icon-${i}" class="fa-solid fa-chevron-down opacity-30 text-[10px]"></i>
                </button>
                <div id="acc-${i}" class="accordion-content px-4 space-y-2">
                    ${q.opts.map((opt, oi) => `
                        <label class="flex items-center gap-3 text-xs p-3 bg-slate-50 rounded-lg cursor-pointer hover:bg-blue-50">
                            <input type="radio" name="q-${i}" value="${oi}"> ${opt}
                        </label>`).join('')}
                </div>
            </div>
        `).join('');
    }
    
    updateUI();
}

function updateUI() {
    dbLessons.forEach((l, i) => {
        const btn = document.getElementById(`btn-${l.id}`);
        const icon = document.getElementById(`check-${l.id}`);
        
        if (!btn) return;

        // Highlight active lesson
        if (i === currentIdx) {
            btn.classList.add('active-lesson');
            // Auto-open the module dropdown if it's hidden
            document.getElementById(`mod-${l.moduleIndex}`).classList.remove('hidden');
        } else {
            btn.classList.remove('active-lesson');
        }

        // Mark completed lessons
        if (completedLessons.includes(l.id)) {
            icon.className = "fa-solid fa-circle-check text-emerald-500";
        } else {
            icon.className = "fa-regular fa-circle text-slate-300";
        }
    });

    calculateProgress();
}

function calculateProgress() {
    // 1. Create a map to store finished counts for each module
    const finishedByModule = {};

    // 2. Loop through every lesson in your database array
    dbLessons.forEach(lesson => {
        // If this lesson is finished...
        if (completedLessons.includes(lesson.id)) {
            // ...add 1 to its module's count
            finishedByModule[lesson.moduleIndex] = (finishedByModule[lesson.moduleIndex] || 0) + 1;
        }
    });

    // 3. Update the HTML spans for each module
    // We look for every module that exists in dbLessons
    const uniqueModules = [...new Set(dbLessons.map(l => l.moduleIndex))];
    
    uniqueModules.forEach(modIdx => {
        const span = document.getElementById(`mod-prog-${modIdx}`);
        if (span) {
            span.innerText = finishedByModule[modIdx] || 0;
        }
    });

    // 4. Update the "X of Y Modules Complete" at the very top
    updateOverallProgress();
}

function updateOverallProgress() {
    let completedModulesCount = 0;
    
    // Get all module lists from the sidebar
    const moduleLists = document.querySelectorAll('[id^="mod-"]'); // matches mod-1, mod-2, etc.
    const totalModules = moduleLists.length;

    moduleLists.forEach((listDiv, index) => {
        const modId = index + 1;
        const span = document.getElementById(`mod-prog-${modId}`);
        
        if (span) {
            const currentDone = parseInt(span.innerText);
            // Count how many buttons (lessons) are inside this specific module div
            const totalInModule = listDiv.querySelectorAll('button').length;

            if (currentDone === totalInModule && totalInModule > 0) {
                completedModulesCount++;
            }
        }
    });

    const overallText = document.getElementById('overall-progress');
    if (overallText) {
        overallText.innerText = `${completedModulesCount} of ${totalModules} Modules complete`;
    }
}

function checkAllAnswers() {
    const l = dbLessons[currentIdx];
    let wrong = [];
    
    l.questions.forEach((q, i) => {
        const sel = document.querySelector(`input[name="q-${i}"]:checked`);
        if (!sel || sel.value !== q.ans) wrong.push(i + 1);
    });

    if (wrong.length === 0) {
        if (!completedLessons.includes(l.id)) {
            completedLessons.push(l.id);
        }
        document.getElementById('feedback-correct').classList.remove('hidden');
        updateUI();
    } else {
        document.getElementById('error-details').innerHTML = `Check Question(s): ${wrong.join(', ')}`;
        document.getElementById('feedback-wrong').classList.remove('hidden');
    }
}

function moveToNextLesson() {
    closeFeedback();
    if (currentIdx < dbLessons.length - 1) {
        loadLesson(currentIdx + 1);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Helpers
function toggleAcc(i) {
    document.getElementById(`acc-${i}`).classList.toggle('open');
    document.getElementById(`icon-${i}`).classList.toggle('rotate-180');
}

function closeFeedback() {
    document.getElementById('feedback-correct').classList.add('hidden');
    document.getElementById('feedback-wrong').classList.add('hidden');
}

function jumpToLessonById(id) {
    const idx = dbLessons.findIndex(l => l.id === id);
    if (idx !== -1) loadLesson(idx);
}