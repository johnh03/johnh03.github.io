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

function getDistanceLabel(distance, unit) {
  const unitLabels = { m: "meter", km: "kilometer", mile: "mile" };
  return `${distance} ${unitLabels[unit]}${distance === 1 ? "" : "s"}`;
}

function updateResults() {
  const paceSecondsPerKilometer = getPaceSecondsPerKilometer();
  const distanceMeters = getDistanceMeters();
  const distance = Number(distanceInput.value);

  if (paceSecondsPerKilometer === null || distanceMeters === null) {
    inputMessage.textContent = paceSecondsPerKilometer === null
      ? "Enter a pace greater than 0, with seconds between 0 and 59."
      : "Enter a distance greater than 0.";
    customResult.textContent = "--:--";
    resultDistance.textContent = "Check your pace and distance";
    pacePerKm.textContent = "--:-- / km";
    pacePerMile.textContent = "--:-- / mi";
    raceRows.forEach((row) => { row.cells[2].textContent = "--:--"; });
    return;
  }

  inputMessage.textContent = "";
  customResult.textContent = formatTime(paceSecondsPerKilometer * distanceMeters / metersPerKilometer);
  resultDistance.textContent = `for ${getDistanceLabel(distance, distanceUnitInput.value)}`;
  pacePerKm.textContent = `${formatTime(paceSecondsPerKilometer)} / km`;
  pacePerMile.textContent = `${formatTime(paceSecondsPerKilometer * metersPerMile / metersPerKilometer)} / mi`;

  raceRows.forEach((row, index) => {
    row.cells[2].textContent = formatTime(paceSecondsPerKilometer * raceDistances[index].meters / metersPerKilometer);
  });
}

document.querySelectorAll("#converter-form input, #converter-form select").forEach((input) => {
  input.addEventListener("input", updateResults);
  input.addEventListener("change", updateResults);
});

updateResults();