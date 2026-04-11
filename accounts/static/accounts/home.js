document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.counter');
    
    // The "Observer" watches for when the stats enter the screen
    const observerOptions = {
        threshold: 0.6, // Start animation when 60% of the element is visible
        rootMargin: "0px 0px -50px 0px" // Slight offset to ensure it feels natural
    };

    const startCounter = (entries, observer) => {
        entries.forEach(entry => {
            // ONLY start if the element is actually on the screen
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseFloat(counter.getAttribute('data-target'));
                const duration = 2000; // 2 seconds to reach final value
                let startTime = null;

                const animate = (currentTime) => {
                    if (!startTime) startTime = currentTime;
                    const progress = Math.min((currentTime - startTime) / duration, 1);
                    
                    // Power-3 Ease Out (starts fast, slows down perfectly at the end)
                    const easedProgress = 1 - Math.pow(1 - progress, 3);
                    const currentCount = target * easedProgress;

                    // Handle decimals (like 4.9) vs whole numbers (1500)
                    if (target % 1 !== 0) {
                        counter.innerText = currentCount.toFixed(1);
                    } else {
                        counter.innerText = Math.floor(currentCount);
                    }

                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    } else {
                        counter.innerText = target; // Final snap to target
                    }
                };

                requestAnimationFrame(animate);
                // Important: stop watching after animation starts so it doesn't repeat
                observer.unobserve(counter);
            }
        });
    };

    const observer = new IntersectionObserver(startCounter, observerOptions);

    counters.forEach(counter => {
        observer.observe(counter);
    });
});

function toggleDropdown() {
    const dropdown = document.getElementById('user-dropdown');
    dropdown.classList.toggle('hidden');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('user-dropdown');
    const button = document.querySelector('button[onclick*="toggleDropdown"]');
    if (dropdown && !dropdown.contains(event.target) && event.target !== button) {
        dropdown.classList.add('hidden');
    }
});