# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Create a high score setting.

**What did the agent do?**

Read the files before inserting several lines: a Streamlit `metric` for the high score, a line initializing the high score to 0 (only at the start of the app, not after a new game), and basic logic updating the high score if we obtain a score that is greater than it.

**What did you have to verify or fix manually?**

I verified that the initialization was in the correct place, as well as checking the app to make sure that the metric placed in the sidebar would accurately reflect a high score. The agent made an error by placing the logic to update the high score such that it runs after every single guess, not after winning a game, which I observed and reprompted it to fix.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

```
General prompt used:
Add some difficult edge cases for @tests/test_game_logic.py  based on the functions in @logic_utils.py . You might test multiple function calls in sequence to make sure the entire workflow is solid, and especially edge cases covering all of the logic for parse_guess and update_score. Do not overwrite or replace any existing tests in the test file.
```

|     Edge Case     |     Prompt Used     |     AI-Suggested Test     |     Did It Pass?     |     Your Reasoning     |
|-------------------|---------------------|---------------------------|----------------------|------------------------|
| Numbers within whitespace | (general)   | parse_guess("  42  ") == (True, 42, None) |  Yes | As the chatbot explained, the parse function `int()` should be able to handle arbitrary whitespace on both sides. |
| Numbers with multiple dots | (general)  | parse_guess("10.5.5") == (False, None, "That is not a number.") | Yes | This makes sense because the program will attempt to cast "10.5.5" from a float to an int, which results in an error, but this error is caught. |
| Full workflow: multiple function calls | (general) | (see below) | Yes | The first guess was too high, the second guess was too low, and the third guess was correct. As expected, this caused the number of attempts to accumulate and the score to decrease, then the amount earned from the win is correctly calculated based on the cumulative number of attempts. |

Workflow Test for #3:
```
def test_full_workflow_misses_then_win_accumulates_score():
    # Two wrong guesses (-5 each) then a win on attempt 3 (100 - 20 = 80).
    secret = 30
    score = 0

    ok, g1, _ = parse_guess("40")
    out1, _ = check_guess(g1, secret)
    assert out1 == "Too High"
    score = update_score(score, out1, 1)
    assert score == -5

    ok, g2, _ = parse_guess("3.9")  # truncates to 3, still too low
    out2, _ = check_guess(g2, secret)
    assert out2 == "Too Low"
    score = update_score(score, out2, 2)
    assert score == -10

    ok, g3, _ = parse_guess("30")
    out3, _ = check_guess(g3, secret)
    assert out3 == "Win"
    score = update_score(score, out3, 3)
    # -10 + (100 - 10*2) = -10 + 80 = 70
    assert score == 70
```

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Add descriptive docstrings to each of the functions in @logic_utils.py , and verify that both the provided docstrings and the functions themselves follow PEP 8 guidelines.
```

**Linting output before:**

```
No linter was installed, but the agent notified me that some of the comments did not have spaces immediately following the #, which violated E265, and changed one comment that may have gone past the horizontal span limit as a result.
```

**Changes applied:**

The AI generated descriptive docstrings for each of the functions, which I verified to make sure they aligned with what the function does. (for example, the docstring for update_score attempted to address the default case where the input message is not win, too high, or too low, which is impossible and is simply addressed as an edge case that should not happen but is accounted for anyway) Additionally, I added spaces between some of the comments and their text. I prompted it further to make sure all the names follow the conventions (snake case, e.g.), and there were no issues.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
