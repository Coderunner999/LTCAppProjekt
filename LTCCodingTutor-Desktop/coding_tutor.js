

// limits und allgemeine variablen:
const messageLimit = 10;
let liveMessages = 0;

let chatContent = document.querySelector(".chat-content");

// Nachricht der Ai im chat einfügen:
function appendBotMessage(messageText) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot-message";

  const avatar = document.createElement("div");
  avatar.className = "fas fa-robot message-avatar";

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  contentDiv.textContent = messageText;

  messageDiv.append(avatar, contentDiv);
  chatContent.appendChild(messageDiv);

  chatContent.scrollTop = chatContent.scrollHeight;
}

// Begrüßungs Message von der AI:
appendBotMessage("Hallo! Ich bin der AI Coding Tutor von LTC, wie kann ich dir helfen? 😊");


// Amtwort erstellen und zurückschicken:
function getAnswer() {
  if (liveMessages === messageLimit) {
    appendBotMessage(
      "Ich würde diese Frage gerne beantworten, aber es scheint als hättest du das Limit an kostenlosen Nachrichten erreicht!",
    );
    // Sperre von einagbefeld wenn limit ereicht
    document.getElementById("request").value = "";
    document.getElementById("request").disabled = true;
    return "Limit reached!";
  }

  let request = document.getElementById("request").value;
  appendUserMessage(request);

  if (request === "hallo" || request === "Hallo" || request === "Moin") {
    setTimeout(function () {
      appendBotMessage("Hallo! Welches Coding-Thema wollen wir heute aufgreifen? 😎");
    }, 2000);
  } else if (request === "Wer bist du" || request === "wer bist du") {
    setTimeout(function () {
      appendBotMessage(
        "Ich bin dein persönlicher AI Coding Tutor, wie kann ich dir beim Lernen helfen? 😊",
      );
    }, 2000);
  } else if (request === "nichts" || request === "Nichts") {
    setTimeout(function () {
      appendBotMessage(
        "OK, dann eben mal heute ncihts, aber du weißt ja: ich bin immer hier wenn du mich brauchst! 😊",
      );
    }, 2000);
  } else if (
    request === "Keine ahnung" ||
    request === "keine ahnung" ||
    request === "Keine Ahnung"
  ) {
    setTimeout(function () {
      appendBotMessage(
        "Das ist überhaupt kein Problem! Wie möchtest du an der Sache herangehen? 😊",
      );
    }, 2000);
  } else if (request === "nein" || request === "Nein") {
    setTimeout(function () {
      appendBotMessage(
        "Verstanden, gibt es noch weitere Anweisungen, Aufgaben, etc.? 🤔",
      );
    }, 2000);
  } else if (request === "was kannst du" || request === "Was kannst du") {
    setTimeout(function () {
      appendBotMessage(
        "Ich kann dir helfen Code zu verstehen, Projekte aufzubauen,oder einfach mal nur mit dir Zeit verbringen! 😏",
      );
    }, 2000);
  } else if (request === "bist du schlau" || request === "Bist du schlau") {
    setTimeout(function () {
      appendBotMessage(
        "Ich bin schlau genug für die meisten deiner Aufgaben! 😉",
      );
    }, 2000);
  } else if (request === "klar" || request === "Klar") {
    setTimeout(function () {
      appendBotMessage("Wie möchtest du jetzt fortfahren? 🤔");
    }, 2000);
  } else if (request === "du bist dumm" || request === "Du bist dumm") {
    setTimeout(function () {
      appendBotMessage(
        "Das tut mir leid zu hören! 😕 Was kann ich besser machen?",
      );
    }, 2000);
  } else if (
    request === "hast du ein limit" ||
    request === "Hast du ein Limit"
  ) {
    setTimeout(function () {
      let freeMessagesLeft = messageLimit - liveMessages;
      appendBotMessage(
        "Bei mir hast du ein Nachrichtenlimit von " +
          messageLimit +
          ". Du hast aktuell noch " +
          freeMessagesLeft +
          " Nachrichten frei. Wofür wollen wir diese nutzen?",
      );
    }, 2000);
  } else if (
    request === "wie viele fragen noch" ||
    request === "Wie viele Fragen noch" ||
    request === "wie viele nachrichten noch" ||
    request === "Wie viele Nachrichten noch"
  ) {
    setTimeout(function () {
      appendBotMessage("AGENTIC AI MODE");
      setTimeout(function () {
        appendBotMessage("Analysiere Anfrage...");
        setTimeout(function () {
          appendBotMessage("Rechne nach...");
          setTimeout(function () {
            appendBotMessage("Werte Daten aus...");
            setTimeout(function () {
              appendBotMessage("Erstelle professionelle Antwort...");
              setTimeout(function () {
                let freeMessagesLeft = messageLimit - liveMessages;
                appendBotMessage(
                  "Agentic AI: Das Ergenis ist da. Ich habe alle Schritte sauber durchzogen, und du hast noch exakt " +
                    freeMessagesLeft +
                    " Nachrichten frei.",
                );
              }, 7500);
            }, 7500);
          }, 7500);
        }, 7500);
      }, 2000);
    }, 500);
  } else {
    setTimeout(function () {
      appendBotMessage(
        "Aktiviere Agentic AI Mode mit stärkster, und modernster Leistung, um die beste Antwort auf deine Nachricht zu finden...",
      );
      setTimeout(function () {
        appendBotMessage("AGENTIC AI MODE");
        setTimeout(function () {
          appendBotMessage("Analysiere Anfrage...");
          setTimeout(function () {
            appendBotMessage("Suche nach Antwortdaten...");
            setTimeout(function () {
              appendBotMessage("Fehlgeschlagen, suche im Web nach Daten...");
              setTimeout(function () {
                appendBotMessage(
                  "Agentic AI: Ich konnte leider trotz intensiver Rechenleistung, keine Antwort finden. Vielleicht versuchst du es mit einer anderen Anfrage?",
                );
              }, 7500);
            }, 7500);
          }, 7500);
        }, 7500);
      }, 30000);
    }, 3000);
  }
  liveMessages++;
  // eingabe nach dem senden leeren:
  document.getElementById("request").value = "";
}

// message vom user anzeigen im chat:
function appendUserMessage(request) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message user-message";

  const avatar = document.createElement("div");
  avatar.className = "fas fa-smile message-avatar";

  const contentDiv = document.createElement("div");
  contentDiv.className = "message-content";
  contentDiv.textContent = request;

  messageDiv.append(avatar, contentDiv);
  chatContent.appendChild(messageDiv);

  chatContent.scrollTop = chatContent.scrollHeight;
}

// tastendruck message senden:
document.getElementById("request").addEventListener("keydown", function(event) {
  if (event.key === "Enter") {
    getAnswer();
  }
});

// Funktion zum resetten des chats:
function resetChat() {
  chatContent.innerHTML = "";
  liveMessages = 0;
  let input = document.getElementById("request");
  input.disabled = false;
  input.value = "";
  appendBotMessage("Hallo! Ich bin Nexora, wie kann ich dir helfen?");
}
