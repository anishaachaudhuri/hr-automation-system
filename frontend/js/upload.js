const API_BASE = "";

const uploadBtn =
    document.getElementById(
        "uploadBtn"
    );

uploadBtn.addEventListener(
    "click",
    async function () {

        const fileInput =
            document.getElementById(
                "resumeFile"
            );

        const file =
            fileInput.files[0];

        if (!file) {

            alert(
                "Please select a resume"
            );

            return;
        }

        const formData =
            new FormData();

        formData.append(
            "file",
            file
        );

        const status =
            document.getElementById(
                "status"
            );

        const resultBox =
            document.getElementById(
                "uploadResult"
            );

        status.innerHTML =
            "Processing resume...";

        try {

            let endpoint =
                `${API_BASE}/upload`;

            // ZIP upload
            if (
                file.name.endsWith(".zip")
            ) {

                endpoint =
                    `${API_BASE}/upload-zip`;
            }

            const response =
                await fetch(
                    endpoint,
                    {
                        method: "POST",
                        body: formData
                    }
                );

            if (!response.ok) {

                const errorText =
                    await response.text();

                console.error(errorText);

                throw new Error(
                    "Upload failed"
                );
            }

            const data =
                await response.json();

            // ZIP RESPONSE
            if (
                file.name.endsWith(".zip")
            ) {

                status.innerHTML =
                    "Bulk upload completed";

                resultBox.innerHTML = `

                    <div class="candidate-card">

                        <h2>
                            Bulk Upload Successful
                        </h2>

                        <p>
                            Total Resumes Processed:
                            ${data.total_processed}
                        </p>

                    </div>
                `;

                return;
            }

            // SINGLE PDF RESPONSE

            status.innerHTML =
                "Resume processed successfully";

            const skillsHtml =
                data.skills
                .map(skill =>

                    `<span class="skill-chip">
                        ${skill}
                    </span>`

                ).join("");

            const reasonsHtml =
                data.evaluation.reasons
                .map(reason =>

                    `<li>${reason}</li>`

                ).join("");

            const semanticScore =
                Math.round(
                    (
                        data.semantic_matching
                        ?.average_similarity || 0
                    ) * 100
                );

            const researchDetected =
                data.evaluation.reasons
                .some(reason =>

                    reason
                    .toLowerCase()
                    .includes("research")

                );

            resultBox.innerHTML = `

                <div class="candidate-card">

                    <div class="candidate-top">

                        <div>

                            <h2>
                                ${data.name || "Unknown Candidate"}
                            </h2>

                            <p class="candidate-role">
                                AI/ML Candidate Evaluation
                            </p>

                        </div>

                        <div class="
                            status-badge
                            ${data.evaluation.selected
                                ? "selected-badge"
                                : "rejected-badge"}
                        ">

                            ${data.evaluation.selected
                                ? "SELECTED"
                                : "REJECTED"}

                        </div>

                    </div>

                    <div class="score-section">

                        <div class="score-card">

                            <span>
                                Final Score
                            </span>

                            <strong>
                                ${data.evaluation.score}
                            </strong>

                        </div>

                        <div class="score-card">

                            <span>
                                GPA
                            </span>

                            <strong>
                                ${data.marks.gpa || "N/A"}
                            </strong>

                        </div>

                        <div class="score-card">

                            <span>
                                Semantic Match
                            </span>

                            <strong>
                                ${semanticScore}%
                            </strong>

                        </div>

                    </div>

                    <div class="skills-section">

                        <h3>
                            Top Skills
                        </h3>

                        <div class="skills-wrapper">
                            ${skillsHtml}
                        </div>

                    </div>

                    <div class="research-box">

                        <h3>
                            Research Experience
                        </h3>

                        <p>
                            ${researchDetected
                                ? "Research background detected"
                                : "No major research indicators"}
                        </p>

                    </div>

                    <div class="explanation-box">

                        <h3>
                            Key Evaluation Reasons
                        </h3>

                        <ul>
                            ${reasonsHtml}
                        </ul>

                    </div>

                </div>
            `;

        } catch (error) {

            console.error(error);

            status.innerHTML =
                "Upload failed";
        }
    }
);