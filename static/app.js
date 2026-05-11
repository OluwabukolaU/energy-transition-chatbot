const fileInput = document.getElementById("fileInput");
const urlInput = document.getElementById("urlInput");
const addUrlBtn = document.getElementById("addUrl");
const dropZone = document.getElementById("dropZone");
const docItems = document.getElementById("docItems");
const documentList = document.getElementById("documentList");
const questionInput = document.getElementById("questionInput");
const askBtn = document.getElementById("askBtn");
const messages = document.getElementById("messages");

let uploadedDocs = [];

// Drag and drop
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("drag-over");
  handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener("change", () => handleFiles(fileInput.files));

// Handle PDF files
async function handleFiles(files) {
  for (const file of files) {
    if (file.type === "application/pdf") {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("/upload", { method: "POST", body: formData });
      const data = await res.json();

      if (data.success) {
        uploadedDocs.push({ name: file.name, id: data.doc_id });
        addDocToList("📄 " + file.name);
        enableChat();
      }
    }
  }
}

// Handle URL
addUrlBtn.addEventListener("click", async () => {
  const url = urlInput.value.trim();
  if (!url.startsWith("https://")) return;

  const res = await fetch("/upload-url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  const data = await res.json();

  if (data.success) {
    uploadedDocs.push({ name: url, id: data.doc_id });
    addDocToList("🌐 " + url);
    urlInput.value = "";
    enableChat();
  }
});

function addDocToList(name) {
  documentList.classList.remove("hidden");
  const li = document.createElement("li");
  li.innerHTML = `✅ ${name}`;
  docItems.appendChild(li);
}

function enableChat() {
  questionInput.disabled = false;
  askBtn.disabled = false;
  questionInput.placeholder = "Ask a research question...";
}

// Ask question
askBtn.addEventListener("click", askQuestion);
questionInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") askQuestion();
});

async function askQuestion() {
  const question = questionInput.value.trim();
  if (!question || uploadedDocs.length === 0) return;

  // Show user message
  addMessage("user", question);
  questionInput.value = "";
  askBtn.disabled = true;

  // Show typing indicator
  const typing = showTyping();

  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      doc_ids: uploadedDocs.map((d) => d.id),
    }),
  });

  const data = await res.json();
  typing.remove();
  addMessage("agent", data.answer);
  askBtn.disabled = false;
}

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;

  if (role === "agent") {
    div.innerHTML = `<span class="agent-label">⚡ Agent</span><div class="content">${text}</div>`;
  } else {
    div.innerHTML = `<p>${text}</p>`;
  }

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function showTyping() {
  const div = document.createElement("div");
  div.className = "message agent";
  div.innerHTML = `
        <span class="agent-label">⚡ Agent</span>
        <div class="typing">
            <span></span><span></span><span></span>
        </div>`;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}
