// Ambient Lighting Mode: Daylight vs Evening 2700K Glow
document.addEventListener('DOMContentLoaded', function() {
    const glowToggleBtn = document.getElementById('ambient-glow-toggle');
    const isEveningMode = localStorage.getItem('atelier_evening_mode') === 'true';

    if (isEveningMode) {
        document.body.classList.add('evening-glow-mode');
        updateGlowButtonState(true);
    }

    if (glowToggleBtn) {
        glowToggleBtn.addEventListener('click', function() {
            const active = document.body.classList.toggle('evening-glow-mode');
            localStorage.setItem('atelier_evening_mode', active);
            updateGlowButtonState(active);
        });
    }

    function updateGlowButtonState(active) {
        if (!glowToggleBtn) return;
        const icon = glowToggleBtn.querySelector('i');
        const text = glowToggleBtn.querySelector('.btn-label');
        if (active) {
            if (icon) icon.className = 'fa-solid fa-moon text-amber-500';
            if (text) text.textContent = 'Evening 2700K';
            glowToggleBtn.setAttribute('title', 'Switch to Crisp Daylight');
        } else {
            if (icon) icon.className = 'fa-regular fa-sun text-yellow-600';
            if (text) text.textContent = 'Daylight';
            glowToggleBtn.setAttribute('title', 'Switch to Cozy Evening Glow');
        }
    }
});
