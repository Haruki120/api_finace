import cv2
import matplotlib.pyplot as plt
# %matplotlib inline
import matplotlib
import os
import io

from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ocr-test-317005-43180e2ec119.json"

client = vision.ImageAnnotatorClient()
with io.open("image.jpg", 'rb') as image_file:
    content = image_file.read()
image = vision.Image(content=content)
response = client.document_text_detection(image=image)


# document = response.full_text_annotation
# for page in document.pages:
#     for block in page.blocks:
#         for paragraph in block.paragraphs:
#             for word in paragraph.words:
#                 box = [(v.x, v.y) for v in word.bounding_box.vertices]
#                 text = []
#                 for symbol in word.symbols:
#                     text.append(symbol.text)
#                 print(box, ''.join(text))
    

def get_sorted_lines(response):
    document = response.full_text_annotation
    bounds = []
    for page in document.pages:
      for block in page.blocks:
        for paragraph in block.paragraphs:
          for word in paragraph.words:
            for symbol in word.symbols:
              x = symbol.bounding_box.vertices[0].x
              y = symbol.bounding_box.vertices[0].y
              text = symbol.text
              bounds.append([x, y, text, symbol.bounding_box])
    # print(bounds)
    bounds.sort(key=lambda x: x[1])
    old_y = -1
    line = []
    lines = []
    threshold = 1
    for bound in bounds:
      x = bound[0]
      y = bound[1]
      if old_y == -1:
        old_y = y
      elif old_y-threshold <= y <= old_y+threshold:
        old_y = y
      else:
        old_y = -1
        line.sort(key=lambda x: x[0])
        lines.append(line)
        line = []
      line.append(bound)
    line.sort(key=lambda x: x[0])
    lines.append(line)
    return lines

img = cv2.imread("image.jpg", cv2.IMREAD_COLOR)

lines = get_sorted_lines(response)
for line in lines:
  texts = [i[2] for i in line]
  texts = ''.join(texts)
  bounds = [i[3] for i in line]
  print(texts)
 

plt.figure(figsize=[10,10])
plt.axis('off')
plt.imshow(img[:,:,::-1]);plt.title("img_by_line")


# if __name__ == '__main__':
#     get_sorted_lines(response)