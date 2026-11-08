const form = document.querySelector("#emotion-form");
const messageInput = document.querySelector("#message");
const charCount = document.querySelector("#char-count");
const analyzeButton = document.querySelector("#analyze-button");
const readout = document.querySelector("#readout");
const emptyState = document.querySelector("#empty-state");
const resultState = document.querySelector("#result-state");
const errorMessage = document.querySelector("#error-message");

const emotionIcons = {
  anger: "😠",
  fear: "😨",
  joy: "😊",
  love: "❤️",
  sadness: "😢",
  surprise: "😲",
};

messageInput.addEventListener("input", () => {
  charCount.textContent = `${messageInput.value.length} / 1000`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message) {
    messageInput.focus();
    return;
  }

  setLoading(true);
  hideError();

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: message }),
    });
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "The analysis could not be completed.");
    }

    showResult(result);
  } catch (error) {
    showError(error.message || "Couldn't reach the prediction service. Please try again.");
  } finally {
    setLoading(false);
  }
});

function setLoading(loading) {
  analyzeButton.disabled = loading;
  analyzeButton.querySelector("span:first-child").textContent = loading ? "Listening..." : "Read the feeling";
  readout.setAttribute("aria-busy", String(loading));
}

function hideError() {
  errorMessage.hidden = true;
  errorMessage.textContent = "";
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}

function showResult(result) {
  emptyState.hidden = true;
  resultState.hidden = false;
  document.querySelector("#emotion-emoji").textContent = emotionIcons[result.emotion] || "🙂";
  document.querySelector("#emotion-name").textContent = result.emotion;
  document.querySelector("#confidence-value").textContent = `${result.confidence.toFixed(1)}%`;

  const probabilities = document.querySelector("#probabilities");
  probabilities.replaceChildren();
  result.probabilities.forEach(({ emotion, probability }) => {
    const row = document.createElement("div");
    row.className = "probability-row";
    row.innerHTML = `
      <span class="probability-name">${escapeHtml(emotion)}</span>
      <span class="probability-track"><span class="probability-fill" style="display:block;width:${Math.max(0, Math.min(100, probability))}%"></span></span>
      <span class="probability-score">${probability.toFixed(1)}%</span>
    `;
    probabilities.append(row);
  });

  document.querySelector("#suggestion").innerHTML = `<strong>A GENTLE NUDGE</strong>${escapeHtml(result.suggestion)}`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}