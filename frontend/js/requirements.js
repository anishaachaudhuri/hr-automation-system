async function loadRequirementsPage() {

    const authResponse =
        await fetch(
            "/auth-status",
            {
                credentials: "include"
            }
        );

    const authData =
        await authResponse.json();

    if (authData.authenticated) {

        loadRequirementsDashboard();

    } else {

        loadLoginPage();
    }
}

async function loadLoginPage() {

    const content =
        document.getElementById(
            "content-area"
        );

    if (!content) {
        return;
    }

    const response =
        await fetch(
            "/static/pages/requirements-login.html"
        );

    const html =
        await response.text();

    content.innerHTML = html;

    attachLoginHandler();
}

function attachLoginHandler() {

    const loginBtn =
        document.getElementById(
            "loginBtn"
        );

    if (!loginBtn) {
        return;
    }

    loginBtn.addEventListener(
        "click",
        async function () {

            const username =
                document.getElementById(
                    "username"
                ).value;

            const password =
                document.getElementById(
                    "password"
                ).value;

            const formData =
                new FormData();

            formData.append(
                "username",
                username
            );

            formData.append(
                "password",
                password
            );

            const response =
                await fetch(
                    "/login",
                    {
                        method: "POST",
                        body: formData,
                        credentials: "include"
                    }
                );

            if (!response.ok) {

                const error =
                    document.getElementById(
                        "loginError"
                    );

                if (error) {

                    error.innerText =
                        "Invalid username or password";
                }

                return;
            }

            loadRequirementsDashboard();
        }
    );
}

async function loadRequirementsDashboard() {

    const content =
        document.getElementById(
            "content-area"
        );

    if (!content) {
        return;
    }

    const response =
        await fetch(
            "/static/pages/requirements-dashboard.html"
        );

    const html =
        await response.text();

    content.innerHTML = html;

    loadRequirementData();

    attachSaveHandler();

    attachLogoutHandler();
}

async function loadRequirementData() {

    const response =
        await fetch(
            "/requirements",
            {
                credentials: "include"
            }
        );

    if (!response.ok) {
        return;
    }

    const data =
        await response.json();

    document.getElementById(
        "minimumGpa"
    ).value =
        data.minimum_gpa || "";

    document.getElementById(
        "requiredSkills"
    ).value =
        data.required_skills || "";

    document.getElementById(
        "preferredSkills"
    ).value =
        data.preferred_skills || "";

    document.getElementById(
        "disallowedBranches"
    ).value =
        data.disallowed_branches || "";

    document.getElementById(
        "skillWeight"
    ).value =
        data.skill_weight || "";

    document.getElementById(
        "gpaWeight"
    ).value =
        data.gpa_weight || "";

    document.getElementById(
        "researchWeight"
    ).value =
        data.research_weight || "";

    document.getElementById(
        "achievementWeight"
    ).value =
        data.achievement_weight || "";
}

function attachSaveHandler() {

    const saveBtn =
        document.getElementById(
            "saveBtn"
        );

    if (!saveBtn) {
        return;
    }

    saveBtn.addEventListener(
        "click",
        async function () {

            const payload = {

                minimum_gpa:
                    parseFloat(
                        document.getElementById(
                            "minimumGpa"
                        ).value
                    ),

                required_skills:
                    document.getElementById(
                        "requiredSkills"
                    ).value,

                preferred_skills:
                    document.getElementById(
                        "preferredSkills"
                    ).value,

                disallowed_branches:
                    document.getElementById(
                        "disallowedBranches"
                    ).value,

                skill_weight:
                    parseFloat(
                        document.getElementById(
                            "skillWeight"
                        ).value
                    ),

                gpa_weight:
                    parseFloat(
                        document.getElementById(
                            "gpaWeight"
                        ).value
                    ),

                research_weight:
                    parseFloat(
                        document.getElementById(
                            "researchWeight"
                        ).value
                    ),

                achievement_weight:
                    parseFloat(
                        document.getElementById(
                            "achievementWeight"
                        ).value
                    )
            };

            const response =
                await fetch(
                    "/requirements",
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        credentials: "include",

                        body:
                            JSON.stringify(
                                payload
                            )
                    }
                );

            if (!response.ok) {
                alert(
                    "Failed to save configuration"
                );
                return;
            }

            const toast =
                document.getElementById(
                    "saveToast"
                );

            if (toast) {

                toast.style.opacity = "1";

                setTimeout(() => {

                    toast.style.opacity = "0";

                }, 2000);
            }
        }
    );
}

function attachLogoutHandler() {

    const logoutBtn =
        document.getElementById(
            "logoutBtn"
        );

    if (!logoutBtn) {
        return;
    }

    logoutBtn.addEventListener(
        "click",
        async function () {

            await fetch(
                "/logout",
                {
                    method: "POST",
                    credentials: "include"
                }
            );

            loadLoginPage();
        }
    );
}

loadRequirementsPage();