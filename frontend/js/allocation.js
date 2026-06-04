window.allocationScientists =
    window.allocationScientists || [];

window.allocationCandidates =
    window.allocationCandidates || [];

async function loadScientists() {

    try {

        const scientistsResponse =
            await fetch("/scientists");

        allocationScientists =
            await scientistsResponse.json();

        const candidatesResponse =
            await fetch("/candidates");

        allocationCandidates =
            await candidatesResponse.json();

        renderAllocation();

    } catch (error) {

        console.error(
            "Failed to load allocation data:",
            error
        );
    }
}

function renderAllocation() {

    const container =
        document.getElementById(
            "allocationContainer"
        );

    if (!container) {
        return;
    }

    const searchInput =
        document.getElementById(
            "searchScientist"
        );

    const searchValue =
        searchInput
            ? searchInput.value.toLowerCase()
            : "";

    const filteredScientists =

        allocationScientists.filter(
            scientist =>

                scientist.name
                    .toLowerCase()
                    .includes(searchValue)
        );

    container.innerHTML = "";

    filteredScientists.forEach(scientist => {

        const assignedCandidates =

            allocationCandidates.filter(
                candidate =>

                    (candidate.allotted_scientist || "")
                    === scientist.name
            );

        const assignedList =

            assignedCandidates.length > 0

            ? assignedCandidates.map(
                candidate =>

                    `<li>${candidate.name}</li>`
              ).join("")

            : `<li class="empty-state">
                    No interns allocated
               </li>`;

        container.innerHTML += `

            <div class="allocation-card">

                <h3>
                    ${scientist.name}
                </h3>

                <div class="specialization-badge">

                    ${scientist.specialization}

                </div>

                <div class="assigned-count">

                    Division:
                    ${scientist.division}

                </div>

                <div class="assigned-count">

                    Allocated:
                    ${assignedCandidates.length}
                    /
                    ${scientist.maxInterns || 10}

                </div>

                <h4>
                    Allocated Interns
                </h4>

                <ul class="intern-list">

                    ${assignedList}

                </ul>

            </div>
        `;
    });
}

function openScientistModal() {

    const modal =
        document.getElementById(
            "scientistModal"
        );

    if (modal) {

        modal.style.display =
            "flex";
    }
}

function closeModals() {

    document
        .querySelectorAll(".modal")
        .forEach(modal => {

            modal.style.display =
                "none";
        });
}

async function addScientist() {

    const name =
        document.getElementById(
            "scientistName"
        ).value.trim();

    const specialization =
        document.getElementById(
            "scientistSpecialization"
        ).value.trim();

    const division =
        document.getElementById(
            "scientistDivision"
        ).value.trim();

    if (
        !name ||
        !specialization ||
        !division
    ) {

        alert(
            "Please fill all fields"
        );

        return;
    }

    const confirmed = confirm(

        "Are you sure you want to create this scientist?\n\nThe scientist will immediately become available for future intern allocation."

    );

    if (!confirmed) {
        return;
    }

    try {

        const response =
            await fetch(
                "/scientists",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        name,
                        specialization,
                        division,
                        maxInterns: 10
                    })
                }
            );

        const data =
            await response.json();

        alert(
            data.message ||
            "Scientist created successfully"
        );

        closeModals();

        document.getElementById(
            "scientistName"
        ).value = "";

        document.getElementById(
            "scientistSpecialization"
        ).value = "";

        document.getElementById(
            "scientistDivision"
        ).value = "";

        await loadScientists();

    } catch (error) {

        console.error(error);

        alert(
            "Failed to create scientist"
        );
    }
}

function attachAllocationEvents() {

    const searchInput =
        document.getElementById(
            "searchScientist"
        );

    if (searchInput) {

        searchInput.oninput =
            renderAllocation;
    }
}

async function initializeAllocation() {

    attachAllocationEvents();

    await loadScientists();
}

initializeAllocation();