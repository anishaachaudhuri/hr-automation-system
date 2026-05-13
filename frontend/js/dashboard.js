async function loadPage(pageName) {

    const content =
        document.getElementById("content");

    const response = await fetch(
        `/static/pages/${pageName}.html`
    );

    const html = await response.text();

    content.innerHTML = html;

    const oldStyles =
        document.querySelectorAll(
            ".dynamic-style"
        );

    oldStyles.forEach(style => style.remove());

    const style =
        document.createElement("link");

    style.rel = "stylesheet";

    style.href = `/static/css/${pageName}.css`;

    style.className = "dynamic-style";

    document.head.appendChild(style);

    const oldScript =
        document.getElementById("dynamic-script");

    if (oldScript) {
        oldScript.remove();
    }

    const script =
        document.createElement("script");

    script.src = `/static/js/${pageName}.js`;

    script.id = "dynamic-script";

    document.body.appendChild(script);
}

window.onload = function () {
    loadPage("upload");
};