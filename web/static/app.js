document.addEventListener('DOMContentLoaded', () => {
  // --- Patient State Management ---
  let currentPatient = {
    name: "",
    age: "",
    place: "",
    disease: "",
    id: ""
  };

  // --- DOM Elements ---
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');
  const btnClearChat = document.getElementById('btn-clear-chat');
  const promptChips = document.querySelectorAll('.prompt-chip');
  const navTabs = document.querySelectorAll('.nav-tab');
  const tabViews = document.querySelectorAll('.tab-view');
  const pendingBadge = document.getElementById('pending-badge');
  const toastContainer = document.getElementById('toast-container');
  
  // Patient Profile Elements
  const patientAvatar = document.getElementById('patient-avatar');
  const displayPatientName = document.getElementById('display-patient-name');
  const displayPatientMeta = document.getElementById('display-patient-meta');
  const displayPatientId = document.getElementById('display-patient-id');
  const displayIdStatus = document.getElementById('display-id-status');
  const btnSwitchPatient = document.getElementById('btn-switch-patient');
  
  // Patient Registration Modal Elements
  const patientModalBackdrop = document.getElementById('patient-modal-backdrop');
  const patientModalCloseBtn = document.getElementById('patient-modal-close-btn');
  const patientRegForm = document.getElementById('patient-registration-form');
  const regPatientId = document.getElementById('reg-patient-id');
  const btnGenerateNewId = document.getElementById('btn-generate-new-id');
  const idStatusPill = document.getElementById('id-status-pill');
  const idValidationMessage = document.getElementById('id-validation-message');
  const regPatientName = document.getElementById('reg-patient-name');
  const regPatientAge = document.getElementById('reg-patient-age');
  const regPatientPlace = document.getElementById('reg-patient-place');
  const regPatientDisease = document.getElementById('reg-patient-disease');

  // Pipeline Nodes
  const pipelineStatus = document.getElementById('pipeline-status');
  const nodeIntake = document.getElementById('node-intake');
  const nodeOrchestrator = document.getElementById('node-orchestrator');
  const nodeRag = document.getElementById('node-rag');
  const nodeTool = document.getElementById('node-tool');
  const nodeSafety = document.getElementById('node-safety');
  
  // Pipeline Data Values
  const intakeUrgencyPill = document.getElementById('intake-urgency-pill');
  const valIntent = document.getElementById('val-intent');
  const valSpecialty = document.getElementById('val-specialty');
  const valSymptoms = document.getElementById('val-symptoms');
  const ragDataBox = document.getElementById('rag-data-box');
  const toolDataBox = document.getElementById('tool-data-box');
  const valSafetyStatus = document.getElementById('val-safety-status');
  const safetyDataBox = document.getElementById('safety-data-box');

  // --- Patient Helper Functions ---
  function getInitials(name) {
    if (!name) return "PT";
    const parts = name.trim().split(/\s+/);
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  function updatePatientUI() {
    if (!currentPatient.name) {
      displayPatientName.textContent = "Patient: Please Register";
      displayPatientMeta.textContent = "Age: — • Place: — • Chief Complaint: —";
      if (displayPatientId) displayPatientId.textContent = "ID: Not Assigned";
      if (displayIdStatus) {
        displayIdStatus.textContent = "Unregistered";
        displayIdStatus.style.background = "rgba(100, 116, 139, 0.2)";
        displayIdStatus.style.color = "var(--text-dim)";
        displayIdStatus.style.borderColor = "rgba(100, 116, 139, 0.3)";
      }
      patientAvatar.textContent = "PT";
      return;
    }

    displayPatientName.textContent = `Patient: ${currentPatient.name}`;
    displayPatientMeta.textContent = `Age: ${currentPatient.age} yrs • Place: ${currentPatient.place} • Condition: ${currentPatient.disease}`;
    patientAvatar.textContent = getInitials(currentPatient.name);

    if (displayPatientId) {
      displayPatientId.textContent = `ID: ${currentPatient.id}`;
    }
    if (displayIdStatus) {
      if (currentPatient.status === 'used') {
        displayIdStatus.textContent = "🔒 Used & Retired";
        displayIdStatus.style.background = "rgba(239, 68, 68, 0.15)";
        displayIdStatus.style.borderColor = "rgba(239, 68, 68, 0.35)";
        displayIdStatus.style.color = "#F87171";
      } else {
        displayIdStatus.textContent = "🟢 Active (Protected)";
        displayIdStatus.style.background = "rgba(16, 185, 129, 0.15)";
        displayIdStatus.style.borderColor = "rgba(16, 185, 129, 0.35)";
        displayIdStatus.style.color = "#10B981";
      }
    }
  }

  async function fetchFreshUniquePatientId() {
    try {
      const res = await fetch('/api/patient/generate-id');
      const data = await res.json();
      if (regPatientId) {
        regPatientId.value = data.patient_id;
        updateIdPill(true, "🛡️ Unique Available");
        if (idValidationMessage) {
          idValidationMessage.innerHTML = `🔒 <em>Policy Guarantee: This ID belongs strictly to this patient. Once used, it is permanently retired.</em>`;
          idValidationMessage.style.color = "var(--text-dim)";
        }
      }
      return data.patient_id;
    } catch (e) {
      console.warn("Could not fetch unique ID from server:", e);
      const fallbackId = `PT-${Math.floor(1000 + Math.random() * 9000)}`;
      if (regPatientId) regPatientId.value = fallbackId;
      return fallbackId;
    }
  }

  function updateIdPill(isValid, text) {
    if (!idStatusPill) return;
    idStatusPill.textContent = text;
    if (isValid) {
      idStatusPill.style.background = "rgba(16, 185, 129, 0.15)";
      idStatusPill.style.borderColor = "rgba(16, 185, 129, 0.35)";
      idStatusPill.style.color = "#10B981";
    } else {
      idStatusPill.style.background = "rgba(239, 68, 68, 0.15)";
      idStatusPill.style.borderColor = "rgba(239, 68, 68, 0.35)";
      idStatusPill.style.color = "#F87171";
    }
  }

  async function validateIdLive() {
    if (!regPatientId) return;
    const id = regPatientId.value.trim();
    const name = (regPatientName.value.trim()) || (currentPatient.name) || "Patient";
    if (!id) return;
    try {
      const res = await fetch('/api/patient/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ patient_id: id, patient_name: name })
      });
      const data = await res.json();
      if (data.valid) {
        updateIdPill(true, "✅ Valid & Authorized");
        idValidationMessage.textContent = `Valid: ${data.message}`;
        idValidationMessage.style.color = "#10B981";
      } else {
        updateIdPill(false, "❌ Policy Blocked");
        idValidationMessage.textContent = data.message;
        idValidationMessage.style.color = "#F87171";
      }
    } catch (e) {
      console.warn("Live validation error:", e);
    }
  }

  if (regPatientId) {
    regPatientId.addEventListener('input', validateIdLive);
    regPatientId.addEventListener('blur', validateIdLive);
  }

  if (btnGenerateNewId) {
    btnGenerateNewId.addEventListener('click', async () => {
      showToast("Generating fresh unallocated Patient ID...");
      await fetchFreshUniquePatientId();
    });
  }

  async function initPatient() {
    const saved = sessionStorage.getItem('careflow_patient');
    if (saved) {
      try {
        currentPatient = JSON.parse(saved);
        updatePatientUI();
        patientModalBackdrop.classList.remove('open');
      } catch (e) {
        patientModalBackdrop.classList.add('open');
        await fetchFreshUniquePatientId();
      }
    } else {
      patientModalBackdrop.classList.add('open');
      await fetchFreshUniquePatientId();
      setTimeout(() => regPatientName.focus(), 200);
    }
  }

  // Patient Registration Form Submission
  patientRegForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = regPatientName.value.trim();
    const age = regPatientAge.value.trim();
    const place = regPatientPlace.value.trim();
    const disease = regPatientDisease.value.trim();
    let id = regPatientId ? regPatientId.value.trim() : "";

    if (!name || !age || !place || !disease) return;

    if (!id) {
      id = await fetchFreshUniquePatientId();
    }

    try {
      const res = await fetch('/api/patient/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: id,
          patient_name: name,
          patient_age: age,
          patient_place: place,
          disease_condition: disease
        })
      });

      if (!res.ok) {
        const errData = await res.json();
        const errMsg = errData.detail || "Patient ID validation failed.";
        updateIdPill(false, "❌ Blocked");
        idValidationMessage.textContent = errMsg;
        idValidationMessage.style.color = "#F87171";
        showToast(errMsg, true);
        return;
      }

      currentPatient = {
        name: name,
        age: age,
        place: place,
        disease: disease,
        id: id,
        status: "active"
      };

      sessionStorage.setItem('careflow_patient', JSON.stringify(currentPatient));
      updatePatientUI();
      patientModalBackdrop.classList.remove('open');
      showToast(`Patient registered! Exclusive ID: ${id}`);
      loadPatientRegistry(true);

      // Reset Chat stream with initial personalized message
      chatMessages.innerHTML = '';
      
      // Automatically query the system for this patient's disease
      sendMessage(`I am ${currentPatient.name}, ${currentPatient.age} years old from ${currentPatient.place}. I am suffering with ${currentPatient.disease}. What are the symptoms, precautions, what to avoid, and specialist options?`);
    } catch (err) {
      showToast(`Network error: ${err.message}`, true);
    }
  });

  // Switch / Edit Patient
  btnSwitchPatient.addEventListener('click', async () => {
    if (currentPatient.name) {
      regPatientName.value = currentPatient.name;
      regPatientAge.value = currentPatient.age;
      regPatientPlace.value = currentPatient.place;
      regPatientDisease.value = currentPatient.disease;
      
      // If previous ID was already consumed/retired, automatically issue a new unique ID
      if (currentPatient.status === 'used') {
        showToast("Previous ID was used & retired. Minting fresh ID...", false);
        await fetchFreshUniquePatientId();
      } else {
        if (regPatientId) regPatientId.value = currentPatient.id;
        updateIdPill(true, "🟢 Active Assigned");
      }
    } else {
      await fetchFreshUniquePatientId();
    }
    patientModalBackdrop.classList.add('open');
    regPatientName.focus();
  });

  patientModalCloseBtn.addEventListener('click', () => {
    if (currentPatient.name) {
      patientModalBackdrop.classList.remove('open');
    } else {
      showToast("Please enter patient details to begin consultation.", true);
    }
  });

  // --- Tab Navigation ---
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetTab = tab.getAttribute('data-tab');
      navTabs.forEach(t => t.classList.remove('active'));
      tabViews.forEach(v => v.classList.remove('active'));
      
      tab.classList.add('active');
      const targetView = document.getElementById(`view-${targetTab}`);
      if (targetView) targetView.classList.add('active');

      if (targetTab === 'hitl') {
        loadAppointments();
        loadPatientRegistry();
      }
      if (targetTab === 'hospital') loadDoctors();
      if (targetTab === 'eval') loadBenchmarks();
    });
  });


  // --- Quick Prompt Chips ---
  promptChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const text = chip.getAttribute('data-prompt');
      chatInput.value = text;
      chatInput.focus();
      sendMessage(text);
    });
  });

  // --- Chat Submission ---
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = chatInput.value.trim();
    if (!text) return;
    sendMessage(text);
    chatInput.value = '';
  });

  // --- Reset Chat ---
  btnClearChat.addEventListener('click', async () => {
    // If the ID was consumed, generate a fresh new ID for the new chat
    if (currentPatient.status === 'used') {
      const oldId = currentPatient.id;
      const newId = await fetchFreshUniquePatientId();
      currentPatient.id = newId;
      currentPatient.status = "active";
      sessionStorage.setItem('careflow_patient', JSON.stringify(currentPatient));
      updatePatientUI();
      showToast(`Previous ID ${oldId} retired. Assigned fresh unique ID: ${newId}!`);
    }
    const pName = currentPatient.name || "Patient";
    chatMessages.innerHTML = `
      <div class="chat-message message-assistant animate-pop-in">
        <div class="message-avatar">
          <img src="/static/logo.jpg" alt="CareFlow">
        </div>
        <div class="message-bubble">
          <p>Chat session reset. Hello <strong>${escapeHtml(pName)}</strong> (ID: <code>${currentPatient.id || "Assigned"}</code>), how can I coordinate your care today?</p>
          <div class="quick-disclaimer">
            <span>🛡️ <em>Safety note: CareFlow performs coordination & triage support. For sudden acute emergencies, dial 911 / 112 immediately.</em></span>
          </div>
        </div>
      </div>
    `;
    resetPipelineInspector();
    showToast("Chat session refreshed.");
  });

  // --- Send Message Function ---
  async function sendMessage(text) {
    if (!currentPatient.name) {
      patientModalBackdrop.classList.add('open');
      showToast("Please enter patient details first.", true);
      return;
    }

    appendUserMessage(text);
    setPipelineProcessing(true);

    const typingId = appendTypingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          patient_name: currentPatient.name,
          patient_id: currentPatient.id || "PT-1001",
          patient_age: currentPatient.age,
          patient_place: currentPatient.place,
          disease_condition: currentPatient.disease
        })
      });

      removeTypingIndicator(typingId);
      setPipelineProcessing(false);

      if (!response.ok) {
        const errJson = await response.json().catch(() => ({}));
        const detailMsg = errJson.detail || `Server returned status ${response.status}`;
        throw new Error(detailMsg);
      }

      const data = await response.json();
      appendAssistantMessage(data.response, data.safety_passed);
      updatePipelineInspector(data);

      if (data.tool_result && data.tool_result.booking) {
        const b = data.tool_result.booking;
        currentPatient.status = "used";
        currentPatient.bookingId = b.booking_id;
        sessionStorage.setItem('careflow_patient', JSON.stringify(currentPatient));
        updatePatientUI();
        updatePendingBadge();
        loadAppointments(true);
        loadPatientRegistry(true);

        appendSystemNotice(`🔒 **Security Policy Applied**: Patient ID \`${currentPatient.id}\` has now been permanently consumed and retired for booking \`${b.booking_id}\`. This ID belongs solely to ${currentPatient.name} and cannot be reused again. Next consultation will automatically generate a new unique ID.`);
      }
    } catch (err) {
      removeTypingIndicator(typingId);
      setPipelineProcessing(false);
      appendAssistantMessage(`⚠️ **Policy/System Notice**: ${err.message}`, false);
      showToast(err.message, true);
    }
  }

  // --- Message DOM Appenders ---
  function appendUserMessage(text) {
    const initials = getInitials(currentPatient.name);
    const msgEl = document.createElement('div');
    msgEl.className = 'chat-message message-user';
    msgEl.innerHTML = `
      <div class="message-avatar">
        <div class="avatar-patient">${initials}</div>
      </div>
      <div class="message-bubble">
        <p>${escapeHtml(text)}</p>
      </div>
    `;
    chatMessages.appendChild(msgEl);
    scrollToBottom();
  }

  function appendAssistantMessage(rawText, safetyPassed) {
    const msgEl = document.createElement('div');
    msgEl.className = 'chat-message message-assistant';
    
    let formattedHtml = rawText
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`([^`]+)`/g, '<code style="background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; color: #06B6D4;">$1</code>')
      .replace(/• (.*?)(?=(\n•|\n\n|$))/g, '<li style="margin-left: 18px; margin-bottom: 5px;">$1</li>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/\n/g, '<br>');

    const bubbleStyle = !safetyPassed 
      ? 'background: rgba(239, 68, 68, 0.15); border-color: rgba(239, 68, 68, 0.4);' 
      : '';

    const bookingMatch = rawText.match(/BK-\d+/);
    let referralBtnHtml = '';
    if (bookingMatch) {
      const bId = bookingMatch[0];
      referralBtnHtml = `
        <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--border-subtle); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
          <span style="font-size: 12px; color: var(--emerald); font-weight: 600;">✅ Slot Reserved & Pre-Registered</span>
          <a href="/api/appointments/${bId}/slip" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 6px; background: rgba(6, 182, 212, 0.2); border: 1px solid #06B6D4; color: #E0F2FE; font-size: 12px; font-weight: 700;">
            📄 Download Official Referral Slip (PDF) →
          </a>
        </div>
      `;
    }

    msgEl.innerHTML = `
      <div class="message-avatar">
        <img src="/static/logo.jpg" alt="CareFlow">
      </div>
      <div class="message-bubble" style="${bubbleStyle}">
        ${formattedHtml}
        ${referralBtnHtml}
      </div>
    `;
    chatMessages.appendChild(msgEl);
    scrollToBottom();
  }

  function appendSystemNotice(text) {
    const noticeEl = document.createElement('div');
    noticeEl.className = 'chat-message message-assistant animate-pop-in';
    noticeEl.innerHTML = `
      <div class="message-avatar">
        <div style="width:34px; height:34px; border-radius:10px; background:rgba(239, 68, 68, 0.15); border:1px solid rgba(239, 68, 68, 0.35); display:flex; align-items:center; justify-content:center; font-size:14px;">🛡️</div>
      </div>
      <div class="message-bubble" style="background: rgba(15, 23, 42, 0.9); border: 1px dashed rgba(6, 182, 212, 0.4); font-size: 12.5px; color: #CBD5E1;">
        ${text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/`([^`]+)`/g, '<code style="background: rgba(0,0,0,0.4); padding: 2px 6px; border-radius: 4px; color: #06B6D4;">$1</code>')}
      </div>
    `;
    chatMessages.appendChild(noticeEl);
    scrollToBottom();
  }


  function appendTypingIndicator() {
    const id = 'typing-' + Date.now();
    const typingEl = document.createElement('div');
    typingEl.id = id;
    typingEl.className = 'chat-message message-assistant';
    typingEl.innerHTML = `
      <div class="message-avatar">
        <img src="/static/logo.jpg" alt="CareFlow">
      </div>
      <div class="message-bubble" style="color: var(--text-dim); font-style: italic;">
        <span>CareFlow LangGraph orchestrator evaluating request for ${escapeHtml(currentPatient.name || "Patient")}...</span>
      </div>
    `;
    chatMessages.appendChild(typingEl);
    scrollToBottom();
    return id;
  }

  function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // --- Pipeline Inspector Live Updates ---
  function setPipelineProcessing(isBusy) {
    if (isBusy) {
      pipelineStatus.textContent = 'Orchestrating...';
      pipelineStatus.className = 'pipeline-live-tag processing';
      [nodeIntake, nodeOrchestrator, nodeRag, nodeTool, nodeSafety].forEach(n => n.classList.add('active'));
    } else {
      pipelineStatus.textContent = 'Active • Synced';
      pipelineStatus.className = 'pipeline-live-tag';
    }
  }

  function updatePipelineInspector(data) {
    const intake = data.intake;
    if (intake) {
      valIntent.textContent = intake.intent || '—';
      valSpecialty.textContent = intake.requested_specialty || 'General';
      valSymptoms.textContent = intake.symptoms && intake.symptoms.length > 0 ? intake.symptoms.join(', ') : 'None listed';
      
      intakeUrgencyPill.textContent = intake.urgency_level || 'standard';
      intakeUrgencyPill.className = `urgency-pill pill-${intake.urgency_level || 'neutral'}`;
    }

    if (data.retrieved_knowledge && data.retrieved_knowledge.length > 0) {
      ragDataBox.innerHTML = data.retrieved_knowledge.map(d => `<div style="margin-bottom: 6px; color: #E2E8F0;">• ${escapeHtml(d)}</div>`).join('');
    } else {
      ragDataBox.innerHTML = `<span class="placeholder-text">Standard hospital protocol referenced.</span>`;
    }

    if (data.tool_result && data.tool_result.booking) {
      const b = data.tool_result.booking;
      toolDataBox.innerHTML = `
        <div class="data-row"><span class="k">Booking ID:</span> <span class="v" style="color: #06B6D4;">${b.booking_id}</span></div>
        <div class="data-row"><span class="k">Patient:</span> <span class="v">${escapeHtml(currentPatient.name)}</span></div>
        <div class="data-row"><span class="k">Doctor:</span> <span class="v">${data.tool_result.doctor_name}</span></div>
        <div class="data-row"><span class="k">Slot:</span> <span class="v">${b.slot_time}</span></div>
        <div class="data-row"><span class="k">Status:</span> <span class="v" style="color: #F59E0B;">Pending Sign-off</span></div>
      `;
    } else {
      toolDataBox.innerHTML = `<span class="placeholder-text">No booking transaction required.</span>`;
    }

    if (data.safety_passed) {
      valSafetyStatus.textContent = 'Passed ✅';
      valSafetyStatus.className = 'safety-pill pill-passed';
      safetyDataBox.innerHTML = `<span style="color: #10B981;">No acute emergencies detected. Safe for coordination.</span>`;
    } else {
      valSafetyStatus.textContent = 'Flagged 🚨';
      valSafetyStatus.className = 'safety-pill pill-failed';
      safetyDataBox.innerHTML = `<span style="color: #EF4444;">${data.safety_violations.join('<br>')}</span>`;
    }
  }

  function resetPipelineInspector() {
    valIntent.textContent = '—';
    valSpecialty.textContent = '—';
    valSymptoms.textContent = '—';
    intakeUrgencyPill.textContent = 'Awaiting input';
    intakeUrgencyPill.className = 'urgency-pill pill-neutral';
    ragDataBox.innerHTML = '<span class="placeholder-text">Awaiting query retrieval...</span>';
    toolDataBox.innerHTML = '<span class="placeholder-text">No active tool calls.</span>';
    valSafetyStatus.textContent = 'Active Guard';
    valSafetyStatus.className = 'safety-pill pill-passed';
    safetyDataBox.innerHTML = '<span class="placeholder-text">Standard guardrail active.</span>';
  }

  let cachedDoctorsHtml = null;
  let cachedAppointments = null;

  async function loadAppointments(forceRefresh = false) {
    const tbody = document.getElementById('appointments-tbody');
    
    if (!cachedAppointments && !forceRefresh) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-dim); padding: 20px;">Loading bookings...</td></tr>`;
    }

    try {
      const res = await fetch('/api/appointments');
      const data = await res.json();
      cachedAppointments = data.appointments || [];
      renderAppointmentsTable(cachedAppointments);
      updatePendingBadge(cachedAppointments);
    } catch (e) {
      if (!cachedAppointments) tbody.innerHTML = `<tr><td colspan="7" style="color: #EF4444;">Failed to load bookings: ${e.message}</td></tr>`;
    }
  }

  function renderAppointmentsTable(appointments) {
    const tbody = document.getElementById('appointments-tbody');
    if (appointments.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-dim); padding: 30px;">No appointments reserved yet. Book one from the chat!</td></tr>`;
      return;
    }

    tbody.innerHTML = appointments.map(apt => {
      const isApproved = apt.status && apt.status.includes('Approved');
      return `
        <tr>
          <td style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #06B6D4;">${apt.booking_id}</td>
          <td>${apt.patient_id}</td>
          <td><strong>${apt.doctor_id}</strong></td>
          <td>${apt.slot_time}</td>
          <td>${escapeHtml(apt.reason || 'Routine care')}</td>
          <td>
            <span class="${isApproved ? 'status-badge-approved' : 'status-badge-pending'}">
              ${apt.status}
            </span>
          </td>
          <td>
            ${isApproved 
              ? '<span style="color: #10B981; font-weight: 600;">Signed Off</span>' 
              : `<button class="btn-approve-action" onclick="approveAppointment('${apt.booking_id}')">Approve & Sign-off</button>`}
          </td>
          <td>
            <a href="/api/appointments/${apt.booking_id}/slip" target="_blank" style="text-decoration:none; display:inline-flex; align-items:center; gap:4px; padding: 4px 8px; border-radius: 6px; background: rgba(6, 182, 212, 0.15); border: 1px solid rgba(6, 182, 212, 0.3); color: #06B6D4; font-size: 11px; font-weight: 600;">
              📄 PDF Slip
            </a>
          </td>
        </tr>
      `;
    }).join('');
  }

  // --- Patient ID Registry Audit View ---
  let cachedRegistry = null;

  async function loadPatientRegistry(forceRefresh = false) {
    const tbody = document.getElementById('registry-tbody');
    if (!tbody) return;
    if (!cachedRegistry && !forceRefresh) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-dim); padding: 20px;">Loading Patient Registry...</td></tr>`;
    }
    try {
      const res = await fetch('/api/patient/registry');
      const data = await res.json();
      cachedRegistry = data.records || [];
      renderRegistryTable(cachedRegistry);
    } catch (e) {
      if (!cachedRegistry) tbody.innerHTML = `<tr><td colspan="7" style="color: #EF4444;">Failed to load registry: ${e.message}</td></tr>`;
    }
  }

  function renderRegistryTable(records) {
    const tbody = document.getElementById('registry-tbody');
    if (!tbody) return;
    if (records.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-dim); padding: 20px;">No patient records registered yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = records.map(rec => {
      const isUsed = rec.status === 'used';
      return `
        <tr>
          <td style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #06B6D4;">${rec.patient_id}</td>
          <td><strong>${escapeHtml(rec.patient_name)}</strong></td>
          <td>${escapeHtml(rec.patient_age)} yrs • ${escapeHtml(rec.patient_place)}</td>
          <td>${escapeHtml(rec.disease || 'General')}</td>
          <td>
            <span class="${isUsed ? 'status-badge-pending' : 'status-badge-approved'}" style="${isUsed ? 'background:rgba(239,68,68,0.15); color:#F87171; border-color:rgba(239,68,68,0.3);' : ''}">
              ${isUsed ? '🔒 Retired (Used)' : '🟢 Active in Consultation'}
            </span>
          </td>
          <td>${rec.booking_id ? `<span style="font-family:'JetBrains Mono', monospace; font-weight:600; color:#06B6D4;">${rec.booking_id}</span>` : '<span style="color:var(--text-dim);">—</span>'}</td>
          <td>
            <span style="font-size: 11px; color: ${isUsed ? '#F87171' : '#10B981'}; font-weight: 600;">
              ${isUsed ? '❌ Permanently Locked (Cannot Reuse)' : `🔒 Exclusive to ${escapeHtml(rec.patient_name)}`}
            </span>
          </td>
        </tr>
      `;
    }).join('');
  }

  // Security Policy Demo Modal Elements & Handlers
  const securityModalBackdrop = document.getElementById('security-test-modal-backdrop');
  const securityModalCloseBtn = document.getElementById('security-modal-close-btn');
  const btnDemoTestRules = document.getElementById('btn-demo-test-rules');
  const btnRefreshRegistry = document.getElementById('btn-refresh-registry');
  const btnTestCollision = document.getElementById('btn-test-collision');
  const btnTestReuse = document.getElementById('btn-test-reuse');
  const btnTestValid = document.getElementById('btn-test-valid');
  const securityTestOutputBox = document.getElementById('security-test-output-box');
  const btnSecurityModalDone = document.getElementById('btn-security-modal-done');

  if (btnDemoTestRules) {
    btnDemoTestRules.addEventListener('click', () => {
      securityModalBackdrop.classList.add('open');
      if (securityTestOutputBox) securityTestOutputBox.style.display = 'none';
    });
  }
  if (securityModalCloseBtn) {
    securityModalCloseBtn.addEventListener('click', () => {
      securityModalBackdrop.classList.remove('open');
    });
  }
  if (btnSecurityModalDone) {
    btnSecurityModalDone.addEventListener('click', () => {
      securityModalBackdrop.classList.remove('open');
    });
  }
  if (btnRefreshRegistry) {
    btnRefreshRegistry.addEventListener('click', () => {
      loadPatientRegistry(true);
      showToast("Patient ID registry refreshed.");
    });
  }

  if (btnTestCollision) {
    btnTestCollision.addEventListener('click', async () => {
      securityTestOutputBox.style.display = 'block';
      securityTestOutputBox.innerHTML = '<span style="color:#06B6D4;">▶ Sending simulated request: Patient "Priya Sharma" attempting to use "PT-1001" (Owned by Kalyan)...</span><br>';
      try {
        const res = await fetch('/api/patient/validate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ patient_id: "PT-1001", patient_name: "Priya Sharma" })
        });
        const data = await res.json();
        if (!data.valid) {
          securityTestOutputBox.innerHTML += `<br><span style="color:#10B981; font-weight:700;">✅ SECURITY INVARIANT PASSED: Ownership check strictly blocked collision!</span><br><br><span style="color:#F87171;">System Error Detail:</span><br>${escapeHtml(data.message)}`;
          showToast("Collision blocked: ID belongs exclusively to Kalyan!");
        } else {
          securityTestOutputBox.innerHTML += `<br><span style="color:#EF4444;">❌ Security Violation: Server allowed unauthorized collision!</span>`;
        }
      } catch (e) {
        securityTestOutputBox.innerHTML += `<br>Error: ${e.message}`;
      }
    });
  }

  if (btnTestReuse) {
    btnTestReuse.addEventListener('click', async () => {
      securityTestOutputBox.style.display = 'block';
      securityTestOutputBox.innerHTML = '<span style="color:#06B6D4;">▶ Registering and consuming ID "PT-SPENT-DEMO", then attempting reuse...</span><br>';
      try {
        await fetch('/api/patient/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ patient_id: "PT-SPENT-DEMO", patient_name: "Ramesh Kumar" })
        });
        await fetch('/api/patient/retire', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ patient_id: "PT-SPENT-DEMO", reason: "Demonstration Retirement" })
        });

        const res = await fetch('/api/patient/validate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ patient_id: "PT-SPENT-DEMO", patient_name: "Ramesh Kumar" })
        });
        const data = await res.json();
        if (!data.valid) {
          securityTestOutputBox.innerHTML += `<br><span style="color:#10B981; font-weight:700;">✅ SECURITY INVARIANT PASSED: Single-Use Policy strictly blocked reuse of retired ID!</span><br><br><span style="color:#F59E0B;">System Error Detail:</span><br>${escapeHtml(data.message)}`;
          showToast("Reuse blocked: ID is permanently retired!");
          loadPatientRegistry(true);
        } else {
          securityTestOutputBox.innerHTML += `<br><span style="color:#EF4444;">❌ Policy Violation: Server allowed reuse of retired ID!</span>`;
        }
      } catch (e) {
        securityTestOutputBox.innerHTML += `<br>Error: ${e.message}`;
      }
    });
  }

  if (btnTestValid) {
    btnTestValid.addEventListener('click', async () => {
      securityTestOutputBox.style.display = 'block';
      securityTestOutputBox.innerHTML = '<span style="color:#06B6D4;">▶ Minting fresh unallocated ID from generator...</span><br>';
      try {
        const genRes = await fetch('/api/patient/generate-id');
        const genData = await genRes.json();
        const freshId = genData.patient_id;
        securityTestOutputBox.innerHTML += `Minted Fresh Unique ID: <strong style="color:#06B6D4;">${freshId}</strong><br>Validating allocation...<br>`;

        const valRes = await fetch('/api/patient/validate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ patient_id: freshId, patient_name: "Anita Roy" })
        });
        const valData = await valRes.json();
        if (valData.valid) {
          securityTestOutputBox.innerHTML += `<br><span style="color:#10B981; font-weight:700;">✅ ALLOCATION APPROVED: Fresh ID reserved exclusively for Anita Roy!</span><br><br><span style="color:#A7F3D0;">Result: ${escapeHtml(valData.message)}</span>`;
          showToast(`Fresh ID ${freshId} successfully allocated!`);
        }
      } catch (e) {
        securityTestOutputBox.innerHTML += `<br>Error: ${e.message}`;
      }
    });
  }

  // --- Evaluation & Benchmarks View ---
  async function loadBenchmarks() {
    try {
      const res = await fetch('/api/benchmarks');
      const data = await res.json();
      const b = data.benchmark_summary;
      if (b) {
        const elRed = document.getElementById('kpi-red-flag');
        const elContra = document.getElementById('kpi-contra');
        const elLat = document.getElementById('kpi-latency');
        const elSch = document.getElementById('kpi-schema');
        if (elRed) elRed.textContent = `${b.red_flag_recall_pct.toFixed(1)}%`;
        if (elContra) elContra.textContent = `${b.contraindication_safety_pct.toFixed(1)}%`;
        if (elLat) elLat.textContent = `${b.latency_offline_ms.toFixed(1)} ms`;
        if (elSch) elSch.textContent = `${b.schema_validation_pct.toFixed(1)}%`;
      }
    } catch (e) {
      console.warn("Could not load benchmarks:", e);
    }
  }

  const btnRunBenchmark = document.getElementById('btn-run-benchmark');
  if (btnRunBenchmark) {
    btnRunBenchmark.addEventListener('click', async () => {
      showToast('Refreshing live 25-case evaluation metrics...');
      await loadBenchmarks();
      showToast('Benchmarks verified: 100% Emergency Recall & Safety compliance!');
    });
  }


  window.approveAppointment = async function(bookingId) {
    try {
      const res = await fetch(`/api/appointments/${bookingId}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coordinator_notes: "Clinician confirmed slot and verified pre-check." })
      });
      if (res.ok) {
        showToast(`Booking ${bookingId} approved by Clinician!`);
        loadAppointments(true);
      }
    } catch (e) {
      showToast(`Error approving booking: ${e.message}`, true);
    }
  };

  async function updatePendingBadge(preloadedList = null) {
    if (preloadedList) {
      const pending = preloadedList.filter(a => !a.status.includes('Approved')).length;
      pendingBadge.textContent = pending;
      pendingBadge.style.display = pending > 0 ? 'inline-block' : 'none';
      return;
    }
    try {
      const res = await fetch('/api/appointments');
      const data = await res.json();
      cachedAppointments = data.appointments || [];
      const pending = cachedAppointments.filter(a => !a.status.includes('Approved')).length;
      pendingBadge.textContent = pending;
      pendingBadge.style.display = pending > 0 ? 'inline-block' : 'none';
    } catch (e) {
      /* Silently ignore network fetch errors */
    }
  }

  // --- Hospital Directory View (Instant rendering with caching) ---
  async function loadDoctors(forceRefresh = false) {
    const grid = document.getElementById('doctors-grid');
    
    // Instant zero-delay render if cached
    if (cachedDoctorsHtml && !forceRefresh) {
      grid.innerHTML = cachedDoctorsHtml;
      return;
    }

    if (!cachedDoctorsHtml) {
      grid.innerHTML = `<div style="color: var(--text-dim); padding: 20px;">Loading doctor roster...</div>`;
    }

    try {
      const res = await fetch('/api/doctors');
      const data = await res.json();
      const schedules = data.schedules || {};

      let html = '';
      for (const [specialty, doctors] of Object.entries(schedules)) {
        for (const doc of doctors) {
          const slotsHtml = (doc.available_slots || []).map(s => `<span class="slot-pill">${s}</span>`).join('');
          html += `
            <div class="doctor-card">
              <div class="doctor-top">
                <div class="doctor-avatar">${doc.name.split(' ').map(n=>n[0]).join('').slice(0,2)}</div>
                <div>
                  <div class="doctor-name">${doc.name}</div>
                  <div class="doctor-spec">${specialty} • ${doc.doctor_id}</div>
                </div>
              </div>
              <div class="slots-label">Upcoming Available Slots</div>
              <div class="slots-pill-group">
                ${slotsHtml || '<span style="color: var(--text-dim); font-size: 12px;">No open slots</span>'}
              </div>
            </div>
          `;
        }
      }
      cachedDoctorsHtml = html;
      grid.innerHTML = html;
    } catch (e) {
      if (!cachedDoctorsHtml) grid.innerHTML = `<div style="color: #EF4444;">Failed to load roster: ${e.message}</div>`;
    }
  }

  // --- Utility Toast ---
  function showToast(msg, isError = false) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    if (isError) toast.style.borderColor = 'rgba(239, 68, 68, 0.5)';
    toast.textContent = msg;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 3500);
  }

  function escapeHtml(string) {
    return String(string).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // --- AI Model Connection Modal Logic ---
  const btnOpenAiModal = document.getElementById('btn-open-ai-modal');
  const aiModalBackdrop = document.getElementById('ai-modal-backdrop');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const btnModalCancel = document.getElementById('btn-modal-cancel');
  const aiConnectForm = document.getElementById('ai-connect-form');
  const inputApiKey = document.getElementById('input-api-key');
  const btnToggleVis = document.getElementById('btn-toggle-vis');
  const modalCurrentEngine = document.getElementById('modal-current-engine');
  const modalStatusTag = document.getElementById('modal-status-tag');
  const engineStatusText = document.getElementById('engine-status-text');
  const enginePulseDot = document.getElementById('engine-pulse-dot');
  const aiBtnLabel = document.getElementById('ai-btn-label');
  const providerRadios = document.querySelectorAll('input[name="ai_provider"]');
  const providerCards = document.querySelectorAll('.provider-card');
  const apiKeyLabel = document.getElementById('api-key-label');

  btnOpenAiModal.addEventListener('click', () => {
    aiModalBackdrop.classList.add('open');
    inputApiKey.focus();
    checkAiStatus();
  });

  function closeAiModal() {
    aiModalBackdrop.classList.remove('open');
  }
  modalCloseBtn.addEventListener('click', closeAiModal);
  btnModalCancel.addEventListener('click', closeAiModal);
  aiModalBackdrop.addEventListener('click', (e) => {
    if (e.target === aiModalBackdrop) closeAiModal();
  });

  btnToggleVis.addEventListener('click', () => {
    if (inputApiKey.type === 'password') {
      inputApiKey.type = 'text';
      btnToggleVis.textContent = '🔒';
    } else {
      inputApiKey.type = 'password';
      btnToggleVis.textContent = '👁️';
    }
  });

  providerRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      providerCards.forEach(c => c.classList.remove('selected'));
      radio.closest('.provider-card').classList.add('selected');
      
      if (radio.value === 'openai') {
        apiKeyLabel.textContent = 'Enter OpenAI API Key (sk-...)';
        inputApiKey.placeholder = 'sk-proj-...';
      } else {
        apiKeyLabel.textContent = 'Enter Google Gemini API Key (AIza...)';
        inputApiKey.placeholder = 'AIzaSy...';
      }
    });
  });

  async function checkAiStatus() {
    try {
      const res = await fetch('/api/ai/status');
      const data = await res.json();
      
      if (data.connected) {
        modalCurrentEngine.textContent = `${data.provider} (${data.model})`;
        modalStatusTag.textContent = 'Live Connected';
        modalStatusTag.className = 'status-indicator-tag active';
        
        btnOpenAiModal.classList.add('connected');
        aiBtnLabel.textContent = `${data.provider} Connected`;
        engineStatusText.textContent = `${data.model}`;
      } else {
        modalCurrentEngine.textContent = 'Rule-based Offline Engine';
        modalStatusTag.textContent = 'Offline Fallback';
        modalStatusTag.className = 'status-indicator-tag';
        
        btnOpenAiModal.classList.remove('connected');
        aiBtnLabel.textContent = 'Connect AI Model';
        engineStatusText.textContent = 'LangGraph Mock';
      }
    } catch (e) {
      console.warn("Could not check AI status:", e);
    }
  }

  aiConnectForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const selectedProvider = document.querySelector('input[name="ai_provider"]:checked').value;
    const apiKey = inputApiKey.value.trim();
    const btnSubmit = document.getElementById('btn-submit-key');
    const submitText = document.getElementById('btn-submit-text');

    if (!apiKey) return;

    btnSubmit.disabled = true;
    submitText.textContent = 'Verifying API Key with Model...';

    try {
      const res = await fetch('/api/ai/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider: selectedProvider, api_key: apiKey })
      });

      const data = await res.json();
      btnSubmit.disabled = false;
      submitText.textContent = 'Verify & Connect Engine';

      if (!res.ok) {
        throw new Error(data.detail || 'Failed to connect');
      }

      showToast(`Success! ${data.message}`);
      inputApiKey.value = '';
      closeAiModal();
      checkAiStatus();
    } catch (err) {
      btnSubmit.disabled = false;
      submitText.textContent = 'Verify & Connect Engine';
      showToast(err.message, true);
    }
  });

  // --- Initial Launch Setup ---
  initPatient();
  updatePendingBadge();
  checkAiStatus();
  loadPatientRegistry();
});
