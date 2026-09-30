// Calming Atelier Ambient Soundscape (Web Audio API Synthesizer)
let audioCtx = null;
let soundGain = null;
let isSoundPlaying = false;
let noiseSource = null;
let chimeInterval = null;

function initAtelierAudio() {
    if (audioCtx) return;
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContext();
    soundGain = audioCtx.createGain();
    soundGain.gain.setValueAtTime(0.001, audioCtx.currentTime);
    soundGain.connect(audioCtx.destination);
}

function startWarmHum() {
    initAtelierAudio();
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }

    // Generate soft brown/pink noise (like a warm ceramic kiln breeze)
    const bufferSize = audioCtx.sampleRate * 2;
    const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        output[i] = (lastOut + (0.02 * white)) / 1.02;
        lastOut = output[i];
        output[i] *= 1.5;
    }

    noiseSource = audioCtx.createBufferSource();
    noiseSource.buffer = noiseBuffer;
    noiseSource.loop = true;

    // Filter to warm deep soothing frequencies
    const filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(220, audioCtx.currentTime);

    noiseSource.connect(filter);
    filter.connect(soundGain);
    noiseSource.start();

    // Fade in
    soundGain.gain.linearRampToValueAtTime(0.08, audioCtx.currentTime + 1.5);

    // Periodic gentle harmonic ceramic chime
    chimeInterval = setInterval(playGentleChime, 6000);
}

function playGentleChime() {
    if (!audioCtx || !isSoundPlaying) return;
    const notes = [523.25, 659.25, 783.99, 1046.50, 1318.51]; // C pentatonic
    const freq = notes[Math.floor(Math.random() * notes.length)];

    const osc = audioCtx.createOscillator();
    const chimeGain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);

    chimeGain.gain.setValueAtTime(0.001, audioCtx.currentTime);
    chimeGain.gain.exponentialRampToValueAtTime(0.035, audioCtx.currentTime + 0.08);
    chimeGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 2.8);

    osc.connect(chimeGain);
    chimeGain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 3.0);
}

function stopWarmHum() {
    if (!audioCtx) return;
    clearInterval(chimeInterval);
    if (soundGain) {
        soundGain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 1.0);
        setTimeout(() => {
            if (noiseSource) {
                try { noiseSource.stop(); } catch(e) {}
            }
        }, 1100);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const soundBtn = document.getElementById('atelier-sound-toggle');
    if (!soundBtn) return;

    soundBtn.addEventListener('click', function() {
        if (!isSoundPlaying) {
            startWarmHum();
            isSoundPlaying = true;
            soundBtn.classList.add('playing');
            soundBtn.querySelector('i').className = 'fa-solid fa-volume-high text-emerald-600';
            const label = soundBtn.querySelector('.btn-label');
            if (label) label.textContent = 'Kiln Sound: On';
        } else {
            stopWarmHum();
            isSoundPlaying = false;
            soundBtn.classList.remove('playing');
            soundBtn.querySelector('i').className = 'fa-solid fa-volume-xmark text-stone-400';
            const label = soundBtn.querySelector('.btn-label');
            if (label) label.textContent = 'Kiln Sound: Off';
        }
    });
});
