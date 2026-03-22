const pass = document.getElementById("pass");
const generateBtn = document.querySelector("button");
const clearBtn = document.getElementById("clear");
const historyList = document.querySelector("ul");

function updateHistory() {
    fetch("/history")
        .then(res => res.json())
        .then(data => {
            historyList.innerHTML = "";
            if (data.length === 0) {
                const li = document.createElement("li");
                li.textContent = "тут тоже ничего";
                historyList.appendChild(li);
            } else {
                data.forEach(pwd => {
                    const li = document.createElement("li");
                    li.textContent = pwd;
                    historyList.appendChild(li);
                });
            }
        });
}

generateBtn.addEventListener("click", () => {
    const length = parseInt(document.getElementById("length").value) || 16;
    const include_specials = document.getElementById("specials").checked;
    const include_digits = document.getElementById("digits").checked;

    fetch("/password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ length, include_specials, include_digits })
    })
    .then(res => res.json())
    .then(data => {
        pass.textContent = data.password;
        updateHistory();
    });
});

pass.addEventListener("click", () => {
    const text = pass.textContent;
    if (text !== "тут пусто") {
        navigator.clipboard.writeText(text).then(() => alert("Пароль скопирован!"));
    }
});

clearBtn.addEventListener("click", () => {
    fetch("/history", { method: "DELETE" })
        .then(res => res.json())
        .then(() => updateHistory());
});


updateHistory();