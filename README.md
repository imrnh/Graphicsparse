# Graphicsparse

## Overview

This repository contains code to extract graphical elements such as **Tables** and **Figures** from images of PDF pages. The extraction pipeline leverages two specialized YOLO models:

- A **YOLO-v9c** model trained specifically to detect **figures**.
- A **YOLO-v8l** model trained specifically to detect **tables**.

The input PDF file is first split into individual pages (images), and then the models detect the graphical elements. Users have the option to specify whether they want to remove the detected figures or tables from the PDF pages.

---

## Features

- Splits PDF documents into page images for processing.
- Detects figures and tables on each page using dedicated YOLO models.
- Allows selective removal of figures or tables from PDF pages.
- Supports customization to keep or remove specific graphical elements.

---

## Training Data

To train the detection models, we compiled a dataset from **one thousand research papers**. Figures and tables were manually extracted and labeled to create high-quality training data. Both YOLO-v9c (for figures) and YOLO-v8l (for tables) models were trained extensively on this dataset to achieve accurate detection.

---

## Performance and Hardware Requirements

- The models can be efficiently run on a GPU equivalent to or greater than an NVIDIA Tesla T4.
- For an image sized approximately **1000×700 pixels**, inference time is approximately **1 second on a Tesla T4 GPU**.
- On a CPU, the same inference takes approximately **10 seconds**.

---

## Usage

1. Provide a PDF file as input.
2. The tool splits the PDF into page images.
3. The models detect tables and figures on each page.
4. Specify if you want to remove figures, tables, or keep all.
5. Processed pages can be saved or exported as needed.

---

## Requirements

- Python 3.x  
- PyTorch  
- YOLOv8 and YOLOv9 dependencies  
- Other image processing libraries (e.g., OpenCV, PIL)  

---

## License

[Specify your license here]

---

## Acknowledgements

- YOLO team for the object detection framework.
- Dataset contributors and annotators.

---

For any questions or contributions, feel free to open an issue or submit a pull request.

`I've originally made that for my side-project echoscript.` 
