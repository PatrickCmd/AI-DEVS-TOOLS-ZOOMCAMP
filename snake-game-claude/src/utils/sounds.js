/**
 * Simple sound effects using Web Audio API
 */

let audioContext = null;

const initAudioContext = () => {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
};

/**
 * Play a beep sound with specified frequency and duration
 */
const playTone = (frequency, duration, volume = 0.3) => {
  const ctx = initAudioContext();

  const oscillator = ctx.createOscillator();
  const gainNode = ctx.createGain();

  oscillator.connect(gainNode);
  gainNode.connect(ctx.destination);

  oscillator.frequency.value = frequency;
  oscillator.type = 'square';

  gainNode.gain.setValueAtTime(volume, ctx.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration);

  oscillator.start(ctx.currentTime);
  oscillator.stop(ctx.currentTime + duration);
};

/**
 * Sound effects
 */
export const sounds = {
  eat: () => {
    // Happy eating sound - ascending notes
    playTone(400, 0.05);
    setTimeout(() => playTone(600, 0.05), 50);
  },

  gameOver: () => {
    // Sad game over sound - descending notes
    playTone(400, 0.1);
    setTimeout(() => playTone(300, 0.1), 100);
    setTimeout(() => playTone(200, 0.2), 200);
  },

  move: () => {
    // Subtle movement sound
    playTone(200, 0.02, 0.1);
  },

  newHighScore: () => {
    // Victory sound - triumphant notes
    playTone(523, 0.1); // C5
    setTimeout(() => playTone(659, 0.1), 100); // E5
    setTimeout(() => playTone(784, 0.15), 200); // G5
  },
};

/**
 * Play a sound effect if sound is enabled
 */
export const playSound = (soundName, soundEnabled) => {
  if (!soundEnabled || !sounds[soundName]) {
    return;
  }

  try {
    sounds[soundName]();
  } catch (error) {
    console.error('Error playing sound:', error);
  }
};
