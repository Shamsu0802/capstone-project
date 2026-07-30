async function analyzePatient() {

    const patientText = document
        .getElementById("patient_text")
        .value;

    if (patientText.trim() === "") {

        alert("Please enter patient symptoms.");

        return;
    }

    document.getElementById("urgency").innerHTML = "Analyzing...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/intake",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    patient_text: patientText
                })

            }
        );

        const result = await response.json();

        // -------------------------
        // Urgency
        // -------------------------

        document.getElementById("urgency").innerHTML =
            `<h2>${result.urgency}</h2>`;

        // -------------------------
        // Features
        // -------------------------

        document.getElementById("features").innerHTML =
            JSON.stringify(result.features, null, 4);

        // -------------------------
        // Recommendation
        // -------------------------

        document.getElementById("recommendation").innerHTML =
            result.recommendation;

        // -------------------------
        // Guideline
        // -------------------------

        document.getElementById("guideline").innerHTML =
            result.retrieved_guideline;

        // -------------------------
        // Source
        // -------------------------

        document.getElementById("source").innerHTML =
            result.source;

    }

    catch (error) {

        console.error(error);

        document.getElementById("urgency").innerHTML =
            "Unable to connect to API.";

    }

}