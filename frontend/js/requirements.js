async function loadRequirementsPage() {

    const authResponse =
        await fetch("/auth-status");

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
        document.getElementById("content");

    const response = await fetch(
        "/static/pages/requirements-login.html"
    );

    const html = await response.text();

    content.innerHTML = html;

    loadDynamicCSS(
        "/static/css/requirements-login.css"
    );

    attachLoginHandler();
}

function attachLoginHandler() {

    document
        .getElementById("loginBtn")
        .addEventListener(
            "click",
            async function () {

                const formData =
                    new FormData();

                formData.append(
                    "username",
                    document.getElementById(
                        "username"
                    ).value
                );

                formData.append(
                    "password",
                    document.getElementById(
                        "password"
                    ).value
                );

                const response =
                    await fetch(
                        "/login",
                        {
                            method: "POST",
                            body: formData
                        }
                    );

                if (!response.ok) {

                    document.getElementById(
                        "loginError"
                    ).innerHTML =
                        "Invalid credentials";

                    return;
                }

                loadRequirementsDashboard();
            }
        );
}

async function loadRequirementsDashboard() {

    const content =
        document.getElementById("content");

    const response = await fetch(
        "/static/pages/requirements-dashboard.html"
    );

    const html = await response.text();

    content.innerHTML = html;

    loadDynamicCSS(
        "/static/css/requirements-dashboard.css"
    );

    loadRequirementData();

    attachSaveHandler();

    attachLogoutHandler();
}

async function loadRequirementData() {

    const response =
        await fetch("/requirements");

    const data =
        await response.json();

    document.getElementById(
        "minimumGpa"
    ).value = data.minimum_gpa;

    document.getElementById(
        "requiredSkills"
    ).value = data.required_skills;

    document.getElementById(
        "preferredSkills"
    ).value = data.preferred_skills;

    document.getElementById(
        "disallowedBranches"
    ).value = data.disallowed_branches;

    document.getElementById(
        "skillWeight"
    ).value = data.skill_weight;

    document.getElementById(
        "gpaWeight"
    ).value = data.gpa_weight;

    document.getElementById(
        "researchWeight"
    ).value = data.research_weight;

    document.getElementById(
        "achievementWeight"
    ).value = data.achievement_weight;
}

function attachSaveHandler() {

    document
        .getElementById("saveBtn")
        .addEventListener(
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

                await fetch(
                    "/requirements",
                    {
                        method: "PUT",
                        headers: {
                            "Content-Type":
                                "application/json"
                        },
                        body: JSON.stringify(payload)
                    }
                );

                const toast =
                    document.getElementById(
                        "saveToast"
                    );

                toast.classList.add("show");

                setTimeout(() => {

                    toast.classList.remove(
                        "show"
                    );

                }, 2000);
            }
        );
}

function attachLogoutHandler() {

    document
        .getElementById("logoutBtn")
        .addEventListener(
            "click",
            async function () {

                await fetch(
                    "/logout",
                    {
                        method: "POST"
                    }
                );

                loadLoginPage();
            }
        );
}

function loadDynamicCSS(href) {

    const oldStyles =
        document.querySelectorAll(
            ".dynamic-style"
        );

    oldStyles.forEach(style =>
        style.remove()
    );

    const style =
        document.createElement("link");

    style.rel = "stylesheet";

    style.href = href;

    style.className = "dynamic-style";

    document.head.appendChild(style);
}

loadRequirementsPage();