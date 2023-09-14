# -*- coding: utf-8 -*-
from os import PathLike

import torch
import torchvision
from PIL import Image
from torch import nn
from torchvision import transforms

from utils.constants import MODEL_SAVE_PATH  # pylint: disable=import-error


class EfficientNetV2S(nn.Module):
    """
    Class to create a pretrained EfficientNetV2S model with a custom classifier.
    """

    def __init__(self, fan_out: int = 8, model_path: PathLike = MODEL_SAVE_PATH) -> None:
        """
        Creates a pretrained EfficientNetV2S model with a custom classifier.
        :param fan_out: Number of classes. Defaults to 8.
        :param model_path: Path to the pretrained weights. Defaults to MODEL_SAVE_PATH.
        """
        super().__init__()
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = torchvision.models.efficientnet_v2_s()
        self.model.classifier = torch.nn.Sequential(
            nn.Dropout(p=0.2, inplace=True),
            nn.Linear(in_features=1280, out_features=fan_out, bias=True),
        )
        self.checkpoint = torch.load(model_path, map_location=torch.device(self._device))
        # load model state dict and class dict
        self.model.load_state_dict(self.checkpoint["model_state_dict"])
        self.class_dict = self.checkpoint["class_to_idx"]
        self.class_dict = {v: k for k, v in self.class_dict.items()}

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Function to forward propagate an image through the model.
        :param x: Input tensor.
        :return: Model logits.
        """
        return self.model(x)

    def predict_class_label(self, x: torch.Tensor) -> str:
        """
        Function to predict the class label
        :param x: image as tensor
        :return: label prediction
        """
        self.model.eval()
        with torch.inference_mode():
            # predict class probabilities
            class_probabilities = self._predict(x)
            # get highest likelihood
            prediction = torch.argmax(class_probabilities, dim=1).item()
            # get label
            label = self.class_dict[prediction]
        # return label
        return label

    def _predict(self, x: torch.Tensor) -> torch.Tensor:
        """
        Function to predict the class probabilities.
        :param x: Input tensor.
        :return: class probabilities as tensors.
        """
        return torch.softmax(self.forward(x), dim=1)


def transform(img: Image.Image) -> torch.Tensor:
    """
    Function to transform an image to an EfficientNet compatible tensor.
    :param img: image as pillow image
    :return: transformed image as tensor
    """
    # define image transformations
    transformer = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    # transform image
    img_tensor = transformer(img)
    # add batch dimension
    img_tensor = img_tensor.unsqueeze(dim=0)
    return img_tensor
