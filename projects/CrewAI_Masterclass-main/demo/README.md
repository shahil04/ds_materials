# Demo Crew

Welcome to the Demo Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

## Quick Start Visual Reference
For a visual guide to the demo setup and run process, see `steps.md`. The images below show the main setup and execution steps for the demo.

- `img/img1_code.png`: Code setup and project structure
- `img/img2_run.png`: Running the demo with `crewai run`
- `img/img3_process.png`: Agent process and task flow
- `img/img4_result.png`: Generated output and results
- `img/img5_final.png`: Final demo summary and verification

![Code setup](img/img1_code.png)

![Run demo](img/img2_run.png)

![Process flow](img/img3_process.png)

![Result example](img/img4_result.png)

![Final summary](img/img5_final.png)

This gallery illustrates the main commands and workflow steps referenced in `steps.md`.

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/demo/config/agents.yaml` to define your agents
- Modify `src/demo/config/tasks.yaml` to define your tasks
- Modify `src/demo/crew.py` to add your own logic, tools and specific args
- Modify `src/demo/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the demo Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The demo Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the Demo Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
