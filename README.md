# cintel-06-custom

## Running locally:
In terminal, navigate to the project directory and run:
``` shiny run --reload --launch-browser penguins/app.py ```
## Build the App to Docs Folder and Test Locally
With your project virtual environment active in the terminal and the necessary packages installed, remove any existing assets and use shinylive export to build the app in the penguins folder to the docs folder:
```
shiny static-assets remove
shinylive export penguins docs
```
