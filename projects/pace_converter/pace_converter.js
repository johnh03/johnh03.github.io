const metersPerKilometer = 1000;
const metersPerMile = 1609.344;
const raceDistances = [
  { meters: 400 },
  { meters: 800 },
  { meters: 5000 },
  { meters: 10000 },
  { meters: 15000 },
  { meters: 21097.5 },
  { meters: 42195 }
];

const minutesInput = document.querySelector("#pace-minutes");
const secondsInput = document.querySelector("#pace-seconds");
const hoursTotalInput = document.querySelector("#time-hours");
const minutesTotalInput = document.querySelector("#time-minutes");
const secondsTotalInput = document.querySelector("#time-seconds");
const outputUnitInput = document.querySelector("#pace-output-unit");
const paceEntry = document.querySelector("#pace-entry");
const totalTimeEntry = document.querySelector("#total-time-entry");
const resultTitle = document.querySelector("#result-title");
const raceDescription = document.querySelector("#race-description");
const distanceInput = document.querySelector("#distance-value");
const distanceUnitInput = document.querySelector("#distance-unit");
const customResult = document.querySelector("#custom-result");
const resultDistance = document.querySelector("#result-distance");
const pacePerKm = document.querySelector("#pace-per-km");
const pacePerMile = document.querySelector("#pace-per-mile");
const inputMessage = document.querySelector("#input-message");
const raceRows = document.querySelectorAll("#race-results tr");

function formatTime(totalSeconds) {
  const roundedSeconds = Math.round(totalSeconds);
  const hours = Math.floor(roundedSeconds / 3600);
  const minutes = Math.floor((roundedSeconds % 3600) / 60);
  const seconds = roundedSeconds % 60;
  const minutePart = hours > 0 ? String(minutes).padStart(2, "0") : String(minutes);
  const time = [minutePart, String(seconds).padStart(2, "0")];

  if (hours > 0) time.unshift(String(hours).padStart(2, "0"));
  return time.join(":");
}

function getDistanceMeters() {
  const distance = Number(distanceInput.value);
  if (!Number.isFinite(distance) || distance <= 0) return null;

  if (distanceUnitInput.value === "m") return distance;
  if (distanceUnitInput.value === "mile") return distance * metersPerMile;
  return distance * metersPerKilometer;
}

function getPaceSecondsPerKilometer() {
  const minutes = Number(minutesInput.value);
  const seconds = Number(secondsInput.value);
  if (!Number.isInteger(minutes) || minutes < 0 || !Number.isInteger(seconds) || seconds < 0 || seconds > 59) {
    return null;
  }

  const paceSeconds = minutes * 60 + seconds;
  if (paceSeconds <= 0) return null;

  const selectedUnit = document.querySelector('input[name="pace-unit"]:checked').value;
  return selectedUnit === "mile" ? paceSeconds / (metersPerMile / metersPerKilometer) : paceSeconds;
}

function getCalculationMode() {
  return document.querySelector('input[name="calculation-mode"]:checked').value;
}

function getTotalTimeSeconds() {
  const hours = Number(hoursTotalInput.value);
  const minutes = Number(minutesTotalInput.value);
  const seconds = Number(secondsTotalInput.value);

  if (!Number.isInteger(hours) || hours < 0
    || !Number.isInteger(minutes) || minutes < 0 || minutes > 59
    || !Number.isInteger(seconds) || seconds < 0 || seconds > 59) {
    return null;
  }

  const totalSeconds = hours * 3600 + minutes * 60 + seconds;
  return totalSeconds > 0 ? totalSeconds : null;
}

function getDistanceLabel(distance, unit) {
  const unitLabels = { m: "meter", km: "kilometer", mile: "mile" };
  return `${distance} ${unitLabels[unit]}${distance === 1 ? "" : "s"}`;
}

function updateResults() {
  const mode = getCalculationMode();
  const isTotalTimeMode = mode === "total-time";
  const paceSecondsPerKilometer = isTotalTimeMode ? null : getPaceSecondsPerKilometer();
  const distanceMeters = getDistanceMeters();
  const distance = Number(distanceInput.value);
  const totalTimeSeconds = isTotalTimeMode ? getTotalTimeSeconds() : null;

  paceEntry.hidden = isTotalTimeMode;
  totalTimeEntry.hidden = !isTotalTimeMode;
  [hoursTotalInput, minutesTotalInput, secondsTotalInput, outputUnitInput].forEach((input) => {
    input.disabled = !isTotalTimeMode;
  });
  resultTitle.textContent = isTotalTimeMode ? "Calculated running pace" : "Estimated finish time";
  raceDescription.textContent = isTotalTimeMode ? "Based on the calculated pace" : "Based on your current pace";

  const invalidTime = isTotalTimeMode ? totalTimeSeconds === null : paceSecondsPerKilometer === null;
  if (invalidTime || distanceMeters === null) {
    inputMessage.textContent = invalidTime
      ? isTotalTimeMode
        ? "Enter a total time greater than 0, with minutes and seconds between 0 and 59."
        : "Enter a pace greater than 0, with seconds between 0 and 59."
      : "Enter a distance greater than 0.";
    customResult.textContent = "--:--";
    resultDistance.textContent = isTotalTimeMode ? "Check your time and distance" : "Check your pace and distance";
    pacePerKm.textContent = "--:-- / km";
    pacePerMile.textContent = "--:-- / mi";
    raceRows.forEach((row) => { row.cells[2].textContent = "--:--"; });
    return;
  }

  const calculatedPaceSecondsPerKilometer = isTotalTimeMode
    ? totalTimeSeconds * metersPerKilometer / distanceMeters
    : paceSecondsPerKilometer;
  const selectedPace = outputUnitInput.value === "mile"
    ? calculatedPaceSecondsPerKilometer * metersPerMile / metersPerKilometer
    : calculatedPaceSecondsPerKilometer;

  inputMessage.textContent = "";
  customResult.textContent = isTotalTimeMode
    ? `${formatTime(selectedPace)} / ${outputUnitInput.value === "mile" ? "mi" : "km"}`
    : formatTime(calculatedPaceSecondsPerKilometer * distanceMeters / metersPerKilometer);
  resultDistance.textContent = isTotalTimeMode
    ? `for ${getDistanceLabel(distance, distanceUnitInput.value)} in ${formatTime(totalTimeSeconds)}`
    : `for ${getDistanceLabel(distance, distanceUnitInput.value)}`;
  pacePerKm.textContent = `${formatTime(calculatedPaceSecondsPerKilometer)} / km`;
  pacePerMile.textContent = `${formatTime(calculatedPaceSecondsPerKilometer * metersPerMile / metersPerKilometer)} / mi`;

  raceRows.forEach((row, index) => {
    row.cells[2].textContent = formatTime(calculatedPaceSecondsPerKilometer * raceDistances[index].meters / metersPerKilometer);
  });
}

document.querySelectorAll("#converter-form input, #converter-form select").forEach((input) => {
  input.addEventListener("input", updateResults);
  input.addEventListener("change", updateResults);
});

updateResults();