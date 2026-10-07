# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

The purpose of this project was to debug an AI-generated Streamlit number guessing game and make its behavior consistent and testable.

I found several bugs, including reversed high/low hints, incorrect attempt counting, difficulty ranges that did not match the generated secret, and incomplete New Game state resets.

I fixed the core guess-checking logic by moving it into `logic_utils.py`, corrected the hint mapping, fixed difficulty-specific ranges and game resets, and added regression tests to verify the repairs.

## 📸 Demo Walkthrough

1. User starts a Normal game with the full number of attempts available.
2. User enters a guess below the secret number.
3. The game returns "Too Low" and tells the user to go higher.
4. User enters a guess above the secret number.
5. The game returns "Too High" and tells the user to go lower.
6. User enters the correct number and wins the game.
7. Clicking New Game resets the score, attempts, history, and game status.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

============================================================= test session starts =============================================================
platform darwin -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/sbedoui/codepath/ai110-module1show-gameglitchinvestigator-starter
configfile: pytest.ini
plugins: anyio-4.7.0
collected 8 items                                                                                                                             

tests/test_game_logic.py ........                                                                                                       [100%]

============================================================== 8 passed in 0.63s ==============================================================


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
