# StabiHacks

Fork of https://github.com/elektrobohemian/StabiHacks with a few adjustments.

Various utilities to deal with metadata and content provided by the Berlin State Library/Staatsbibliothek zu Berlin

The scripts work together as illustrated below:

![general workflow between SBBget, OAI-Analyzer, and Fulltext statistics](./img/general_workflow.png)

## SBBget
* a [Python script](sbbget/sbbget.py) that is capable of downloading digitized media, the associated metadata, and its fulltext from Berlin State Library's digitized collections. 
* it also extracts images that have been detected by the OCR and stores them in the desired file format, e.g., JPEG
* the extracted illustrations can also be stored as .tar files to facilitate distribution
* its logic is based on the more or less unique PPN identifier used at the Berlin State Library.
* some PPN lists are shipped for demonstration purposes. more can be obtained at the Berlin State Library or the creator of the script.
* the script will create various folders below its current working directory, e.g.,
    * downloads (fulltexts, original digitizations etc.) are stored at: sbbget_downloads/download_temp/<PPN>
    * extracted images are stored at: sbbget_downloads/extracted_images/<PPN>
    * METS/MODS files are stored at: sbbget_downloads/download_temp/<PPN>/__metsmods/

### First Run
* the script comes pre-configured and tries to download an existing book from the Berlin State Library if run directly (no parameters needed)
* the script has been tested with Python 3.9 and 3.11 but should run with other versions as well

### Configuration

* the script can be configured by modifying the accompanying [YAML configuration file](sbbget/config.yaml)
### Sample Data

* the script comes with some sample collection that are described [here](ppn_lists/README.md)


## OAI-Analyzer
* a [Python script](oai-analyzer/oai-analyzer.py) that downloads METS/MODS files and DC metadata via OAI-PMH and analyzes them, e.g., to save ALTO XML URLs for certain records or to save metadata such as language codes or authorships
* the results of the analyses are saved locally for further processing in various formats, e.g. Excel and CSV

## Fulltext Analysis
* a [Python script](fulltext-tools/fulltext_analysis.py) that retrieves all fulltexts from a SBBget created download directory and converts all files to raw text files
* additionally, the script runs a NER on all created raw text files and saves the results, the NER is based on [flair](https://github.com/flairNLP)
* for best (i.e. fast) results you should use a GPU but the script will also run on the CPU
* alternatively the script can operate on the result file created by OAI-Analyzer and download ALTO files directly, from this perspective it serves as a Stabi fulltext corpus builder

### First Run

* the script is based on [NLTK](http://www.nltk.org) which needs additional installation steps, i.e.:
    * install NLTK in your Python environment
    * when running the script, Python will ask you to install additional NLTK packages, the easiest way is to open a Python interpreter
    and run to launch NLTK's graphical installer or to download the needed data via:
    ```
    import nltk
    nltk.download('punkt')
    ```
    * usually, NLTK will inform you about missing data if you forgot this step
    * further information can be found an [online book](http://www.nltk.org/book) that also gives an introduction into natural language processing
* the script comes pre-configured and can be launched after [SBBget](sbbget/sbbget.py) has run (no additional parameters are needed, the script looks for the SBBget download folder at the standard location)
* the script has been tested with Python 3.9 and 3.11 but should run with other versions as well
### Future Improvements

* [ner_analysis](fulltext-tools/ner_analysis.py) is based on the results from [fulltext_analysis](fulltext-tools/fulltext_analysis.py) and creates graph data etc. 
* this script is still under development
## Pica Plus

* a [Python script](pica_plus/processPicaPlus.py) that parses files in the Pica+ format as provided by the [GBV](https://www.gbv.de)
* the script lets you choose interesting fields (as stored in the _fieldsOfInterest_ list) and will output the contained data
* records will be separated by a *NEW_RECORD* string on command line or by an empty line in the text format
* output can be saved in text format, separated by the language of the record
* standard fields are:
    * title
    * author (+ optional GND ID)
    * country of publication (only the first entry in a specific extension of the [DIN ISO 3166 format](https://www.dnb.de/SharedDocs/Downloads/DE/DNB/standardisierung/inhaltserschliessung/laenderCodesSyst.pdf?__blob=publicationFile)) 
    * publisher and place of publication


* documentation of the Pica Plus format is only available in German here:
    * [general overview](https://www.gbv.de/bibliotheken/verbundbibliotheken/02Verbund/01Erschliessung/02Richtlinien/01KatRicht/inhalt.shtml)
    * [list of fields](https://www.gbv.de/bibliotheken/verbundbibliotheken/02Verbund/01Erschliessung/02Richtlinien/01KatRicht/pica3.pdf)

