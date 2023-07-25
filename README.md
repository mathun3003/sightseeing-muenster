# Sightseeing Münster App

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)  
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)

---

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sightseeingmuenster.streamlit.app/)

## Description

Find information on Münster sights with just one photo! 

The following sights are currently supported:
- Aasee Münster
- St. Paulus Dom MÜnster
- Erbdrostenhof Münster
- LWL-Museum für Kunst und Kultur Münster
- Schloss Münster
- St. Lamberti Münster
- Rathaus Münster
- Hafen Münster

App users can either take a photo of one of the supported sights or upload a photo from their device. Then, with that photo, the app classifies the photo and the corresponding tourist information is queried from the [Open Data Portal Münsterland](https://www.muensterland.com/muensterland-e.v/unsere-projekte/muensterland-digital/datenportal-muensterland/). The information is displayed to the user at a glance and is available in German, English, and Dutch.

The app was implemented with [Streamlit](https://docs.streamlit.io/). A pre-trained EfficientNetV2S was fine-tuned using [PyTorch](https://www.pytorch.org/) on scraped images from Bing Search. The model was trained on images of various sights from Münster with a very good performance (>90% accuracy) using GPU instances from Google Colab. The tourist information is queried from the API of the [Open Data Portal Münsterland](https://www.muensterland.com/muensterland-e.v/unsere-projekte/muensterland-digital/datenportal-muensterland/), an open database containing data of numerous points of interest.

The Web App is hosted on the community cloud of Streamlit and is available [here](https://sightseeingmuenster.streamlit.app/).

## Installation

Clone the repository and install the required packages with the following command:

```bash
cd to/your/directory
bash setup.sh
```
``setup.sh`` is a custom bash script that handles the installation of dependencies.

## Usage

To run the app, execute the following command:

```bash
bash run_dev.sh
```

``run_dev.sh`` is a custom bash script that handles the execution of the app and is used for development as it refreshes the page when changes occur to any files in the directory.


## Deployment

The app is deployed on the community cloud of Streamlit. All dependencies and the entire code base needs to be on GitHub. The app is then deployed by using the Community Cloud UI of Streamlit. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. For further improvements, please also open an issue.

## License

If you want to use the code, please read the ``LICENSE.md`` file thoroughly.