# Typeracer Autotyper

A bot that automates inputs for [typeracer.com](https://typeracer.com).\
The bot works by taking the screenshot of a small portion of the screen where the text may be, converting the image to text using `opencv-python` and `pytesseract`.

The [Tesseract](https://tesseract-ocr.github.io/tessdoc/Downloads.html) OCR should be installed on the system prior to using the program, as it depends on the tesseract OCR engine.

Make sure that the starting border of the leaderboard table under the typing box is 1cm / 39 pixels from the bottom of the screen. 

There are two phases:
- To grab the screenshot.
- To start typing the converted text.

Both the phases can be triggered using the `right control` key.

The program also takes optional arguments. Do `python autotyper.py -h` to see the list of arguments.

### This program works only on windows machines.

## Required modules

```bash
python -m pip install -r requirements.txt
```

## License
[autotyper](https://github.com/0xcabrex/autotyper) is licensed under the MIT License as stated in the [LICENSE](https://github.com/0xcabrex/autotyper/blob/master/LICENSE) file.