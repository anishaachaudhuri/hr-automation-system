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
                `/static/pages/${page}.html?v=${Date.now()}`
            );

        const html =
            await response.text();

        contentArea.innerHTML =
            html;

        removeOldScripts();

        await loadPageScript(page);

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

    return new Promise((resolve) => {

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

            resolve();
            return;
        }

        const script =
            document.createElement(
                "script"
            );

        script.className =
            "dynamic-script";

        script.src =
            scriptPath;

        script.onload = () => {

            resolve();
        };

        script.onerror = () => {

            console.error(
                "Failed to load script:",
                scriptPath
            );

            resolve();
        };

        document.body.appendChild(
            script
        );
    });
}

window.onload = async function () {

    await loadPage(
        "analytics"
    );
};