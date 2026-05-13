const API_BASE = "";

const uploadBtn =
    document.getElementById("uploadBtn");

uploadBtn.addEventListener(
    "click",
    async function () {

        const fileInput =
            document.getElementById("resumeFile");

        const file = fileInput.files[0];

        if (!file) {
            alert("Please select a file");
            return;
        }

        const formData = new FormData();

        formData.append("file", file);

        const status =
            document.getElementById("status");

        const resultBox =
            document.getElementById("uploadResult");

        status.innerHTML = "Uploading...";

        try {

            const response = await fetch(
                `${API_BASE}/upload`,
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            status.innerHTML =
                "Resume processed successfully";

            const skillsText =
                data.skills.join(", ");

            const reasonsHtml =
                data.evaluation.reasons
                .map(reason =>
                    `<li>${reason}</li>`
                )
                .join("");

            resultBox.innerHTML = `

                <div class="result-box">

                    <h3>
                        ${data.filename}
                    </h3>

                    <p>
                        <strong>Score:</strong>
                        ${data.evaluation.score}
                    </p>

                    <p>
                        <strong>Status:</strong>
                        ${data.evaluation.selected ? "SELECTED" : "REJECTED"}
                    </p>

                    <p>
                        <strong>GPA:</strong>
                        ${data.marks.gpa}
                    </p>

                    <p>
                        <strong>Skills:</strong>
                        ${skillsText}
                    </p>

                    <strong>
                        Evaluation Reasons
                    </strong>

                    <ul>
                        ${reasonsHtml}
                    </ul>

                </div>
            `;

        } catch (error) {

            console.error(error);

            status.innerHTML =
                "Upload failed";
        }
    }
);