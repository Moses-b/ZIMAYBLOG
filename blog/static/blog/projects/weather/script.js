const apiKey = "53bd3136dee4207908caabc4fe3f44a9";

const btn = document.getElementById("searchBtn");
const input = document.getElementById("cityInput");
const infoBox = document.getElementById("infoBox");
const errorMsg = document.getElementById("error");

function weatherEmoji(main) {
    const value = (main || "").toLowerCase();
    if (value.includes("clear")) return "☀";
    if (value.includes("cloud")) return "☁";
    if (value.includes("rain") || value.includes("drizzle")) return "🌧";
    if (value.includes("thunder")) return "⛈";
    if (value.includes("snow")) return "❄";
    return "🌤";
}

async function checkWeather(city) {
    if (!city) return;

    if (!apiKey || apiKey === "VOTRE_CLE_API") {
        errorMsg.textContent = "Ajoutez votre cle API OpenWeather dans le fichier script.js.";
        errorMsg.style.display = "block";
        infoBox.classList.remove("active");
        return;
    }

    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&units=metric&lang=fr&appid=${apiKey}`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Ville non trouvee");
        }

        const data = await response.json();
        document.getElementById("cityName").textContent = `${data.name}, ${data.sys.country}`;
        document.getElementById("tempValue").textContent = Math.round(data.main.temp);
        document.getElementById("humidity").textContent = data.main.humidity;
        document.getElementById("wind").textContent = data.wind.speed;
        document.getElementById("weatherDesc").textContent = data.weather[0].description;
        document.getElementById("iconContainer").textContent = weatherEmoji(data.weather[0].main);

        const options = { weekday: "long", day: "numeric", month: "long" };
        document.getElementById("dateText").textContent = new Date().toLocaleDateString("fr-FR", options);

        errorMsg.style.display = "none";
        infoBox.classList.add("active");
    } catch (err) {
        errorMsg.textContent = "Ville non trouvee ou erreur reseau.";
        errorMsg.style.display = "block";
        infoBox.classList.remove("active");
    }
}

btn?.addEventListener("click", () => {
    checkWeather(input?.value?.trim());
});

input?.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        checkWeather(input.value.trim());
    }
});
