let auditLogs = [];

async function loadAuditLogs() {

    try {

        const response =
            await fetch("/audit-logs");

        auditLogs =
            await response.json();

        renderAuditLogs();

        attachAuditEvents();

    } catch (error) {

        console.error(error);
    }
}

function attachAuditEvents() {

    const filter =
        document.getElementById(
            "auditFilter"
        );

    if (filter) {

        filter.onchange =
            renderAuditLogs;
    }

    const exportCsv =
        document.getElementById(
            "exportAuditCsv"
        );

    if (exportCsv) {

        exportCsv.onclick =
            exportAuditCSV;
    }

    const exportPdf =
        document.getElementById(
            "exportAuditPdf"
        );

    if (exportPdf) {

        exportPdf.onclick =
            exportAuditPDF;
    }

    const deleteBtn =
        document.getElementById(
            "deleteAuditsBtn"
        );

    if (deleteBtn) {

        deleteBtn.onclick =
            clearAuditLogs;
    }
}

async function clearAuditLogs() {

    const confirmed = confirm(

        "Are you sure you want to permanently clear all audit logs?\n\nThis action cannot be undone."

    );

    if (!confirmed) {
        return;
    }

    try {

        await fetch(
            "/audit-logs",
            {
                method: "DELETE"
            }
        );

        auditLogs = [];

        renderAuditLogs();

        alert(
            "Audit logs cleared successfully"
        );

    } catch (error) {

        console.error(error);

        alert(
            "Failed to clear audit logs"
        );
    }
}

function renderAuditLogs() {

    const container =
        document.getElementById(
            "auditContainer"
        );

    if (!container) {
        return;
    }

    const filterElement =
        document.getElementById(
            "auditFilter"
        );

    const filter =
        filterElement
            ? filterElement.value
            : "ALL";

    let filtered = auditLogs;

    if (filter !== "ALL") {

        filtered =
            auditLogs.filter(
                log =>
                    log.action_type === filter
            );
    }

    container.innerHTML = "";

    filtered.forEach(log => {

        const row =
            document.createElement("div");

        row.className =
            "audit-row";

        row.innerHTML = `

            <div class="audit-time">

                ${new Date(log.timestamp)
                    .toLocaleString()}

            </div>

            <div class="audit-content">

                <span class="audit-action">

                    ${log.action_type}

                </span>

                —

                <span class="audit-description">

                    ${log.description}

                </span>

            </div>
        `;

        container.appendChild(row);
    });
}

function exportAuditCSV() {

    let csv =
        "Timestamp,Action,Description\n";

    auditLogs.forEach(log => {

        csv +=
            `"${log.timestamp}","${log.action_type}","${log.description}"\n`;
    });

    const blob =
        new Blob(
            [csv],
            {
                type: "text/csv"
            }
        );

    const link =
        document.createElement("a");

    link.href =
        URL.createObjectURL(blob);

    link.download =
        "audit-logs.csv";

    link.click();
}

async function exportAuditPDF() {

    const { jsPDF } =
        window.jspdf;

    const pdf =
        new jsPDF();

    pdf.setFontSize(18);

    pdf.text(
        "Audit Logs Report",
        20,
        20
    );

    let y = 40;

    auditLogs.forEach(log => {

        pdf.setFontSize(11);

        pdf.text(
            `${log.timestamp}`,
            20,
            y
        );

        y += 7;

        pdf.text(
            `${log.action_type}`,
            20,
            y
        );

        y += 7;

        const split =
            pdf.splitTextToSize(
                log.description,
                160
            );

        pdf.text(
            split,
            20,
            y
        );

        y += 15;

        if (y > 270) {

            pdf.addPage();

            y = 20;
        }
    });

    pdf.save(
        "audit-logs.pdf"
    );
}

loadAuditLogs();