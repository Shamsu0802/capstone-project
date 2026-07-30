// -------------------------------
// Selected Symptoms
// -------------------------------

let selectedSymptoms = [];

// -------------------------------
// Search Symptoms
// -------------------------------

function searchSymptoms() {

    let searchText = document
        .getElementById("search")
        .value
        .toLowerCase();

    let suggestionBox = document.getElementById("symptomList");

    suggestionBox.innerHTML = "";

    if (searchText === "") {
        return;
    }

    symptoms.forEach(symptom => {

        if (
            symptom.toLowerCase().includes(searchText) &&
            !selectedSymptoms.includes(symptom)
        ) {

            let div = document.createElement("div");

            div.className = "symptom";

            div.innerHTML = symptom;

            div.onclick = function () {
                addSymptom(symptom);
            };

            suggestionBox.appendChild(div);
        }

    });

}

// -------------------------------
// Add Symptom
// -------------------------------

function addSymptom(symptom) {

    selectedSymptoms.push(symptom);

    document.getElementById("search").value = "";

    document.getElementById("symptomList").innerHTML = "";

    displaySelectedSymptoms();

}

// -------------------------------
// Display Selected Symptoms
// -------------------------------

function displaySelectedSymptoms() {

    let selectedBox =
        document.getElementById("selectedSymptoms");

    selectedBox.innerHTML = "";

    selectedSymptoms.forEach(symptom => {

        let div = document.createElement("div");

        div.className = "selected";

        div.innerHTML = `
            ${symptom}
            <button onclick="removeSymptom('${symptom}')">
                ✖
            </button>
        `;

        selectedBox.appendChild(div);

    });

}

// -------------------------------
// Remove Symptom
// -------------------------------

function removeSymptom(symptom) {

    selectedSymptoms =
        selectedSymptoms.filter(item => item !== symptom);

    displaySelectedSymptoms();

}

// -------------------------------
// Predict
// -------------------------------

async function predict() {

    let data = {};

    // --------------------------
    // Required Fields
    // --------------------------

    data.age =
        Number(document.getElementById("age").value);

    data.gender =
        Number(document.getElementById("gender").value);

    // --------------------------
    // Symptoms
    // --------------------------

    selectedSymptoms.forEach(symptom => {

        let key = symptom
            .toLowerCase()
            .replaceAll(" ", "_");

        data[key] = 1;

    });

    // --------------------------
    // Medical History
    // --------------------------

    [
        "diabetes",
        "hypertension",
        "asthma",
        "copd",
        "heart_disease",
        "kidney_disease",
        "stroke_history",
        "pregnancy"
    ].forEach(item => {

        if (document.getElementById(item).checked) {
            data[item] = 1;
        }

    });

    // --------------------------
    // Optional Vitals
    // --------------------------

    const optionalFields = [
        "heart_rate",
        "systolic_bp",
        "oxygen_level",
        "temperature",
        "respiratory_rate",
        "symptom_duration_hours"
    ];

    optionalFields.forEach(field => {

        const value =
            document.getElementById(field).value;

        if (value !== "") {

            data[field] = Number(value);

        }

    });

    console.log("Sending JSON:");

    console.log(data);

    // --------------------------
    // API Call
    // --------------------------

    try {

        let response = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        let result = await response.json();

        document.getElementById("result").innerHTML = `
            <h2>Urgency</h2>
            <h1>${result.urgency}</h1>
        `;

    }

    catch (error) {

        console.error(error);

        document.getElementById("result").innerHTML =
            "<h2>Unable to connect to API.</h2>";

    }

}