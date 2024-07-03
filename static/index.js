// alert("OK");
let tg = window.Telegram.WebApp;
tg.expand();

const btn = document.getElementById("coin");
const counter = document.getElementById("counter");
const title = document.getElementById("title");

const first_name = tg.initDataUnsafe.user.first_name;
const last_name = tg.initDataUnsafe.user.last_name;

const username = first_name + " " + last_name;
const userId = tg.initDataUnsafe.user.id;
let counterValue = 0;

let socket = new WebSocket("/ws");

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  counterValue = data.score;
  renderCounter();
  console.log(data);
};

function renderCounter() {
  counter.textContent = counterValue;
}

function increaseCounter() {
  counterValue++;
  tg.HapticFeedback.impactOccurred("medium")	

  socket.send(
    JSON.stringify({
      type: "increase",
      value: counterValue,
      id: userId,
    })
  );

  renderCounter();
}

function authUser() {
  socket.send(
    JSON.stringify({
      type: "auth",
      id: userId,
      username: username,
    })
  );
}

socket.onopen = (d) => {
  title.textContent = `Привіт, ${username}`;
  authUser();

  btn.addEventListener("click", (e) => {
    increaseCounter();
  });
  btn.removeAttribute("disabled");
};
