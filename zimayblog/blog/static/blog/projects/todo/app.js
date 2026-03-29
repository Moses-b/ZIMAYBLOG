const STORAGE_KEY = "todo-mvp-tasks";

const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");
const emptyState = document.querySelector("#empty-state");
const counter = document.querySelector("#task-counter");

let tasks = loadTasks();
renderTasks();

form?.addEventListener("submit", (event) => {
    event.preventDefault();

    const title = input.value.trim();
    if (!title) {
        input.focus();
        return;
    }

    tasks.unshift({
        id: crypto.randomUUID(),
        title,
        completed: false,
    });

    syncTasks();
    form.reset();
    input.focus();
});

list?.addEventListener("change", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement) || target.type !== "checkbox") {
        return;
    }

    const task = tasks.find((item) => item.id === target.dataset.id);
    if (!task) {
        return;
    }

    task.completed = target.checked;
    syncTasks();
});

list?.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement) || target.dataset.action !== "delete") {
        return;
    }

    tasks = tasks.filter((item) => item.id !== target.dataset.id);
    syncTasks();
});

function loadTasks() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        return saved ? JSON.parse(saved) : [];
    } catch (error) {
        console.error("Impossible de lire les taches sauvegardees.", error);
        return [];
    }
}

function syncTasks() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
    renderTasks();
}

function renderTasks() {
    if (!list || !emptyState || !counter) {
        return;
    }

    list.innerHTML = "";

    tasks.forEach((task) => {
        const item = document.createElement("li");
        item.className = `todo-item${task.completed ? " completed" : ""}`;

        const checkbox = document.createElement("input");
        checkbox.className = "todo-checkbox";
        checkbox.type = "checkbox";
        checkbox.checked = task.completed;
        checkbox.dataset.id = task.id;
        checkbox.setAttribute("aria-label", `Marquer ${task.title} comme terminee`);

        const text = document.createElement("p");
        text.className = "todo-text";
        text.textContent = task.title;

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-btn";
        deleteButton.type = "button";
        deleteButton.dataset.action = "delete";
        deleteButton.dataset.id = task.id;
        deleteButton.textContent = "Supprimer";
        deleteButton.setAttribute("aria-label", `Supprimer ${task.title}`);

        item.append(checkbox, text, deleteButton);
        list.appendChild(item);
    });

    emptyState.hidden = tasks.length > 0;

    const remaining = tasks.filter((task) => !task.completed).length;
    counter.textContent = `${remaining} ${remaining > 1 ? "taches restantes" : "tache restante"}`;
}
