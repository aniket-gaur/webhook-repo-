async function fetchEvents() {
  const res = await fetch("/events");
  const data = await res.json();
  const list = document.getElementById("event-list");

  list.innerHTML = "";

  data.forEach((event) => {
    let text = "";
    if (event.type === "push") {
      text = `${event.author} pushed to ${event.to_branch} on ${event.timestamp}`;
    } else if (event.type === "pull_request") {
      text = `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
    } else if (event.type === "merge") {
      text = `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${event.timestamp}`;
    }

    const li = document.createElement("li");
    li.textContent = text;
    list.appendChild(li);
  });
}

//func to fetch events every 15 seconds
fetchEvents();
setInterval(fetchEvents, 15000);
