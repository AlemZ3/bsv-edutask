# PA1417 — Tutorial 1: Unit Testing with Pytest

This tutorial introduces unit testing in Python using pytest. In Part 1, you will write tests for two functions in `src/util/helpers.py`, progressively learning the AAA pattern, fixtures, mocking, parametrization, and patching. Part 2 extends these concepts with more advanced scenarios.

> Throughout this tutorial, the ✋ symbol means **stop reading and try it yourself** before continuing. Each stop is followed by a collapsed hint — expand it only if you need support.

## Part 1: Unit Testing Basics

### Step 0: Orient Yourself

Open the `backend/` folder in your editor. The structure we care about today:

```
backend/
├── conftest.py          ← empty file; marks this directory as the pytest root
├── pytest.ini           ← pytest configuration
├── requirements.pip     ← Python dependencies (includes pytest and pytest-cov)
├── src/
│   └── util/
│       └── helpers.py   ← the code we will test today
└── test/
    ├── demo/            ← finished reference examples (do not edit these)
    └── unit/            ← where you write your own tests today
```

✋ The `unit` folder is not yet there — create it before moving on.

Open `pytest.ini` and read through it:

```ini
[pytest]
addopts =
    --cov-report term-missing
    --cov=src
testpaths =
    test
markers =
    demo: all tests for demonstration purpose (run with '-m demo')
    unit: all tests on unit/component level (run with '-m unit')
    integration: all tests on integration level (run with '-m integration')
```

- `addopts` — flags applied automatically to every `pytest` run (here: always measure coverage)
- `testpaths` — where pytest looks for test files
- `markers` — named labels to run subsets of tests

Open `src/util/helpers.py` and read the `hasAttribute` function and its docstring. This is the first unit we will test.

---

### Step 1: Designing Test Cases for `hasAttribute`

Before writing any code, derive test cases from the _documentation_, not the code.

✋ **Use the Test Design Technique to derive which tests should exist for this method. Think about the inputs and expected outputs before expanding the hint.**

<details>
<summary>Hint: Test Case Table</summary>

```
hasAttribute(obj: dict, attribute: str) -> bool
  True  — if obj is not None and attribute is a key in obj
  False — if obj is not None and attribute is not a key in obj
  False — if obj is None
```

Fill in the expected values for each combination:

| #   | `obj`      | `attribute`     | Expected |
| --- | ---------- | --------------- | -------- |
| 1   | not `None` | is in `obj`     | ?        |
| 2   | not `None` | is not in `obj` | ?        |
| 3   | `None`     | (irrelevant)    | ?        |

How many valid combinations exist when `obj` is `None`? Why?

> **Principle:** Derive test cases from documentation or a specification — not from the code itself. Code is not ground truth.

</details><br>

---

### Step 2: Implementing the Tests

Create the file `backend/test/unit/test_hasAttribute.py`.

> The `test_` prefix is required — pytest discovers files and functions by name.

✋ **Stop here. Let's slowly write our first unit test together.**

<details>
<summary>Solution Here</summary>

In the `test_hasAttribute.py` file, add the following code:

```python
import pytest
from src.util.helpers import hasAttribute

@pytest.mark.unit
def test_hasAttribute():
    result = hasAttribute({'name': 'Jane'}, 'name')
    assert result == True
```

</details><br>

✋ **Stop here. Write one test function per case and mark each with `@pytest.mark.unit`.**

<details>
<summary>Hint: AAA Pattern</summary>

Structure each test as:

1. **Arrange** — set up the preconditions
2. **Act** — call the unit under test
3. **Assert** — verify the result matches the expected value

> **Principle:** One assert statement per test. Multiple asserts in one test means a failure in the first hides the rest — you lose diagnostic information.

</details><br>

---

### Step 3: Running pytest and Reading the Output

✋ **Run `pytest -m unit` from `backend/` and read the output before continuing.**

Pytest prints one character per test:

- `.` — passed
- `F` — failed
- `E` — error during setup or teardown

When a test fails, the output shows:

- The **name** of the failed test
- The **assert statement** that was not met
- The **error** raised by the code
- A **summary** at the bottom

One of your tests will fail. Read the error carefully — the code crashes rather than returning the expected value. This is a seeded defect: your test found a real bug.

> Observe the coverage table that appears after the results. Because `pytest.ini` sets `addopts = --cov-report term-missing --cov=src`, coverage is measured on every run automatically. The **Missing** column shows which lines were never executed.

---

### Step 4: Reducing Redundancy with Fixtures

✋ **Stop here. Extract the repeated setup across your tests into a `@pytest.fixture` before moving on.**

<details>
<summary>Hint: How Fixtures Work</summary>

- Define a function decorated with `@pytest.fixture` that returns the shared value.
- Any test that declares a parameter with the same name as the fixture will automatically receive it.
- Tests that don't need the shared value should not declare it.

> **Principle:** Encapsulate redundant setup code in fixtures.

</details><br>

<details>
<summary>Solution</summary>

```python
@pytest.fixture
def obj():
    return {'name': 'Jane'}

def test_hasAttribute_true(obj):
    result = hasAttribute(obj, 'name')
    assert result == True
```

</details><br>

Run `pytest -m unit` again to confirm the same results.

---

### Step 5: Testing a Unit with Dependencies — `validateAge`

Open `src/util/helpers.py` and read the `validateAge` method in the `ValidationHelper` class.

✋ **Use the Test Design Technique to derive which tests should exist for this method. Think about the inputs and expected outputs before expanding the hint.**

<details>
<summary>Hint: Test Case Table</summary>

Fill in the expected return value for each age:

| #   | `user['age']` | Expected |
| --- | ------------- | -------- |
| 1   | -1            | ?        |
| 2   | 0             | ?        |
| 3   | 1             | ?        |
| 4   | 17            | ?        |
| 5   | 18            | ?        |
| 6   | 19            | ?        |
| 7   | 119           | ?        |
| 8   | 120           | ?        |
| 9   | 121           | ?        |

</details><br>

✋ **Stop here. Create `backend/test/unit/test_validateAge.py` and try writing tests the same way you did for `hasAttribute`.**

<details>
<summary>What complications did you run into?</summary>

To call `validateAge`, you need a `ValidationHelper` instance. Its constructor takes a `UserController` — which in turn depends on a `DAO`, which expects a real database connection. Every dependency pulls in another, and the test is no longer testing just `validateAge`.

This is the problem with tightly coupled dependencies: to test one unit, you end up needing the entire stack running.

We solve this by **mocking**: replacing the real `UserController` with a fake object whose behaviour we fully control. This isolates `validateAge` completely — if the test fails, we know the bug is in `validateAge`, not in any of its dependencies.

Python's standard library provides `unittest.mock.MagicMock`. You can use it to create a fake `UserController` whose `.get()` method returns whatever dict you tell it to — no real database needed.

</details><br>

✋ **Stop here. Rewrite your tests using what you just read before moving on.**

Run `pytest -m unit`. Both the new tests and the `hasAttribute` tests will run.

---

### Step 6: Avoiding Loops — Parametrization

✋ **Stop here. Rewrite `test_validateAge.py` as a single parametrized test function covering all 9 rows before moving on.**

<details>
<summary>Hint: Parametrize Syntax</summary>

Writing all 9 cases as separate functions is correct but repetitive. Loops in test code are worse — they hide which specific input caused a failure. Use `@pytest.mark.parametrize` instead:

```python
@pytest.mark.parametrize('param1, param2', [
    (value1a, value2a),
    (value1b, value2b),
    ...
])
def test_name(param1, param2):
    ...
```

</details><br>

Run `pytest -m unit`. Pytest now runs 9 separate test instances and labels each with its parameters (e.g., `test_validateAge[18-valid]`). One test will fail — read the output to identify which age value exposes the seeded defect.

> **Principle:** Avoid control structures (loops, conditions) in test code. Use `@pytest.mark.parametrize` instead.

---

### Step 7: Combining Fixtures with Parametrization

✋ **Stop here. Move the mock setup into a fixture so that the test body only calls the method and asserts the result.**

<details>
<summary>Hint</summary>

- Define a `@pytest.fixture` that accepts `age` as a parameter, builds the mock, and returns the `ValidationHelper` instance.
- When a `@pytest.mark.parametrize` variable name matches a fixture parameter name, pytest forwards it automatically — no extra wiring needed.

</details><br>

Run `pytest -m unit`. The results should be identical to before — you only changed the structure.

To observe how pytest sets up and tears down each fixture:

```
pytest -m unit --setup-show
```

To print to the console during a run (useful for debugging):

```
pytest -m unit --capture=no
```

---

### Summary (Steps 1–7)

By the end of Step 7, `backend/test/unit/` contains two files demonstrating the two core patterns for unit testing in this course:

| File                   | Concepts covered                            |
| ---------------------- | ------------------------------------------- |
| `test_hasAttribute.py` | AAA pattern, fixtures, coverage             |
| `test_validateAge.py`  | Mocking, parametrize, parametrized fixtures |

The two seeded defects you found:

1. `hasAttribute` — crashes on `None` input instead of returning `False`
2. `validateAge` — one boundary condition is off by one

These are intentional. Do not fix them — future assignments will involve finding and documenting defects like these.

Continue below to explore more advanced topics, each grounded in a demo file under `backend/test/demo/`.

---

## Part 2: Advanced Topics

The remaining steps each introduce one new concept, building on what came before. For each step you will write a new test file in `backend/test/unit/` and compare your result against the corresponding demo file in `backend/test/demo/` afterwards.

---

### Step 8: Patching Non-Injectable Dependencies — `test_diceroll.py`

**Corresponding demo file:** `backend/test/demo/test_impure.py`

Open `src/util/helpers.py` and read the `diceroll` function and its docstring.

```
diceroll() -> bool
  True  — if the rolled number is higher than 4
  False — otherwise
```

Unlike `ValidationHelper`, this function does not accept any arguments — there is no way to inject a mock. It calls `random.randint` directly. This is an **impure** function: its output depends on something outside our control.

✋ **Stop here. Create `backend/test/unit/test_diceroll.py` and write a single test that calls `diceroll()` and asserts a specific return value.**

Run it a few times with `pytest -m unit --capture=no`. What do you observe? Does the test reliably pass or fail?

Why this is a problem: A test that passes sometimes and fails sometimes is worse than no test at all — it trains you to ignore failures. The solution is to control the random number by replacing `random.randint` with a fake that always returns what you tell it to.

✋ **Stop here. Rewrite your test so that `random.randint` always returns a fixed value before moving on.**

<details>
<summary>Hint: Using `patch`</summary>

The standard library's `unittest.mock.patch` temporarily replaces a name in a module with a `MagicMock` during the test. Use it as a context manager:

```python
with patch('module.path.to.name') as mock_name:
    mock_name.return_value = ...
    # inside this block, the real function is replaced
```

The name to patch is the one your module _uses_ — in this case, `diceroll` calls `random.randint` from within `helpers.py`. Think about which string you would pass to `patch(...)` to intercept that call.

</details><br>

✋ **Stop here. Identify the boundary values from the docstring and rewrite the test using `@pytest.mark.parametrize` to cover all cases.**

<details>
<summary>What To Expect</summary>

One of your parametrized test cases will fail. Read the output to identify which value exposes a discrepancy between the docstring and the code.

</details><br>

> **Principle:** Patch non-injectable dependencies to make impure functions deterministic and testable.

---

### Step 9: Fixture Teardown with `yield` — `test_filehandler.py`

**Corresponding demo file:** `backend/test/demo/test_yield.py`

Open `backend/test/demo/test_yield.py`. It defines a `FileHandler` class that reads a JSON file and returns its contents. The class is defined inside the test file itself — read it carefully, then copy the class definition into your new file `backend/test/unit/test_filehandler.py`.

Testing `FileHandler` requires a real file to exist on disk. Your fixture must create a temporary JSON file before the test and delete it after — even if the test fails.

✋ **Stop here. Write a test that creates the file, tests the result, and cleans up — all inside the test body.**

Run it and confirm it passes. Then ask yourself: what happens to the file if the assertion fails mid-test?

✋ **Stop here. Move the file creation and `FileHandler` instantiation into a `@pytest.fixture` using `return`.**

Run the test again. Now ask: is the file ever cleaned up?

✋ **Stop here. Replace `return` with `yield` in your fixture and add the file-deletion call after the `yield`.**

Any code written _after_ the `yield` statement runs once the test has finished — regardless of whether the test passed or failed. Run the test, then check that the temporary file no longer exists on disk.

> **Principle:** Use `yield` in a fixture when the setup requires a matching teardown (resource acquisition, file creation, database seeding, etc.).

As a final step, wrap your fixture and test inside a class. In pytest, fixtures defined inside a class are scoped to that class and do not conflict with identically-named fixtures elsewhere. Compare your result with `test_yield.py` in the demo folder.

---

### Step 10: Patching Hard-Coded Dependencies — `test_validationhelper2.py`

**Corresponding demo file:** `backend/test/demo/test_patch.py`

Open `src/util/helpers.py` and read the `ValidationHelper2` class. Notice that `ValidationHelper2.__init__` creates its own `UserController` and `DAO` objects internally — there is no constructor parameter to inject a mock into.

✋ **Stop here. Try writing a test for `ValidationHelper2` the same way you did in Step 5.**

<details>
<summary>What To Consider</summary>

Create a `MagicMock` and pass it to the constructor. What happens? Does Python accept it? Does the test reach the assertion?

</details><br>

✋ **Stop here. Write a working test using `patch` to replace the hard-coded dependencies before moving on.**

<details>
<summary>Hint: Patching Classes</summary>

`patch` can replace a _class_ for the duration of a test, so that when the code under test calls `UserController(...)` or `DAO(...)`, it gets a mock instead of the real object:

```python
with patch('src.util.helpers.SomeClass', autospec=True) as MockClass:
    MockClass.return_value = ...  # controls what __init__ returns
```

You need to patch both `UserController` and `DAO`. You can nest two `with patch(...)` blocks or combine them on one line using a backslash continuation.

</details><br>

`patch` can also be applied as a _decorator_ directly above a fixture or test function. Try rewriting your fixture using `@patch(...)` decorators and compare both syntaxes against `test_patch.py` in the demo folder.

> **Principle:** Patch at the location where the name is used, not where it is defined — `src.util.helpers.UserController`, not `src.controllers.usercontroller.UserController`.

---

### Step 11: Understanding Patch Namespaces — `test_namespaces.py` (Exercise)

**Corresponding demo file:** `backend/test/demo/test_namespaces.py`

The most common mistake with `patch` is patching the wrong namespace. The rule is:

> **Patch where the name is looked up, not where the object is defined.**

When a module does `from foo import bar`, it creates its own reference to `bar`. Patching `foo.bar` after the import has no effect — you must patch `that_module.bar`.

Open `backend/test/demo/test_namespaces.py`. It contains three test methods, each with a `# TODO` comment and a `patch('?')` placeholder. Work through each in order.

**Exercise 1 — `test_1`**

✋ **Stop here and fill in `test_1` before moving on.**

<details>
<summary>Hint</summary>

The function `getDao` in `src/util/daos.py` creates a `DAO` object internally. What string would you pass to `patch(...)` to intercept that specific instantiation? Think about where `DAO` is referenced inside the `daos` module.

</details><br>

**Exercise 2 — `test_2`**

✋ **Stop here and fill in `test_2` before moving on.**

<details>
<summary>Hint</summary>

The `diceroll` function in `src/util/helpers.py` calls `random.randint`. In Step 8 you patched `random.randint` directly — but `helpers.py` imports `random` as a whole module and calls `random.randint(...)`. Consider: does patching `random.randint` still work here, or do you need a different path?

</details><br>

**Exercise 3 — `test_3`**

✋ **Stop here and fill in `test_3` before moving on.**

<details>
<summary>Hint</summary>

This test combines two techniques: inject a mocked DAO into `UserController` via the constructor (as you did in earlier steps), and separately patch `re.fullmatch` so that email validation always passes. You need to figure out the correct namespace string for `fullmatch` given how it is called inside `usercontroller.py`.

</details><br>

Run each test after filling in its `patch(...)` argument:

```
pytest backend/test/demo/test_namespaces.py -m namespaces -v
```

> **Tip:** When unsure of the correct namespace, add a `print(mock)` inside the `with` block and run with `--capture=no` to confirm which object was actually replaced.

---

## Final Summary

| Step | File                        | New concepts introduced                                       |
| ---- | --------------------------- | ------------------------------------------------------------- |
| 1–4  | `test_hasAttribute.py`      | AAA pattern, fixtures, coverage                               |
| 5–7  | `test_validateAge.py`       | DI mocking, parametrize, parametrized fixtures                |
| 8    | `test_diceroll.py`          | `patch` as context manager, impure functions                  |
| 9    | `test_filehandler.py`       | `yield` in fixtures, fixture teardown, class-based tests      |
| 10   | `test_validationhelper2.py` | Patching hard-coded deps, decorator vs context manager syntax |
| 11   | `test_namespaces.py` (demo) | Patch namespace resolution, combining DI and patching         |

The seeded defects you should have encountered:

1. `hasAttribute` — crashes on `None` input
2. `validateAge` — off-by-one boundary condition
3. `diceroll` — discrepancy between docstring and comparison operator

Do not fix them — they are there to practice recognising and documenting defects.
