# Fluent Automation Tool

## Overview

This project is a Python-based automation tool for running complete Ansys Fluent simulations, designed using object-oriented programming principles. It automates the full pipeline — from geometry import and meshing to solver setup and post-processing — with minimal manual input.

---
## Environment and Dependencies

This project was developed and tested with the following software versions:

- **ANSYS Fluent**: 2025 R1 (Student Edition)
- **PyFluent**: `ansys-fluent-core==0.30.3`  
- **Python**: 3.11.3  
- **Operating System**: Windows 11
---
## Why This Project

Traditional simulation workflows in Ansys Fluent are GUI-driven and time-consuming. This tool replaces repetitive tasks with clean, modular Python code that improves:

- **Productivity** through full automation  
- **Reproducibility** by eliminating manual clicks  
- **Code quality** via object-oriented structure and separation of concerns

It reflects a strong combination of engineering domain knowledge and modern software development practices.

---

## Features

- Geometry import using PyFluent API  
- Automated watertight meshing workflow  
- Solver setup with fluid properties, inlet conditions, and gravity  
- Post-processing automation: contour plots, vector plots, and plane slices  
- Clean OOP structure with reusable, readable classes

---

## Setup & Requirements

## Setup Instructions (Windows 11)

It is recommended to use a Python virtual environment to keep dependencies isolated and organized.

### Step 1: Create a Virtual Environment

Open a terminal (Command Prompt or PowerShell) and run:

```bash
python -m venv pyfluent-env
```
### Step 2: Activate the Environment

Open a terminal (Command Prompt or PowerShell) and run:

```bash
python -m venv pyfluent-env
.\pyfluent-env\Scripts\activate
```
You should see the environment name ((pyfluent-env)) appear at the beginning of your terminal prompt.


### Step 3: Install Dependencies

Make sure you have a working Fluent installation and Python environment with `ansys.fluent.core`:

#### 1. install ansys-fluent-core

```bash
pip install ansys-fluent-core
```
#### 2. Directory Structure

fluent-automation-tool/
geometry/
Static Mixer geometry.dsco
velocity.png
temperature.png
...
main.py
README.md


#### 3. Run the Script

Inside your virtual environment:

```bash
py .\fluent_automation.py
```