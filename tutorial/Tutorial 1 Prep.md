# PA1417 — Tutorial 1: Unit Testing with Pytest

## Pre-Tutorial Setup

Complete the following setup steps before attending the tutorial.

### 1. Clone the repository

Clone the course repository to your local machine using your preferred git client or the command line.

### 2. Install and open VSCode

You can use any code editor you prefer. We will use **Visual Studio Code (VSCode)** as our example during the course, so if you don’t have a strong preference, download and install it from [https://code.visualstudio.com](https://code.visualstudio.com). Once installed, open the repository folder in VSCode.

The remaining steps can all be performed using VSCode’s integrated terminal (`Terminal → New Terminal`).

### 3. Confirm Python 3 is installed

Open a terminal and confirm you have Python 3 installed:

```shell
python --version
```

> On some systems (macOS, Linux) Python 3 is accessed via `python3`. Either works. Version 3.10 or newer is recommended.

### 4. Install the dependencies

Navigate to the `backend/` folder of the repository and create a virtual environment there:

```shell
python -m venv venv
```

> On some systems use `python3` instead of `python`.

Activate the virtual environment before installing anything or running any commands. You must do this every time you open a new terminal for this project.

**macOS / Linux:**

```shell
source venv/bin/activate
```

**Windows:**

```shell
venv\Scripts\activate
```

Your terminal prompt should change to show `(venv)` when the environment is active. Then install the dependencies:

```shell
pip install -r requirements.pip
```

Your setup is correct when this command runs without errors:

```shell
pytest --version
```

### 5. Run the test suite

Still from inside `backend/`, confirm pytest can discover and run the existing tests:

```shell
pytest -m demo
```

You should see a results summary. Some of the tests are expected to fail—that is the intended state of the repo. What matters it that pytest runs and shows the results.

### 6. Configure VSCode

**Select the correct Python interpreter:** Press `Cmd+Shift+P`, type “Python: Select Interpreter”, and choose the one pointing to `backend/venv/bin/python`. If it doesn’t appear, select “Enter interpreter path…” and paste the full path.
