window.candidates =
    window.candidates || [];

let currentView = "card";

let sortDescending = true;

let topK = 3;

const scientists = [

    {
        name: "Dr. R. Srinivasan",
        specialization: "artificial intelligence",
        division: "AI & Intelligent Systems",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Ananya Mehta",
        specialization: "cybersecurity",
        division: "Cyber Defence Systems",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Vivek Sharma",
        specialization: "machine learning",
        division: "Machine Learning Research",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Priya Nair",
        specialization: "computer vision",
        division: "Vision & Image Processing",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Arvind Rao",
        specialization: "data science",
        division: "Data Analytics Division",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Sneha Kulkarni",
        specialization: "nlp",
        division: "Language Computing Systems",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Karan Malhotra",
        specialization: "cloud computing",
        division: "Distributed Computing Systems",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Neeraj Bhatia",
        specialization: "embedded systems",
        division: "Embedded & Real-Time Systems",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Ishita Verma",
        specialization: "web development",
        division: "Software Applications Group",
        maxInterns: 10,
        assigned: []
    },

    {
        name: "Dr. Aditya Kapoor",
        specialization: "network security",
        division: "Secure Network Systems",
        maxInterns: 10,
        assigned: []
    }
];

async function deleteCandidate(
    candidateId
) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this candidate?\n\nThis action will permanently remove the candidate record, evaluation score, semantic analysis, and allocation details from the database."
        );

    if (!confirmed) {

        return;
    }

    try {

        const response =
            await fetch(
                `/candidate/${candidateId}`,
                {
                    method: "DELETE"
                }
            );

        const data =
            await response.json();

        alert(data.message);

        await loadCandidates();

    } catch (error) {

        console.error(error);

        alert(
            "Failed to delete candidate"
        );
    }
}

async function loadCandidates() {

    try {

        const response =
            await fetch("/candidates");

        candidates =
            await response.json();

        renderCandidates();

        attachEvents();

    } catch (error) {

        console.error(error);
    }
}

function attachEvents() {

    const viewSelector =
        document.getElementById(
            "viewSelector"
        );

    if (viewSelector) {

        viewSelector.onchange =
            function () {

                currentView =
                    this.value;

                renderCandidates();
            };
    }

    const sortBtn =
        document.getElementById(
            "sortBtn"
        );

    if (sortBtn) {

        sortBtn.onclick =
            function () {

                sortDescending =
                    !sortDescending;

                renderCandidates();
            };
    }

    const selectedOnly =
        document.getElementById(
            "selectedOnly"
        );

    if (selectedOnly) {

        selectedOnly.onchange =
            renderCandidates;
    }

    const topKInput =
        document.getElementById(
            "topKInput"
        );

    if (topKInput) {

        topKInput.oninput = async function() {

            topK =
                parseInt(this.value) || 3;

            await fetch(
                `/allocate-scientists?top_k=${topK}`,
                {
                    method: "POST"
                }
            );

            await loadCandidates();
        };
    }
    const exportBtn =
    document.getElementById(
        "exportBtn"
    );

    if (exportBtn) {
        exportBtn.onclick =
            function () {
                const dropdown =
                    document.getElementById(
                        "exportDropdown"
                    );

                dropdown.style.display =
                    dropdown.style.display === "block"
                    ? "none"
                    : "block";
            };
    }
    const downloadBtn =
    document.getElementById(
        "downloadCsvBtn"
    );

    if (downloadBtn) {

        downloadBtn.onclick =
            exportSelectedColumns;
    }
}

function getFilteredCandidates() {

    let filtered =
        [...candidates];

    const selectedOnly =
        document.getElementById(
            "selectedOnly"
        );

    if (
        selectedOnly &&
        selectedOnly.checked
    ) {

        filtered =
            filtered.filter(
                c => c.selected
            );
    }

    filtered.sort((a, b) =>

        sortDescending
        ? b.score - a.score
        : a.score - b.score
    );

    return filtered;
}

function renderCandidates() {

    const container =
        document.getElementById(
            "candidateContainer"
        );

    if (!container) {
        return;
    }
    const filtered =
        getFilteredCandidates();

    if (currentView === "table") {

        renderTableView(
            filtered,
            container
        );

    } else {

        renderCardView(
            filtered,
            container
        );
    }
}

function renderCardView(
    data,
    container
) {

    container.innerHTML =
        `<div class="candidate-grid"></div>`;

    const grid =
        container.querySelector(
            ".candidate-grid"
        );

    data.forEach((candidate, index) => {

        const highlighted =
            index < topK;

        const skills =
            candidate.skills
            ? candidate.skills
                .split(",")
                .map(skill =>

                    `<span class="skill-chip">
                        ${skill.trim()}
                    </span>`

                )
                .join("")
            : "";

        const reasons =
            candidate.reasons
            ? candidate.reasons
                .split(",")
                .map(reason =>

                    `<li>${reason.trim()}</li>`

                )
                .join("")
            : "";

        const card =
            document.createElement("div");

        card.className =
            "candidate-card-ui";

        if (highlighted) {

            card.classList.add(
                "top-highlight"
            );
        }

        card.innerHTML = `

    <div class="candidate-top-ui">

        <div>

            <h2>
                ${candidate.name || "Unknown"}
            </h2>

            <p>
                GPA:
                ${candidate.gpa || "N/A"}
            </p>

        </div>

        <div class="
            ${candidate.selected
                ? "selected-pill"
                : "rejected-pill"}
        ">

            ${candidate.selected
                ? "SELECTED"
                : "REJECTED"}

        </div>

    </div>

    <div class="candidate-score-ui">

        Score:
        ${candidate.score}

    </div>

    <div class="candidate-actions">

        <button
            class="delete-btn"
            onclick="deleteCandidate(${candidate.id})"
        >
            Delete Candidate
        </button>

    </div>

    <div class="candidate-section-ui">

        <h3>
            Allotted Scientist
        </h3>

<p>
    ${candidate.allotted_scientist || "Not Allocated"}
</p>

<p>
    ${candidate.allotted_division || ""}
</p>

<p>
    ${candidate.allocation_reason || ""}
</p>
    </div>

    <div class="candidate-section-ui">

        <h3>
            Skills
        </h3>

        <div class="skills-wrapper">
            ${skills}
        </div>

    </div>

    <div class="candidate-section-ui">

        <h3>
            Evaluation Reasons
        </h3>

        <ul>
            ${reasons}
        </ul>

    </div>

`;

grid.appendChild(card);

});
}

function renderTableView(
    data,
    container
) {

    let tableHTML = `

        <div class="table-wrapper">

            <table>

                <thead>

                    <tr>

                        <th>Name</th>

                        <th>GPA</th>

                        <th>Score</th>

                        <th>Status</th>

                        <th>Scientist</th>

                        <th>Skills</th>

                        <th>Reasons</th>

                        <th>Actions</th>

                    </tr>

                </thead>

                <tbody>
    `;

    data.forEach((candidate, index) => {

        const highlighted =
            index < topK;

        tableHTML += `

            <tr class="
                ${highlighted
                    ? "top-highlight-row"
                    : ""}
            ">

                <td>
                    ${candidate.name || "Unknown"}
                </td>

                <td>
                    ${candidate.gpa || "N/A"}
                </td>

                <td>
                    ${candidate.score}
                </td>

                <td>

                    <span class="
                        ${candidate.selected
                            ? "selected-pill"
                            : "rejected-pill"}
                    ">

                        ${candidate.selected
                            ? "SELECTED"
                            : "REJECTED"}

                    </span>

                </td>

                <td>
                   ${candidate.allotted_scientist || "N/A"}
                </td>

                <td>
                    ${candidate.skills || ""}
                </td>

                <td>
                    ${candidate.reasons || ""}
                </td>

                <td>

                    <button
                        class="delete-btn"
                        onclick="deleteCandidate(${candidate.id})"
                    >
                        Delete
                    </button>

                </td>

            </tr>
        `;
    });

    tableHTML += `

                </tbody>

            </table>

        </div>
    `;

    container.innerHTML =
        tableHTML;
}
function exportSelectedColumns() {

    const checkedColumns =

        Array.from(
            document.querySelectorAll(
                "#exportDropdown input:checked"
            )
        )

        .map(input => input.value);

    if (
        checkedColumns.length === 0
    ) {

        alert(
            "Please select at least one column"
        );

        return;
    }

    let csv = "";

    csv += checkedColumns.join(",");

    csv += "\n";

    candidates.forEach(candidate => {

        const row =
            checkedColumns.map(column => {

                return (
                    candidate[column] ?? ""
                );
            });

        csv +=
            row.join(",") + "\n";
    });

    const blob =
        new Blob(
            [csv],
            {
                type:"text/csv"
            }
        );

    const link =
        document.createElement("a");

    link.href =
        URL.createObjectURL(blob);

    link.download =
        "candidate-results.csv";

    link.click();
}
loadCandidates();