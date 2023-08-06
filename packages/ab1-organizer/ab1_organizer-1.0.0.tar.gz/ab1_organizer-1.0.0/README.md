# ab1_organizer

## Goal

Organize AB1 files by researches and primer-pairs.

## Instalation

For command line usage, simpleously use pip way:

```bash

pip install ab1_organizer

```

## Usage

`ab1_organizer` receive two arguments on initialization: the results file from Macrogen sequencing (-f, --file argument) and the modified order table (-t, --table argument). The sequencing file consists of the raw zipfile (file-name.zip) containing all .ab1, .pdf, phd.1, and .txt files. The order file consists of a simple excel table containing Macrogen order specifications and containing standardized headers (see next section).

### Standardized headers

Your table would contain almost four columns, named respectively:
- sampleName: The unique identifier of sample;
- primerName: The primer name. e.g. "CO3 F", or "ITS1 R";
- personInCharge: The name of a person or a project responsible for the sample processing;
- primerCombination: Underscore separated complementary primer names. As example, if some region are sequenced using the "ITS1-F" and "ITS1-R", the primerCombination would be "ITS1-F_ITS1-R".


At the terminal, run the code:

```bash

ab1_organizer.py -f ./path/to/zip/file -t ./path/to/order/table.xlsx

```

A new folder with the same name of the zip file will be created and all files will be organized by author and genomic marker respectively.


---

Feel free to add new features and contribute through pull requests. Be happy!!
