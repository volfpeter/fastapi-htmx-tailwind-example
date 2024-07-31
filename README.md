![Tests](https://github.com/volfpeter/fastapi-htmx-tailwind-example/actions/workflows/tests.yml/badge.svg)
![Linters](https://github.com/volfpeter/fastapi-htmx-tailwind-example/actions/workflows/linters.yml/badge.svg)

# fastapi-htmx-tailwind-example

Example application (IoT dashboard) built with FastAPI, HTMX, TailwindCSS, DaisyUI, Jinja, and MongoDB.

## Goal

Create an extensive example project that integrates the following technologies:

- `FastAPI` as the backend application framework.
- `HTMX` for frontend interactivity (**no JavaScript**, **no npm** required).
- _TailwindCSS_ and _DaisyUI_ for styling.
- `Jinja2` for templating.
- Async _MongoDB_ with vanilla `Pydantic` for data persistence.

Among others, the project showcases the following topics:

- `FastAPI` and `HTMX` integration using [`FastHX`](https://volfpeter.github.io/fasthx/).
- _TailwindCSS_ and _DaisyUI_ integration into a Python and `Jinja2` project without `npm`.
- Async MongoDB usage with vanilla `Pydantic` and [`motorhead`](https://volfpeter.github.io/motorhead/).
- Single-command local development with `honcho`.
- Using JSON instead of form data between the client and the server ([`json-enc` HTMX extension](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/json-enc/README.md)), so `Pydantic` models can be used in `FastAPI` routes.
- Dynamic dialogs with `HTMX` and _DaisyUI_ that are removed from the DOM when closed.
- Lazy-loaded tables for faster initial page loading.
- Active search and filtering.
- Server-sent event streaming with `sse_starlette`, and client-side listening and dynamic UI updates with `HTMX` and its [`sse` extension](https://github.com/bigskysoftware/htmx-extensions/blob/main/src/sse/README.md).
- Custom server-side `HTMX` triggers using response headers with `FastHX` for automatic UI updates.

Non-goals and caveats:

- Design, styling, and responsiveness (well, dashboard-like applications rarely work on small screens anyway).
- Testing: the backend code is very basic and uses standard tools, the main thing that should be tested is the frontend and its interactivity, but that's for a `selenium` tutorial project.
- Full production readiness, see [this section](#Note-on-TailwindCSS-and-DaisyUI) for more information.

## Getting started

The following developer tools must be available:

- Python (^3.11)
- Docker
- Poetry
- Honcho

The project's dependencies can be installed with `poetry install`.

The following `poethepoet` tasks are defined in the project:

- `start`: Starts the FastAPI backend with `uvicorn`.
- `build-css`: Starts a process that watches `.html` and `.jinja` files and rebuilds the application's TailwindCSS file if necessary.
- `build-prod-css`: Builds the minified, production TailwindCSS file of the application.
- `check-format`: Executes the `ruff` format check.
- `format`: Reformats the codebase with `ruff`.
- `lint`: Executes the `ruff` linter.
- `lint-fix`: Fixes linter errors with `ruff`.
- `mypy`: Executes the `mypy` static code analysis with the project's own configuration.
- `static-checks`: Executes all static checks (linting, formatting, type checking) in sequence.
- `test`: Runs the test suite of the project.

These tasks can be executed with `poetry run poe <task>`.

## Running the project

Just execute `honcho start` in the root directory. The command will spin up three processes:

- `database`: An empty MongoDB instance (using `docker`) available on the default MongoDB port (`27017`) in the host system. In case you have a MongoDB running on you host system, please change the port mapping and update the database connection string accordingly in `app/database.py`.
- `css-builder`: The `build-css` task to make sure the tailwind CSS file of the project is always up to date during development.
- `backend`: The FastAPI application.

The application will be available at `http://127.0.0.1:10001/` (the port is configurable in `.uvicorn.env`).

When started with `honcho start`, the application will create some demo data. To prevent it from doing so, remove the `CREATE_DEMO_DATA=true` part from the `Procfile`'s `backend` process definition.

## Development

Use `ruff` for linting and formatting, `mypy` for static code analysis, `pytest` for testing, and `poethepoet` as the task runner.

As mentioned above, use `honcho start` to start the project, it automatically watches code changes and regenerates or restarts whatever is necessary for a convenient developer experience.

# Contributing

All contributions and enhancements are welcome.

## Note on TailwindCSS and DaisyUI

While TailwindCSS doesn't require `npm`, getting plugins (e.g. DaisyUI) working does. In order to work around this limitation, this project loads the full, minified DaisyUI stylesheet from a CDN, which is quite bad for performance. Production applications should use `npm` and configure TailwindCSS and the DaisyUI plugins as if it was a JavaScript project.

## License - MIT

The project is open-sourced under the conditions of the [MIT license](https://choosealicense.com/licenses/mit/).
