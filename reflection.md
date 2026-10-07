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

I used Claude AI coding assistant to help investigate, refactor, and test the game. One suggestion that was correct was to move check_guess out of app.py and into logic_utils.py, while keeping the Streamlit-specific hint messages in app.py. The AI also removed the unnecessary logic that converted the secret number to a string on alternating attempts. This made check_guess a small, testable function that returns only "Win", "Too High", or "Too Low", which matched the expectations of the existing tests. I verified this change by running pytest, and all three original game-logic tests passed.

One AI result I did not accept as complete was its first version of the refactor, because it intentionally left the user-facing hint messages unchanged. That meant "Too High" still displayed "Go HIGHER!" and "Too Low" still displayed "Go LOWER!". Although the refactor itself was correct, it did not completely fix the bug I had observed in the game, so I asked the AI to update the HINT_MESSAGES mapping separately. After that change, "Too High" correctly told the player to go lower and "Too Low" correctly told the player to go higher. I verified the change by rerunning pytest and adding a regression test specifically checking that the hint direction matches the outcome.

---

## 3. Debugging and testing your fixes

I decided that a bug was fixed only after I could verify the new behavior with tests and by running the Streamlit app again. Before the refactor, the tests could not exercise the intended implementation because logic_utils.py still contained NotImplementedError. After moving check_guess into logic_utils.py, all three original tests passed, confirming that winning, too-high, and too-low guesses were being classified correctly.

I then added a regression test for the reversed hint bug. The test uses check_guess to produce the outcome and verifies that a "Too High" result maps to a message containing "LOWER" and a "Too Low" result maps to one containing "HIGHER". After adding this test, all four tests passed.

For the new-game and difficulty bugs, the AI helped me create additional tests using Streamlit's AppTest. These tests verified that a fresh game begins with zero attempts used, the instructions reflect the selected difficulty range, New Game generates the secret using the selected difficulty's range, and New Game resets attempts, score, status, and history. The full suite finished with eight passing tests.

I also ran the Streamlit app again and checked the fixes directly in the interface. I verified that guesses below the secret told me to go higher, guesses above the secret told me to go lower, the displayed range changed correctly with the selected difficulty, and starting a new game reset the game state as expected. This manual check helped confirm that the fixes worked not only in isolated tests but also in the actual user experience.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
