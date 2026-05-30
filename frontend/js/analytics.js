let analyticsCandidates = [];

let analyticsChart = null;

async function loadAnalytics() {

    try {

        const response =
            await fetch("/candidates");

        analyticsCandidates =
            await response.json();

        console.log(
            "Candidates:",
            analyticsCandidates
        );

        updateStatistics();

        setTimeout(() => {

            renderAnalyticsChart();

        }, 100);

        attachAnalyticsEvents();

    } catch (error) {

        console.error(
            "Analytics Error:",
            error
        );
    }
}

function updateStatistics() {

    const total =
        analyticsCandidates.length;

    const selected =
        analyticsCandidates.filter(
            c => c.selected
        ).length;

    const rejected =
        total - selected;

    const averageScore =
        total > 0
        ? (
            analyticsCandidates.reduce(
                (sum, c) =>
                    sum + (c.score || 0),
                0
            ) / total
        ).toFixed(2)
        : "0";

    const averageGpa =
        total > 0
        ? (
            analyticsCandidates.reduce(
                (sum, c) =>
                    sum + (c.gpa || 0),
                0
            ) / total
        ).toFixed(2)
        : "0";

    const researchCount =
        analyticsCandidates.filter(
            c =>
                c.reasons &&
                c.reasons
                .toLowerCase()
                .includes("research")
        ).length;

    document.getElementById(
        "totalCandidates"
    ).innerText = total;

    document.getElementById(
        "selectedCount"
    ).innerText = selected;

    document.getElementById(
        "rejectedCount"
    ).innerText = rejected;

    document.getElementById(
        "averageScore"
    ).innerText = averageScore;

    document.getElementById(
        "averageGpa"
    ).innerText = averageGpa;

    document.getElementById(
        "researchCount"
    ).innerText = researchCount;

    document.getElementById(
        "summaryText"
    ).innerText =

        `${selected} candidates shortlisted from ${total} applicants. ` +

        `Average evaluation score is ${averageScore}. ` +

        `${researchCount} candidates demonstrated research-oriented profiles.`;
}

function renderAnalyticsChart() {

    const canvas =
        document.getElementById(
            "analyticsChart"
        );

    if (!canvas) {
        return;
    }

    const selector =
        document.getElementById(
            "analyticsType"
        );

    if (!selector) {
        return;
    }

    const type =
        selector.value;

    const ctx =
        canvas.getContext("2d");

    if (analyticsChart) {

        analyticsChart.destroy();
    }

    const chartColors = [
        "#18489c",
        "#2563eb",
        "#60a5fa",
        "#93c5fd",
        "#bfdbfe"
    ];

    if (type === "selection") {

        analyticsChart =
            new Chart(ctx, {

                type: "pie",

                data: {

                    labels: [
                        "Selected",
                        "Rejected"
                    ],

                    datasets: [{

                        data: [

                            analyticsCandidates.filter(
                                c => c.selected
                            ).length,

                            analyticsCandidates.filter(
                                c => !c.selected
                            ).length
                        ],

                        backgroundColor: [
                            "#18489c",
                            "#60a5fa"
                        ],

                        borderWidth: 0
                    }]
                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {
                            position: "bottom"
                        }
                    }
                }
            });
    }

    if (type === "skills") {

        const skillMap = {};

        analyticsCandidates.forEach(c => {

            if (!c.skills) {
                return;
            }

            c.skills
                .split(",")

                .forEach(skill => {

                    const trimmed =
                        skill.trim();

                    if (!skillMap[trimmed]) {

                        skillMap[trimmed] = 0;
                    }

                    skillMap[trimmed]++;
                });
        });

        analyticsChart =
            new Chart(ctx, {

                type: "bar",

                data: {

                    labels:
                        Object.keys(skillMap),

                    datasets: [{

                        label:
                            "Skill Frequency",

                        data:
                            Object.values(skillMap),

                        backgroundColor:
                            chartColors,

                        borderRadius: 8
                    }]
                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {
                            display: false
                        }
                    },

                    scales: {

                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
    }

    if (type === "gpa") {

        analyticsChart =
            new Chart(ctx, {

                type: "bar",

                data: {

                    labels:
                        analyticsCandidates.map(
                            c =>
                                c.name ||
                                "Unknown"
                        ),

                    datasets: [{

                        label: "GPA",

                        data:
                            analyticsCandidates.map(
                                c => c.gpa || 0
                            ),

                        backgroundColor:
                            chartColors,

                        borderRadius: 8
                    }]
                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {
                            display: false
                        }
                    },

                    scales: {

                        y: {
                            beginAtZero: true,
                            max: 10
                        }
                    }
                }
            });
    }

    if (type === "research") {

        const research =
            analyticsCandidates.filter(
                c =>
                    c.reasons &&
                    c.reasons
                    .toLowerCase()
                    .includes("research")
            ).length;

        const nonResearch =
            analyticsCandidates.length
            - research;

        analyticsChart =
            new Chart(ctx, {

                type: "doughnut",

                data: {

                    labels: [
                        "Research",
                        "No Research"
                    ],

                    datasets: [{

                        data: [
                            research,
                            nonResearch
                        ],

                        backgroundColor: [
                            "#18489c",
                            "#93c5fd"
                        ],

                        borderWidth: 0
                    }]
                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {
                            position: "bottom"
                        }
                    }
                }
            });
    }

    if (type === "scores") {

        analyticsChart =
            new Chart(ctx, {

                type: "line",

                data: {

                    labels:
                        analyticsCandidates.map(
                            c =>
                                c.name ||
                                "Unknown"
                        ),

                    datasets: [{

                        label:
                            "Evaluation Score",

                        data:
                            analyticsCandidates.map(
                                c => c.score || 0
                            ),

                        borderColor:
                            "#18489c",

                        backgroundColor:
                            "#93c5fd",

                        tension: 0.4,

                        fill: true
                    }]
                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {
                            display: false
                        }
                    },

                    scales: {

                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
    }
}

function attachAnalyticsEvents() {

    const selector =
        document.getElementById(
            "analyticsType"
        );

    if (!selector) {
        return;
    }

    selector.onchange =
        renderAnalyticsChart;

    const jsonBtn =
        document.getElementById(
            "downloadJson"
        );

    if (jsonBtn) {

        jsonBtn.onclick =
            downloadJSON;
    }

    const csvBtn =
        document.getElementById(
            "downloadCsv"
        );

    if (csvBtn) {

        csvBtn.onclick =
            downloadCSV;
    }

    const pdfBtn =
        document.getElementById(
            "downloadPdf"
        );

    if (pdfBtn) {

        pdfBtn.onclick =
            downloadPDF;
    }
}

function downloadJSON() {

    const blob =
        new Blob(
            [
                JSON.stringify(
                    analyticsCandidates,
                    null,
                    2
                )
            ],
            {
                type:
                    "application/json"
            }
        );

    const link =
        document.createElement("a");

    link.href =
        URL.createObjectURL(blob);

    link.download =
        "candidate-report.json";

    link.click();
}

function downloadCSV() {

    let csv =
        "Name,GPA,Score,Selected\n";

    analyticsCandidates.forEach(c => {

        csv +=

            `${c.name || "Unknown"},${c.gpa || 0},${c.score || 0},${c.selected}\n`;
    });

    const blob =
        new Blob(
            [csv],
            {
                type:
                    "text/csv"
            }
        );

    const link =
        document.createElement("a");

    link.href =
        URL.createObjectURL(blob);

    link.download =
        "candidate-report.csv";

    link.click();
}
async function downloadPDF() {

    try {

        const {
            jsPDF
        } = window.jspdf;

        const pdf =
            new jsPDF(
                "p",
                "mm",
                "a4"
            );

        const chartTypes = [

            {
                value: "selection",
                title:
                    "Selection Distribution"
            },

            {
                value: "skills",
                title:
                    "Top Skills Analysis"
            },

            {
                value: "gpa",
                title:
                    "GPA Distribution"
            },

            {
                value: "research",
                title:
                    "Research Experience"
            },

            {
                value: "scores",
                title:
                    "Evaluation Scores"
            }
        ];

        const selector =
            document.getElementById(
                "analyticsType"
            );

        for (
            let i = 0;
            i < chartTypes.length;
            i++
        ) {

            selector.value =
                chartTypes[i].value;

            renderAnalyticsChart();

            await new Promise(
                resolve =>
                    setTimeout(
                        resolve,
                        800
                    )
            );

            const chartCard =
                document.querySelector(
                    ".chart-card"
                );

            const canvas =
                await html2canvas(
                    chartCard,
                    {
                        scale: 2
                    }
                );

            const imageData =
                canvas.toDataURL(
                    "image/png"
                );

            if (i > 0) {

                pdf.addPage();
            }

            pdf.setFontSize(20);

            pdf.text(
                chartTypes[i].title,
                15,
                20
            );

            const pdfWidth =
                180;

            const pdfHeight =
                (
                    canvas.height
                    * pdfWidth
                ) / canvas.width;

            pdf.addImage(
                imageData,
                "PNG",
                15,
                30,
                pdfWidth,
                pdfHeight
            );
        }

        pdf.save(
            "complete-analytics-report.pdf"
        );

    } catch (error) {

        console.error(error);

        alert(
            "PDF export failed"
        );
    }
}
loadAnalytics();