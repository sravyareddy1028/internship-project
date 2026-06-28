const messages = document.querySelector("#messages");
const form = document.querySelector("#chatForm");
const input = document.querySelector("#messageInput");
const language = document.querySelector("#language");
const intent = document.querySelector("#intent");
const turns = document.querySelector("#turns");
const engine = document.querySelector("#engine");
const apiForm = document.querySelector("#apiForm");
const apiKeyInput = document.querySelector("#apiKeyInput");
const modelInput = document.querySelector("#modelInput");
const apiStatus = document.querySelector("#apiStatus");
const sessionId = crypto.randomUUID();

const addMessage = (role, text, details = "") => {
  const bubble = document.createElement("article");
  bubble.className = `message ${role}`;
  bubble.innerHTML = `
    <p>${escapeHtml(text)}</p>
    ${details ? `<small>${escapeHtml(details)}</small>` : ""}
  `;
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
};

const sendMessage = async (message) => {
  addMessage("user", message);
  input.value = "";
  input.focus();

  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  const data = await response.json();
  if (!response.ok) {
    addMessage("bot", data.error || "Something went wrong.");
    return;
  }

  language.textContent = data.language_name;
  intent.textContent = data.intent;
  turns.textContent = data.context.turns;
  engine.textContent = data.engine;
  const detail = `Detected: ${data.languages_in_message.join(", ")} · Confidence: ${data.confidence}`;
  addMessage("bot", data.reply, detail);
};

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (message) sendMessage(message);
});

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    input.value = button.dataset.prompt;
    sendMessage(button.dataset.prompt);
  });
});

apiForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const apiKey = apiKeyInput.value.trim();
  const model = modelInput.value.trim() || "openrouter/auto";

  if (!apiKey) {
    apiStatus.textContent = "Enter your OpenRouter API key first.";
    return;
  }

  apiStatus.textContent = "Saving API key...";
  const response = await fetch("/config/openrouter", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_key: apiKey, model }),
  });
  const data = await response.json();

  if (!response.ok) {
    apiStatus.textContent = data.error || "Could not save API key.";
    return;
  }

  apiKeyInput.value = "";
  updateApiStatus(data.openrouter);
  addMessage("bot", "OpenRouter API key saved. Your next message will use online API mode.");
});

const loadApiStatus = async () => {
  const response = await fetch("/config");
  const data = await response.json();
  updateApiStatus(data.openrouter);
};

const updateApiStatus = (status) => {
  modelInput.value = status.model || "openrouter/auto";
  apiStatus.textContent = status.enabled
    ? `Online mode ready: ${status.api_key_preview}`
    : "Offline mode. Paste your OpenRouter key to enable online mode.";
};

const escapeHtml = (value) =>
  value.replace(/[&<>"']/g, (char) =>
    ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    })[char]
  );

addMessage(
  "bot",
  "Hello. I can keep context while you switch between English, Hindi, Spanish, and French."
);
loadApiStatus();