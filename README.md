# Routes generator
[![Main Check](https://github.com/jespy666/Routes_KAS/actions/workflows/checked.yml/badge.svg)](https://github.com/jespy666/Routes_KAS/actions/workflows/checked.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/ef8008e49e66c8476096/maintainability)](https://codeclimate.com/github/jespy666/Routes_KAS/maintainability)



<p align="left">
   <img src="https://img.shields.io/badge/python-v3.10-blue" alt="Python Version">
   <img src="https://img.shields.io/badge/APP-v0.0.1(stable)-green" alt="APP Version">
   <img src="https://img.shields.io/badge/License-MIT-purple" alt="License">
</p>

## About
The utility is designed for employees of the company "KIRISHIAVTOSERVIS" generating routes for company vehicles based on user-provided data for each day. The utility aims to reduce working time spent on routine distance calculations and matching searches. It streamlines the process of route planning by automating the calculation of distances and finding suitable matches. This not only enhances efficiency but also eliminates the need for manual route optimization. By utilizing this utility, employees can focus more on their core tasks while ensuring optimized travel routes for the company's vehicles.

## Stack
- <img src="https://img.shields.io/badge/python%203.10-blue" alt="Python">  
- <img src="https://img.shields.io/badge/poetry-green" alt="Poetry">
- <img src="https://img.shields.io/badge/PyTest-red" alt="PyTest">

## Documentation

1. Compile
    - Compile into .exe file. Here's an example of installation using auto-py-to-exe:  
`auto-py-to-exe start_window.py`(being in kas/windows)
    - Or direct command: `pyinstaller --noconfirm --onefile --windowed --collect-all "kas" --hidden-import "fpdf"  "your/path/to/project/start_window.py"`
2. Uses
    - Open the compiled application. Example to fill main window:
      <p align="center">
      <img src="https://i.ibb.co.com/KWfRTjQ/example-main.jpg" alt="main_window">
      </p>
    - Click on the save button, the button to open the days window will become available:
      <p align="center">
      <img src="https://i.ibb.co.com/qyLH0Z7/days-button.jpg" alt="days button">
      </p>
    - Opened Day's window:
      <p align="center">
      <img src="https://i.ibb.co.com/cxd71dG/days-window.jpg" alt="days window">
      </p>
    - Open current day. Example to fill day:
      <p align="center">
      <img src="https://i.ibb.co.com/GFTJpGR/current-day.jpg" alt="current day">
      </p>
    - If entry data was correct, the day that was filled will turn green:
      <p align="center">
      <img src="https://i.ibb.co.com/KK0Yvrx/succeed-fill.jpg" alt="green light">
      </p>
    - After filling in all the days, press the confirm button:
      <p align="center">
      <img src="https://i.ibb.co.com/yPRpmS1/confirm-buttoon.jpg" alt="confirm button">
      </p>
    - After all, button `write to pdf` will become aviable:
      <p align="center">
      <img src="https://i.ibb.co.com/ZmVx5n3/write-button.jpg" alt="write button">
      </p>
    - Get your `output.pdf` file in the directory where the .exe file is located

## Distribute

- https://github.com/jespy666/Routes_KAS


## Developers

- https://github.com/jespy666

## License
Project Routes Generator is distributed under the MIT License
