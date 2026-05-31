async function loadPage(page) {

    const contentArea =
        document.getElementById(
            "content-area"
        );

    if (!contentArea) {
        return;
    }

    try {

        const response =
            await fetch(
                `/static/pages/${page}.html`
            );

        const html =
            await response.text();

        contentArea.innerHTML =
            html;

        removeOldScripts();

        loadPageScript(page);

    } catch (error) {

        console.error(
            "Page Load Error:",
            error
        );
    }
}

function removeOldScripts() {

    const oldScripts =
        document.querySelectorAll(
            ".dynamic-script"
        );

    oldScripts.forEach(script => {

        script.remove();
    });
}

function loadPageScript(page) {

    let scriptPath = "";

    if (page === "analytics") {

        scriptPath =
            "/static/js/analytics.js";
    }

    else if (page === "upload") {

        scriptPath =
            "/static/js/upload.js";
    }

    else if (page === "results") {

        scriptPath =
            "/static/js/results.js";
    }

    else if (
        page === "requirements-login"
    ) {

        scriptPath =
            "/static/js/requirements.js";
    }

    else if (
        page === "requirements-dashboard"
    ) {

        scriptPath =
            "/static/js/requirements.js";
    }

    else if (page === "allocation") {

        scriptPath =
            "/static/js/allocation.js";
    }

    else if (page === "audit") {

        scriptPath =
            "/static/js/audit.js";
    }

    if (scriptPath === "") {
        return;
    }

    const script =
        document.createElement(
            "script"
        );

    script.className =
        "dynamic-script";

    script.src =
        scriptPath +
        "?v=" +
        Date.now();

    document.body.appendChild(
        script
    );
}

window.onload = function () {

    loadPage("analytics");
};