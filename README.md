# City of Henderson Swim Slot Scalper Bot

Automates purchasing of City of Henderson pools' swim lane reservations upon release to public

## Prequisites

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Selenium.

```bash
pip install selenium
```

Must also install 'geckodriver' from Selenium website for proper browser interaction, [download here.](https://selenium-python.readthedocs.io/installation.html)

## Features

* Reserves swim lane reservations, one lane and swimmer at a time per instance
* If wanted swim slot is unavailable, will idle and refresh until available
* Texts user confirmation of lane reservations, as seen here ![automated like clockwork](https://i.imgur.com/IFd47qX.jpg)

## A collapsible section with markdown
<details>
  <summary>Click to expand!</summary>
![automated like clockwork](https://i.imgur.com/IFd47qX.jpg)
</details>

## Usage

1. Install Selenium package and respective browser driver
2. Fill in all variables marked with 'X' in SwimSlotScalper.py with info requested
3. Run from terminal or inside IDE
