/*
  script.js
  Handles all the dynamic behavior across the 3 pages:
  - index.html   -> loadTickets()
  - create.html  -> setupCreateForm()
  - detail.html  -> loadTicketDetail()
*/

// ---------------------------------------------------------
// HOME PAGE: load + search + filter tickets
// ---------------------------------------------------------

function loadTickets() {
  const searchInput = document.getElementById("searchInput");
  const statusFilter = document.getElementById("statusFilter");
  const prevBtn = document.getElementById("prevPageBtn");
  const nextBtn = document.getElementById("nextPageBtn");
  const pageIndicator = document.getElementById("pageIndicator");
  const pagination = document.getElementById("pagination");

  let currentPage = 1;
  const pageSize = 10;

  // Fetches tickets from the API, applying current search/filter/page values
  async function fetchAndRender() {
    const params = new URLSearchParams();
    if (searchInput.value.trim()) params.append("search", searchInput.value.trim());
    if (statusFilter.value) params.append("status", statusFilter.value);
    params.append("page", currentPage);
    params.append("page_size", pageSize);

    const res = await fetch(`/api/tickets?${params.toString()}`);
    const data = await res.json();
    const tickets = data.tickets;

    const tbody = document.getElementById("ticketTableBody");
    const emptyState = document.getElementById("emptyState");
    tbody.innerHTML = "";

    if (tickets.length === 0) {
      emptyState.style.display = "block";
      pagination.style.display = "none";
      return;
    }
    emptyState.style.display = "none";

    tickets.forEach((ticket) => {
      const row = document.createElement("tr");
      row.style.cursor = "pointer";
      row.onclick = () => (window.location.href = `/tickets/${ticket.ticket_id}`);

      const date = new Date(ticket.created_at).toLocaleDateString();
      const statusClass = `status-badge status-${ticket.status.replace(" ", "").toLowerCase()}`;

      row.innerHTML = `
        <td><span class="ticket-chip">${ticket.ticket_id}</span></td>
        <td>${escapeHtml(ticket.customer_name)}</td>
        <td>${escapeHtml(ticket.subject)}</td>
        <td><span class="${statusClass}">${ticket.status}</span></td>
        <td>${date}</td>
      `;
      tbody.appendChild(row);
    });

    // Only show pagination controls if there's more than one page
    if (data.total_pages > 1) {
      pagination.style.display = "flex";
      pageIndicator.textContent = `Page ${data.page} of ${data.total_pages}`;
      prevBtn.disabled = data.page <= 1;
      nextBtn.disabled = data.page >= data.total_pages;
    } else {
      pagination.style.display = "none";
    }
  }

  // Any search/filter change should reset back to page 1
  searchInput.addEventListener("input", () => {
    currentPage = 1;
    fetchAndRender();
  });
  statusFilter.addEventListener("change", () => {
    currentPage = 1;
    fetchAndRender();
  });

  prevBtn.addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      fetchAndRender();
    }
  });
  nextBtn.addEventListener("click", () => {
    currentPage++;
    fetchAndRender();
  });

  fetchAndRender(); // initial load
}

// ---------------------------------------------------------
// CREATE PAGE: handle the new-ticket form submission
// ---------------------------------------------------------

function setupCreateForm() {
  const form = document.getElementById("createTicketForm");
  const errorEl = document.getElementById("formError");

  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // stop normal page-reload form submit

    const payload = {
      customer_name: document.getElementById("customer_name").value,
      customer_email: document.getElementById("customer_email").value,
      subject: document.getElementById("subject").value,
      description: document.getElementById("description").value,
    };

    const res = await fetch("/api/tickets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      errorEl.textContent = "Something went wrong. Please check your inputs and try again.";
      errorEl.style.display = "block";
      return;
    }

    const newTicket = await res.json();
    // Redirect straight to the new ticket's detail page
    window.location.href = `/tickets/${newTicket.ticket_id}`;
  });
}

// ---------------------------------------------------------
// DETAIL PAGE: load ticket info + handle status/note updates
// ---------------------------------------------------------

function loadTicketDetail() {
  const container = document.getElementById("ticketDetail");
  const ticketId = container.dataset.ticketId;

  async function render() {
    const res = await fetch(`/api/tickets/${ticketId}`);

    if (!res.ok) {
      container.innerHTML = `<p>Ticket not found.</p>`;
      return;
    }

    const t = await res.json();

    const notesHtml = t.notes.length
      ? t.notes
          .map(
            (n) => `
        <div class="note">
          <p>${escapeHtml(n.note_text)}</p>
          <span class="note-date">${new Date(n.created_at).toLocaleString()}</span>
        </div>`
          )
          .join("")
      : `<p class="empty-state">No notes yet.</p>`;

    container.innerHTML = `
      <h2>${escapeHtml(t.subject)}</h2>
      <p class="ticket-id"><span class="ticket-chip">${t.ticket_id}</span></p>

      <div class="detail-grid">
        <div><strong>Customer:</strong> ${escapeHtml(t.customer_name)}</div>
        <div><strong>Email:</strong> ${escapeHtml(t.customer_email)}</div>
        <div><strong>Created:</strong> ${new Date(t.created_at).toLocaleString()}</div>
        <div><strong>Last updated:</strong> ${new Date(t.updated_at).toLocaleString()}</div>
      </div>

      <h3>Description</h3>
      <p>${escapeHtml(t.description)}</p>

      <h3>Update Status</h3>
      <select id="statusSelect">
        <option value="Open" ${t.status === "Open" ? "selected" : ""}>Open</option>
        <option value="In Progress" ${t.status === "In Progress" ? "selected" : ""}>In Progress</option>
        <option value="Closed" ${t.status === "Closed" ? "selected" : ""}>Closed</option>
      </select>

      <h3>Add a Note</h3>
      <textarea id="newNote" rows="3" placeholder="Add a comment or note..."></textarea>
      <button id="saveUpdateBtn" class="btn-primary">Save Update</button>

      <h3>Notes</h3>
      <div id="notesList">${notesHtml}</div>
    `;

    document.getElementById("saveUpdateBtn").addEventListener("click", async () => {
      const status = document.getElementById("statusSelect").value;
      const noteText = document.getElementById("newNote").value.trim();

      const body = { status };
      if (noteText) body.notes = noteText;

      const updateRes = await fetch(`/api/tickets/${ticketId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (updateRes.ok) {
        render(); // re-fetch and re-render to show the new note/status
      } else {
        alert("Failed to save update.");
      }
    });
  }

  render();
}

// ---------------------------------------------------------
// Small helper: prevents raw user text from breaking HTML
// (basic XSS protection)
// ---------------------------------------------------------

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}