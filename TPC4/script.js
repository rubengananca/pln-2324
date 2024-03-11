function goToAboutPage() {
    window.location.href = 'about.html';
}

function goToHomePage() {
    window.location.href = 'home.html';
}


const playButtons = document.querySelectorAll('.play-button');
const pauseButton = document.querySelector('.pause-button');
let currentAudioElement;

playButtons.forEach((button) => {
    button.addEventListener('click', () => {
        pauseAllAudio();
        const audioId = button.getAttribute('data-audio-id');
        currentAudioElement = document.querySelector(`#${audioId}`);
        currentAudioElement.play();
    });
});

pauseButton.addEventListener('click', () => {
    pauseAllAudio();
});

function pauseAllAudio() {
    const allAudioElements = document.querySelectorAll('audio');
    allAudioElements.forEach((audio) => {
        audio.pause();
    });
}

