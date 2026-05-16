/* ===== UTILITY ===== */
const $ = id => document.getElementById(id);

function showToast(toastId) {
  const toast = $(toastId);
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2000);
}

async function copyText(text, toastId) {
  try {
    await navigator.clipboard.writeText(text);
    showToast(toastId);
  } catch {
    const el = document.createElement("textarea");
    el.value = text;
    document.body.appendChild(el);
    el.select();
    document.execCommand("copy");
    document.body.removeChild(el);
    showToast(toastId);
  }
}

/* ===== STRENGTH COLORS ===== */
const LABEL_COLORS = {
  "Weak":        "#ff5252",
  "Fair":        "#ffab40",
  "Strong":      "#69f0ae",
  "Very Strong": "#00e676",
};

/* ===== RENDER STRENGTH RESULT ===== */
function renderStrength(data, barId, labelId) {
  const bar   = $(barId);
  const label = $(labelId);
  const color = LABEL_COLORS[data.label] || "#7a7a90";

  bar.style.width           = data.score + "%";
  bar.style.backgroundColor = color;
  label.textContent         = data.label;
  label.style.color         = color;
}

/* ===== CHECKER SECTION ===== */
const passwordInput   = $("password-input");
const strengthSection = $("strength-section");
const strengthBar     = $("strength-bar");
const strengthLabel   = $("strength-label");
const entropyBadge    = $("entropy-badge");
const commonWarning   = $("common-warning");
const feedbackList    = $("feedback-list");

let debounceTimer = null;

passwordInput.addEventListener("input", () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(checkPassword, 120);
});

async function checkPassword() {
  const password = passwordInput.value;

  if (!password) {
    strengthSection.style.display = "none";
    return;
  }

  try {
    const res = await fetch("/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password }),
    });
    const data = await res.json();

    strengthSection.style.display = "block";

    // Strength bar & label
    renderStrength(data, "strength-bar", "strength-label");

    // Entropy badge
    entropyBadge.textContent = `entropy: ${data.entropy} bits`;

    // Common password warning
    commonWarning.style.display = data.is_common ? "block" : "none";

    // Checklist
    Object.entries(data.checks).forEach(([key, passed]) => {
      const el = $(`chk-${key}`);
      if (!el) return;
      el.classList.toggle("pass", passed);
      el.classList.toggle("fail", !passed);
    });

    // Feedback tips
    feedbackList.innerHTML = data.feedback
      .map(tip => `<div class="feedback-item">${tip}</div>`)
      .join("");

  } catch (err) {
    console.error("Check failed:", err);
  }
}

/* ===== TOGGLE VISIBILITY ===== */
$("toggle-visibility").addEventListener("click", () => {
  const isPassword = passwordInput.type === "password";
  passwordInput.type = isPassword ? "text" : "password";
  $("eye-icon").textContent = isPassword ? "🙈" : "👁";
});

/* ===== COPY INPUT ===== */
$("copy-input-btn").addEventListener("click", () => {
  if (passwordInput.value) copyText(passwordInput.value, "copy-toast");
});

/* ===== GENERATOR SECTION ===== */
const lengthSlider  = $("length-slider");
const lengthDisplay = $("length-display");

lengthSlider.addEventListener("input", () => {
  lengthDisplay.textContent = lengthSlider.value;
});

$("generate-btn").addEventListener("click", generatePassword);

async function generatePassword() {
  const length      = parseInt(lengthSlider.value);
  const use_upper   = $("opt-upper").checked;
  const use_lower   = $("opt-lower").checked;
  const use_digits  = $("opt-digits").checked;
  const use_symbols = $("opt-symbols").checked;

  // Ensure at least one option is selected
  if (!use_upper && !use_lower && !use_digits && !use_symbols) {
    alert("Please select at least one character type.");
    return;
  }

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ length, use_upper, use_lower, use_digits, use_symbols }),
    });
    const data = await res.json();

    $("generated-password").textContent = data.password;
    $("generated-output").style.display = "block";

    renderStrength(data.strength, "gen-strength-bar", "gen-strength-label");

  } catch (err) {
    console.error("Generate failed:", err);
  }
}

/* ===== COPY GENERATED ===== */
$("copy-generated-btn").addEventListener("click", () => {
  const pw = $("generated-password").textContent;
  if (pw) copyText(pw, "copy-toast");
});
