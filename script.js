async function analyzeResume() {

    const resume =
        document.getElementById("resume").files[0];

    const jobRole =
        document.getElementById("jobRole").value;

    const status =
        document.getElementById("status");

    if (!resume) {
        status.innerText = "Please upload your resume.";
        return;
    }

    if (!jobRole) {
        status.innerText = "Please enter a job role.";
        return;
    }

    status.innerText =
        "Analyzing your resume... ✨";


    const formData = new FormData();

    formData.append("resume", resume);
    formData.append("job_role", jobRole);


    try {

        const API_URL =
            window.location.hostname === "127.0.0.1" ||
            window.location.hostname === "localhost"
                ? "http://127.0.0.1:8000"
                : "";

        const response = await fetch(`${API_URL}/api/analyze`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();


        if (data.error) {

            status.innerText = data.error;
            return;

        }


        displayResults(data);

        status.innerText =
            "Analysis complete! ✨";

    }

    catch (error) {
        console.error("ERROR:", error);
        status.innerText = "Error: " + error.message;
    }
}


function displayResults(data) {

    document
        .getElementById("results")
        .classList.remove("hidden");


    document
        .getElementById("score")
        .innerText = data.ats_score;


    document
        .getElementById("summary")
        .innerText = data.summary;


    displaySkills(
        "matchedSkills",
        data.matched_skills
    );


    displaySkills(
        "missingSkills",
        data.missing_skills
    );


    displayList(
        "strengths",
        data.strengths
    );


    displayList(
        "weaknesses",
        data.weaknesses
    );


    displayList(
        "suggestions",
        data.suggestions
    );

}


function displaySkills(id, skills) {

    const container =
        document.getElementById(id);

    container.innerHTML = "";

    skills.forEach(skill => {

        const span =
            document.createElement("span");

        span.className = "skill";

        span.innerText = skill;

        container.appendChild(span);

    });

}


function displayList(id, items) {

    const list =
        document.getElementById(id);

    list.innerHTML = "";

    items.forEach(item => {

        const li =
            document.createElement("li");

        li.innerText = item;

        list.appendChild(li);

    });

}