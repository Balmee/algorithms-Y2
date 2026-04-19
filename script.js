const projects = [
  {
    id: "week1",
    title: "Week 1",
    image: "https://picsum.photos/400/200?random=1",
  },
  {
    id: "week2",
    title: "Week 2",
    image: "https://picsum.photos/400/200?random=2",
  },
  {
    id: "week3",
    title: "Week 3",
    image: "https://picsum.photos/400/200?random=3",
  },
  {
    id: "week4",
    title: "Week 4",
    image: "https://picsum.photos/400/200?random=4",
  },
  {
    id: "week5",
    title: "Week 5",
    image: "https://picsum.photos/400/200?random=5",
  },
  {
    id: "week6",
    title: "Week 6",
    image: "https://picsum.photos/400/200?random=6",
  },
  {
    id: "week7",
    title: "Week 7",
    image: "https://picsum.photos/400/200?random=7",
  },
  {
    id: "weekFinal",
    title: "Final Project",
    image: "https://picsum.photos/400/200?random=8",
  }
];

const container = document.getElementById("project-container");

projects.forEach((proj) => {
  const card = document.createElement("div");
  card.className = "project-card";
  card.innerHTML = `
    <img src="${proj.image}" alt="${proj.title}">
    <div class="project-info">
      <h2>${proj.title}</h2>
    </div>
  `;
  card.addEventListener("click", () => {
    window.location.href = `projects/${proj.id}/docs/index.html`;
  });
  container.appendChild(card);
});