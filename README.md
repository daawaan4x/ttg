# 🟰 Truth Table Generator

A Truth Table Generator for Propositional Logic Formulas made with Python.

<div align="center">
	<img width="640" src="./imgs/p_and_q.png" alt="Truth Table Generator">
</div>

## Features

- **Supported Logical Operators**: In order of precedence 
	- `NOT`, `not`, `!`, `~`, `¬`
	- `AND`, `and`, `&`, `&&`, `^`, `∧`
	- `OR`, `or`, `|`, `||`, `v`, `∨`,
	- `THEN`, `then`, `>`, `->`, `→`,
- **Complex Formulas**: Input nested formulas using parenthesis `(...)` 
- **Unlimited Variables**: Add any amount of variables using any combination of alphabet `a-z,A-Z` letters.
- **Input using CLI or File**: Choose either the CLI or a file for input.

## Usage

Open a terminal on this project's root folder.

If you want to use the compiled binaries, simply run the executable file for your operating system from the `./bin` subfolder. Following is an example for Windows.

```sh
cd <this-project-folder>/bin

./ttg "P & Q" 
./ttg "P & Q" --inspect
./ttg input.txt --file
./ttg input.txt --file --inspect
```

---

If you want to run it from source, *setup the project first by visiting section* `Running from Source` *for more information*. Afterwards, simply run `python ttg ...`.

```sh
cd <this-project-folder>

python ttg 

python ttg "P & Q" 
python ttg "P & Q" --inspect
python ttg input.txt --file
python ttg input.txt --file --inspect
```

---

For more usage info, you can run `ttg --help`.

## Running from Source

**Recommended**: Install `Python 3.8` using a version manager such as `pyenv` from https://github.com/pyenv/pyenv/ (Unix) or https://github.com/pyenv-win/pyenv-win (Windows).

Alternatively, you can install python packages from https://www.python.org/downloads/.

**Recommended**: After setting up your python installation, install the project's dependencies with the following commands. Visit `venv` docs from https://docs.python.org/3/library/venv.html for more information:

```sh
cd <this-project-folder>

python -m venv .venv

# --- UNIX ---
source .venv/bin/activate # bash/zsh
.venv/Scripts/Activate.ps1 # Powershell

# --- Windows ---
source .venv/bin/Scripts/activate # bash/zsh
.venv\Scripts\activate.bat # Command Prompt
.venv\Scripts\Activate.ps1 # Powershell



pip install -r requirements.txt
```

Done! Simply run the project with the following:

```sh
python ttg
```

## Compiling from Soure

In order to compile the project into a standalone executable, you will need `pyinstaller` from https://github.com/pyinstaller/pyinstaller (already included in `requirements.txt`). Visit the link for more information.

> **NOTE:** You can only compile to an executable format native to your current operating system (e.g. you can only create `.exe` files when compiling from Windows).

The following will build the project into a single-file standalone executable in the `./bin` folder.

```sh
pyinstaller ttg/__main__.py --onefile --clean --specpath "./bin/spec" --distpath "./bin" --workpath "./bin/build" --name "ttg"
```