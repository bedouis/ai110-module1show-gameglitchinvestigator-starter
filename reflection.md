# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game seemed glitchy from the beginning. The attempts counter did not match the difficulty settings, and displayed updates sometimes lagged behind the game’s feedback. The input field also showed “Press Enter to apply” alongside a **Submit Guess** button, making it unclear whether pressing Enter submitted a guess or only updated the input.

Three concrete bugs stood out during my initial testing:

### Bug 1: Initial attempts counter mismatch

- **Input/trigger:** Launch the app without submitting a guess or clicking **New Game**.
- **Expected behavior:** **Attempts left** should equal the sidebar’s **Attempts allowed** value because no guesses have been made.
- **Actual behavior:** The values differed on launch. Clicking **New Game** made them match.
- **Suspected code location:** The session-state initialization block in `app.py` sets `st.session_state.attempts = 1`. The attempts banner subtracts this value from the attempt limit, displaying one fewer available attempt. The `if new_game:` block resets attempts to zero instead.

### Bug 2: Inconsistent number range

- **Input/trigger:** Select **Hard** difficulty and click **New Game**.
- **Expected behavior:** The sidebar, instructions, and generated secret should all use Hard’s displayed range of **1–50**.
- **Actual behavior:** The sidebar showed **1–50**, while the instructions said **1–100**. The secret could also exceed 50; one recorded example was **69**.
- **Suspected code location:** In `app.py`, `get_range_for_difficulty()` supplies the sidebar’s range, but the `st.info()` instructions hardcode 1–100. The `if new_game:` block also uses `random.randint(1, 100)` instead of the difficulty-specific bounds.

### Bug 3: Debug counters and history lag behind feedback

- **Input/trigger:** Submit a guess and immediately inspect **Developer Debug Info**.
- **Expected behavior:** The attempt counter and history should reflect the latest submission when its feedback appears.
- **Actual behavior:** “Correct!” appeared for the guess **66** while the history excluded that guess and the attempt counter still showed **four**.
- **Suspected code location:** In `app.py`, the attempts banner and **Developer Debug Info** are rendered before the `if submit:` block. That later block increments attempts and updates history, leaving the information already displayed on the page behind the current feedback.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
| --- | --- | --- | --- |
| Launch the app. | **Attempts left** should equal **Attempts allowed** in the sidebar. | On launch, **Attempts left** is one less than **Attempts allowed**. Changing the difficulty does not resolve the mismatch. Starting a new game makes the values match. | Not captured. The counter mismatch is visible in the UI. |
| Submit a number different from the secret. | The hint should display “Go HIGHER!” when the guess is below the secret and “Go LOWER!” when it is above the secret. | The hint suggests the opposite direction. | Not captured. The incorrect hint appears in the UI. |
| Start a new game with **Hard** difficulty selected. | The sidebar, instructions, and generated secret should use Hard’s range of **1–50**. | The sidebar displays **1–50**, but the instructions say **1–100**. The generated secret can exceed 50; one recorded example is **69**. | Not captured. The conflicting ranges and secret are visible in the UI. |
| Submit an out-of-range number: a negative number, zero, or a number above the difficulty’s maximum. | The game should reject the guess, display the allowed range, and leave the remaining attempts unchanged. | Out-of-range numbers are accepted as guesses and consume attempts. | Not captured. The guesses are accepted without a range-validation message. |
| Submit a decimal number, such as `5.6`. | The game should reject the guess without consuming an attempt and display a message requesting a whole number. | The decimal is converted to an integer and processed as a guess. If the converted integer matches the secret, the player wins. | Not captured. No conversion warning appears. The converted value is visible in **Developer Debug Info**. |
| Submit a guess and inspect **Developer Debug Info**. | The attempt counter and history should immediately reflect the submitted guess. | The counter and history still show the previous state and update on a subsequent interaction. | Not captured. The delayed updates are visible in the UI. |
| Click **New Game**, particularly after a win or game over. | The button should start a playable new round with the game state reset. | The button does not reliably restore a playable game, even after rerunning. In my testing, it started working after clearing the cache and rerunning. | Not captured. The failed reset is visible in the UI. |
| Submit nonnumeric input, such as `text` or `5/4`. | The game should display a validation error without consuming an attempt. | The game displays “That is not a number.” but also consumes an attempt. | Not captured. The error message and attempt deduction are visible in the UI. |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
