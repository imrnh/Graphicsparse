from ultralytics import YOLO

def tfgcInference(image_path, model_path):
    model = YOLO(model_path, verbose=False).to(device="cuda")
    inf_res = model(image_path)

    boxes_list = []
    res_box_list = inf_res[0].boxes.xyxy
    for bx in res_box_list:
        boxes_list.append(bx)
    
    return [boxes_list, image_path]

class YOLOInferenceManager():
    def __init__(self, model_path) -> None:
        self.Model = YOLO(model_path, verbose=False).to(device='cpu')
        self.model_path = model_path

    def inference(self, image_path):
        inf_res = self.Model(image_path)

        boxes_list = []
        res_box_list = inf_res[0].boxes.xyxy
        for bx in res_box_list:
            boxes_list.append(bx)
        
        return [boxes_list, image_path]


    def delete_model(self):
        self.Model.cpu()
        del self.Model



# if __name__ == "__main__":
#     from PIL import Image
    
#     yi = YOLOInferenceManager("lib/tfgc_models/tfgc_v1.pt")
#     img = Image.open("tmp/raw_images/8.jpg")    
#     args = [img, "8.jpg"]
#     print(yi.inference(args))
