const presetAffirmations = [
  "You are allowed to begin again, as many times as you need.",
  "You do not have to do everything at once.",
  "Small steps still move you forward.",
  "Rest is part of the work, not a reward for finishing it.",
  "You can meet this moment one breath at a time.",
  "Your best today can look different from your best yesterday.",
  "It is okay to pause and find your footing.",
  "You have handled difficult things before.",
  "Progress does not need to be perfect to count.",
  "You deserve the same patience you give to others.",
  "A slow breath is a small place to start.",
  "You are more than what you get done today."
];

const storageKey = "affirmation-reminder-settings";
const modeInput = document.querySelector("#affirmation-mode");
const customInput = document.querySelector("#custom-affirmations");
const intervalInput = document.querySelector("#interval-minutes");
const intervalModeInput = document.querySelector("#interval-mode");
const minimumIntervalInput = document.querySelector("#minimum-interval");
const maximumIntervalInput = document.querySelector("#maximum-interval");
const fixedIntervalRow = document.querySelector("#fixed-interval-row");
const randomIntervalRow = document.querySelector("#random-interval-row");
const startButton = document.querySelector("#start-button");
const showNowButton = document.querySelector("#show-now-button");
const preview = document.querySelector("#preview-affirmation");
const statusLabel = document.querySelector("#status-label");
const statusDot = document.querySelector("#status-dot");
const nextReminder = document.querySelector("#next-reminder");
const formMessage = document.querySelector("#form-message");
const dialog = document.querySelector("#affirmation-dialog");
const dialogAffirmation = document.querySelector("#dialog-affirmation");

let reminderTimeout;
let countdownInterval;
let nextReminderAt = 0;
let lastAffirmation = "";

function loadSettings() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || "{}");
    customInput.value = Array.isArray(saved.customAffirmations)
      ? saved.customAffirmations.join("\n")
      : "";
    modeInput.value = ["mixed", "custom", "preset"].includes(saved.mode)
      ? saved.mode
      : "mixed";
    intervalInput.value = Number.isInteger(saved.interval) && saved.interval >= 1 && saved.interval <= 240
      ? saved.interval
      : 20;
    intervalModeInput.value = saved.intervalMode === "random" ? "random" : "fixed";
    minimumIntervalInput.value = Number.isInteger(saved.minimumInterval) && saved.minimumInterval >= 1 && saved.minimumInterval <= 240
      ? saved.minimumInterval
      : 15;
    maximumIntervalInput.value = Number.isInteger(saved.maximumInterval) && saved.maximumInterval >= 1 && saved.maximumInterval <= 240
      ? saved.maximumInterval
      : 30;
    updateIntervalControls();
  } catch {
    formMessage.textContent = "Saved settings could not be loaded; you can still use the included affirmations.";
  }
}

function saveSettings() {
  const customAffirmations = getCustomAffirmations();
  localStorage.setItem(storageKey, JSON.stringify({
    customAffirmations,
    mode: modeInput.value,
    interval: Number(intervalInput.value),
    intervalMode: intervalModeInput.value,
    minimumInterval: Number(minimumIntervalInput.value),
    maximumInterval: Number(maximumIntervalInput.value)
  }));
}

function updateIntervalControls() {
  const useRandomInterval = intervalModeInput.value === "random";
  fixedIntervalRow.hidden = useRandomInterval;
  randomIntervalRow.hidden = !useRandomInterval;
}

function getCustomAffirmations() {
  return customInput.value
    .split("\n")
    .map((affirmation) => affirmation.trim())
    .filter(Boolean);
}

function getAffirmationPool() {
  const customAffirmations = getCustomAffirmations();
  if (modeInput.value === "custom") return customAffirmations;
  if (modeInput.value === "preset") return presetAffirmations;
  return [...presetAffirmations, ...customAffirmations];
}

function pickAffirmation() {
  const affirmations = getAffirmationPool();
  if (affirmations.length === 0) return null;

  const choices = affirmations.length > 1
    ? affirmations.filter((affirmation) => affirmation !== lastAffirmation)
    : affirmations;
  const affirmation = choices[Math.floor(Math.random() * choices.length)];
  lastAffirmation = affirmation;
  preview.textContent = affirmation;
  return affirmation;
}

function showAffirmation() {
  const affirmation = pickAffirmation();
  if (!affirmation) {
    formMessage.textContent = "Add at least one affirmation to use your list, or choose the included affirmations.";
    return false;
  }

  formMessage.textContent = "";
  dialogAffirmation.textContent = affirmation;
  if (!dialog.open) dialog.showModal();
  return true;
}

function renderCountdown() {
  const secondsLeft = Math.max(0, Math.ceil((nextReminderAt - Date.now()) / 1000));
  const minutes = Math.floor(secondsLeft / 60);
  const seconds = String(secondsLeft % 60).padStart(2, "0");
  nextReminder.textContent = `Next reminder in ${minutes}:${seconds}`;
}

function stopReminders() {
  clearTimeout(reminderTimeout);
  clearInterval(countdownInterval);
  reminderTimeout = undefined;
  countdownInterval = undefined;
  startButton.textContent = "Start reminders";
  statusLabel.textContent = "Reminders are paused";
  statusDot.classList.remove("is-active");
  nextReminder.textContent = "Start a timer when you are ready.";
}

function getIntervalBounds() {
  if (intervalModeInput.value === "random") {
    const minimum = Number(minimumIntervalInput.value);
    const maximum = Number(maximumIntervalInput.value);
    if (!Number.isInteger(minimum) || !Number.isInteger(maximum) || minimum < 1 || maximum > 240 || minimum > maximum) {
      formMessage.textContent = "Choose a valid random range between 1 and 240 minutes, with the minimum no greater than the maximum.";
      minimumIntervalInput.focus();
      return null;
    }
    return { minimum, maximum };
  }

  const interval = Number(intervalInput.value);
  if (!Number.isInteger(interval) || interval < 1 || interval > 240) {
    formMessage.textContent = "Choose an interval between 1 and 240 minutes.";
    intervalInput.focus();
    return null;
  }
  return { minimum: interval, maximum: interval };
}

function scheduleNextReminder() {
  const bounds = getIntervalBounds();
  if (bounds === null) {
    stopReminders();
    return;
  }
  const interval = Math.floor(Math.random() * (bounds.maximum - bounds.minimum + 1)) + bounds.minimum;
  const intervalMilliseconds = interval * 60 * 1000;
  nextReminderAt = Date.now() + intervalMilliseconds;
  renderCountdown();
  clearInterval(countdownInterval);
  countdownInterval = setInterval(renderCountdown, 1000);
  reminderTimeout = setTimeout(() => {
    showAffirmation();
    scheduleNextReminder();
  }, intervalMilliseconds);
}

function startReminders() {
  if (getIntervalBounds() === null) return;
  if (getAffirmationPool().length === 0) {
    formMessage.textContent = "Add an affirmation or choose the included affirmations before starting.";
    customInput.focus();
    return;
  }

  saveSettings();
  clearTimeout(reminderTimeout);
  clearInterval(countdownInterval);
  startButton.textContent = "Pause reminders";
  statusLabel.textContent = "Reminders are on";
  statusDot.classList.add("is-active");
  scheduleNextReminder();
}

loadSettings();
preview.textContent = pickAffirmation() || presetAffirmations[0];

startButton.addEventListener("click", () => {
  if (reminderTimeout) {
    stopReminders();
  } else {
    startReminders();
  }
});

showNowButton.addEventListener("click", showAffirmation);
document.querySelector("#another-button").addEventListener("click", showAffirmation);
document.querySelector("#close-dialog-button").addEventListener("click", () => dialog.close());

for (const input of [modeInput, customInput, intervalInput, minimumIntervalInput, maximumIntervalInput]) {
  input.addEventListener("change", () => {
    saveSettings();
    formMessage.textContent = "Your settings are saved.";
  });
}

intervalModeInput.addEventListener("change", () => {
  updateIntervalControls();
  saveSettings();
  formMessage.textContent = "Your settings are saved.";
});

customInput.addEventListener("input", () => {
  saveSettings();
  formMessage.textContent = "Saved.";
});

dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});