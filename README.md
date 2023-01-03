# example-scripts
This repository contains some examples of my scripting work for potential employers. Not included are my Node.js scripts for testing automation which are property of my employer.

A description of the scripts contained in this repository are as follows:

## [bible_contract.py](bible_contract.py):
This script allows the user to select any Bible verse or contiguous group of Bible verses via the [getbible.net](https://getbible.net) V2 API and then returns a .txt file with the selected verses in any desired version, along with a word count. I developed this resource as a way of calculating by-the-word translations. It also includes a short option at the end which will generate a .tex file, with the assumption that the text is in Hebrew, and will add the words into LaTeX code using a modified version of the [expex](https://ctan.org/pkg/expex?lang=en) package that can then be used for interlinear document formatting.

## [skyrim_script.py](skyrim_script.py):
This script is a simple startup application that alerts the user to the fact that a new version of the Skyrim mod SKSE is now available using the [NexusMods API](https://app.swaggerhub.com/apis-docs/NexusMods/nexus-mods_public_api_params_in_form_data/1.0#/).

