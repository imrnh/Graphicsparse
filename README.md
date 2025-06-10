The following repository contains code to extract `Table`, `Figure` etc from given image. One `Yolo-V9c` model was trained to detect figures and another `Yolo-v8l` model was trained to detect tables from the pdf.
Initially, a pdf file will be seperated into pages. You can specify if you want to remove the figure or table from that pdf pages or not. 

### About training
We made a dataset of one thousand research papers and extracted and labeled them manually. The models are then trained on that data. 
