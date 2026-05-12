window.onload = function () {

    const uploadBtn =
        document.getElementById("uploadBtn");

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
                    "Please select a file"
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

            const result =
                document.getElementById(
                    "result"
                );

            status.innerHTML =
                "Uploading...";

            try {

                const response =
                    await fetch(
                        "http://127.0.0.1:8000/upload",
                        {
                            method: "POST",
                            body: formData
                        }
                    );

                const data =
                    await response.json();

                console.log(data);

                status.innerHTML =
                    "Resume processed successfully";

                let skillsText = "";

                if (data.skills) {

                    skillsText =
                        data.skills.join(", ");
                }

                let reasonsHtml = "";

                if (
                    data.evaluation &&
                    data.evaluation.reasons
                ) {

                    reasonsHtml =
                        data.evaluation.reasons
                        .map(
                            reason =>
                                `<li>${reason}</li>`
                        )
                        .join("");
                }

                result.innerHTML = `

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
                            ${
                                data.evaluation.selected
                                ? "SELECTED"
                                : "REJECTED"
                            }
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
};