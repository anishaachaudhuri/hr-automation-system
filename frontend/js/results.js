const RESULTS_API = "";

let candidates = [];
let sortedDescending = true;

async function fetchCandidates() {

    try {

        const response = await fetch(
            `${RESULTS_API}/candidates`
        );

        candidates = await response.json();

        renderTable(candidates);

    } catch (error) {

        console.error(error);
    }
}

function renderTable(data) {

    const tableBody =
        document.getElementById(
            "candidateTableBody"
        );

    tableBody.innerHTML = "";

    const topK = parseInt(
        document.getElementById(
            "topKInput"
        ).value
    ) || 0;

    const sortedData = [...data].sort(
        (a, b) => b.score - a.score
    );

    data.forEach(candidate => {

        const row =
            document.createElement("tr");

        const candidateIndex =
            sortedData.findIndex(
                item => item.id === candidate.id
            );

        if (candidateIndex < topK) {
            row.classList.add(
                "top-k-highlight"
            );
        }

        row.innerHTML = `

            <td>${candidate.filename}</td>
            <td>${candidate.gpa ?? "N/A"}</td>
            <td>${candidate.score}</td>

            <td>
                <span class="${candidate.selected ? "selected-status" : "rejected-status"}">
                    ${candidate.selected ? "SELECTED" : "REJECTED"}
                </span>
            </td>

            <td>${candidate.skills}</td>
        `;

        tableBody.appendChild(row);
    });
}

function searchCandidates() {

    const query =
        document.getElementById(
            "searchInput"
        ).value.toLowerCase();

    const selectedOnly =
        document.getElementById(
            "selectedOnly"
        ).checked;

    const filtered = candidates.filter(candidate => {

        const filenameMatch =
            candidate.filename
            .toLowerCase()
            .includes(query);

        const skillsMatch =
            (candidate.skills || "")
            .toLowerCase()
            .includes(query);

        const selectionMatch =
            selectedOnly
            ? candidate.selected
            : true;

        return (
            (filenameMatch || skillsMatch)
            && selectionMatch
        );
    });

    renderTable(filtered);
}

function sortByScore() {

    sortedDescending = !sortedDescending;

    candidates.sort((a, b) => {

        return sortedDescending
            ? b.score - a.score
            : a.score - b.score;
    });

    renderTable(candidates);
}

fetchCandidates();

document
    .getElementById("searchInput")
    .addEventListener(
        "input",
        searchCandidates
    );

document
    .getElementById("selectedOnly")
    .addEventListener(
        "change",
        searchCandidates
    );

document
    .getElementById("sortBtn")
    .addEventListener(
        "click",
        sortByScore
    );

document
    .getElementById("topKInput")
    .addEventListener(
        "input",
        () => renderTable(candidates)
    );