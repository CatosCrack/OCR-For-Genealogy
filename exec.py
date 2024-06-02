from external_resources import Drive
from recognition import Recognition

rec = Recognition()
drive = Drive()
images = drive.get_drive_files()

for image in images:
    print("................................................")
    print(image)
    id = images[image]
    names = rec.recognitionPipeline(id)
    rec.plot_boxes(id, names)
    # TODO: Add method to upload ID + name data to database