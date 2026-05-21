let candidates = [];

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

        topKInput.oninput =
            function () {

                topK =
                    parseInt(this.value) || 3;

                renderCandidates();
            };
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

function allocateScientists() {

    scientists.forEach(scientist => {

        scientist.assigned = [];
    });

    const selectedCandidates =
        candidates.filter(c => c.selected);

    selectedCandidates.forEach(candidate => {

        const candidateSkills =
            candidate.skills
                .toLowerCase();

        for (let scientist of scientists) {

            const hasMatchingSkill =
                candidateSkills.includes(
                    scientist.specialization
                );

            const hasCapacity =
                scientist.assigned.length
                < scientist.maxInterns;

            if (
                hasMatchingSkill &&
                hasCapacity
            ) {

                scientist.assigned.push(
                    candidate.name
                );

candidate.allottedScientist =
    scientist.name;

candidate.allottedDivision =
    scientist.division;

candidate.allocationReason =
    `Matched with ${scientist.specialization}`;

                break;
            }
        }
    });
}

function renderCandidates() {

    const container =
        document.getElementById(
            "candidateContainer"
        );

    if (!container) {
        return;
    }
    allocateScientists();
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

    <div class="candidate-section-ui">

        <h3>
            Allotted Scientist
        </h3>

<p>
    ${candidate.allottedScientist || "Not Allocated"}
</p>

<p>
    ${candidate.allottedDivision || ""}
</p>

<p>
    ${candidate.allocationReason || ""}
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
                   ${candidate.allottedScientist || "N/A"}
                </td>

                <td>
                    ${candidate.skills || ""}
                </td>

                <td>
                    ${candidate.reasons || ""}
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

loadCandidates();