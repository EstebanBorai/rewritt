<div>
  <h1 align="center">rewritt</h1>
  <p align="center">
    Self-hostable service for EPUB to PDF conversion.
  </p>
</div>

## Usage

### Run with Docker

A docker image is included to run this application without having to setup every
depencency manually.

```bash
docker-compose up
```

If no `PORT` environment variable was provided, the service must be available at http://0.0.0.0:5000.

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
