# Sightseeing Münster App

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Find information on Münster sights with just one photo!


![St. Paulus Dom Münster](resources/demo_images/St.%20Paulus%20Dom.jpg)

The app was implemented with [Streamlit](https://docs.streamlit.io/). An EfficientNetV2 was fine-tuned using [TensorFlow](https://www.tensorflow.org/) on scraped images from Bing Search.

The model was trained on images of various sights from Münster with a very good performance (>90% accuracy). Then, its weights were exported and loaded to the model in the web app. The app user can take a photo of any sight the model was trained on. With that photo, the model makes a prediction and outputs the name of the sight as well as some tourist information.

The web app is hosted on GitHub Pages.
