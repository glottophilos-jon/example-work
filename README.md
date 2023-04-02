# Example Work
This repository contains some examples of my scripting work for potential employers. Not included are my Node.js scripts for testing automation which are property of my employer. To see an example of my skills with HTML, CSS, and JavaScript, you can visit my website at [glottophilos.com](https://glottophilos.com).

A description of the scripts contained in this repository are as follows:

## [bible_contract.py](bible_contract.py):
This script allows the user to select any Bible verse or contiguous group of Bible verses via the [getbible.net](https://getbible.net) V2 API and then returns a .txt file with the selected verses in any desired version, along with a word count. I developed this resource as a way of calculating by-the-word translations. It also includes a short option at the end which will generate a .tex file and will add the words into LaTeX code using a modified version of the [expex](https://ctan.org/pkg/expex?lang=en) package that can then be used for interlinear document formatting.

## [skyrim_script.py](skyrim_script.py):
This script is a simple startup application that alerts the user to the fact that a new version of the Skyrim mod SKSE is now available using the [NexusMods API](https://app.swaggerhub.com/apis-docs/NexusMods/nexus-mods_public_api_params_in_form_data/1.0#/).

## [Expexmod](Expexmod):
This folder contains several different LaTeX files which together constitute a modified version of the expex package for linguistics. I have modified the parser slightly to allow for verse numbering which should help to make interlinear translations of poetry and the Bible or other religious texts simpler. My changes are found in lines 1304-1321 of [expexmod.tex](Expexmod/expexmod.tex), and the commands found in [maincommands.tex](Expexmod/maincommands.tex) should be added to your `main.tex` file. Note that the commments in the [maincommands.tex](Expexmod/maincommands.tex) file explain the new nlevel gloss format and the various arguments available.
