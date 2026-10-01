

const texts = ["Lerne Programmieren",
               "Lerne Python",
               "Lerne Full-Stack",
               "Lerne Back-End",
               "Lerne Front-End",
               "Lerne VS Code",
               "Lerne Git",
               "Lerne KI-Systeme"];

let count = 0, index = 0, currentText = "", letter = "";

(function type() {
  if (count === texts.length) count = 0;
  currentText = texts[count];
  letter = currentText.slice(0, ++index);
  
  document.querySelector("h1").textContent = letter;
  if (letter.length === currentText.length) {
    setTimeout(() => {
      let deleteInterval = setInterval(() => {
        letter = currentText.slice(0, --index);
        document.querySelector("h1").textContent = letter;
        if (letter === "Lerne ") { clearInterval(deleteInterval); count++; index = 6; setTimeout(type, 500); }
      }, 100);
    }, 1500);
  } else { setTimeout(type, 150); }
}());