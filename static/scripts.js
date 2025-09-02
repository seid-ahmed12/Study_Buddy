function generateFlashcards() {
  const notes = document.getElementById("notes").value;

  fetch("http://127.0.0.1:5000/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ notes }),
  })
    .then((res) => res.json())
    .then((data) => {
      const container = document.getElementById("flashcards");
      container.innerHTML = "";
      data.forEach((card) => {
        const flashcard = document.createElement("div");
        flashcard.classList.add("flashcard");
        flashcard.innerHTML = `
                <div class="flashcard-inner">
                    <div class="flashcard-front">
                        <p>${card.question}</p>
                    </div>
                    <div class="flashcard-back">
                        <p>Answer: ${card.answer}</p>
                    </div>
                </div>
            `;
        flashcard.addEventListener("click", () => {
          flashcard.classList.toggle("flipped");
        });
        container.appendChild(flashcard);
      });
    })
    .catch((err) => console.error(err));
}
