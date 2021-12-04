<div>
  <h1 align="center">rahool</h1>
  <p>EPUB to PDF converter</p>
</div>

## Usage

Create a PDF from the provided EPUB with the same name in the current working
directory (CWD).

```bash
rahool ./filename.epub
```

## Development

This project makes use of `pyenv` and `pipenv`, make sure you install the
Python version specified in `.python-version` and use a virtual enviroment to
work with this project locally.

```bash
python --version
> 3.10.0
```

Install dependencies using Pipenv:

```bash
python -m pipenv install
```

Finally create or initialize the Pipenv shell in the repository directory:

```bash
python -m pipenv shell
```

When you are done working with this project, make sure you exit the Pipevn shell
by runing the `exit` command.

## What does "Rahool" means?

In _Destiny_ (the Game from Bungie), Rahool is the name of one of the merchants
capable of decrypting "Engrams".

Given that some apps aren't able to open EPUB files and my main goal is to have
these files available in my favorite PDF reader I'm calling this project Rahool.

### Code Style

We use Black for code styling in this repository.
Install Black as follows:

```bash
pipenv install black
```

Then execute it against all Python files in the codebase:

```bash
python -m black ./**/*.py
```

### Pyright Config

If you are using Pyright make sure you create a config file like the
following with the contents:

```js
// pyrightconfig.json
{
  "venvPath": "<Virtual Environments Directory Path>",
  "venv": "<Virtual Environment Directory Name>",
}
```

## License

Licensed under the MIT License
