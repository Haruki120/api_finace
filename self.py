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
    boxes = []
    for page in document.pages:
      for block in page.blocks:
        for paragraph in block.paragraphs:
          for word in paragraph.words:
                text = []
                for symbol in word.symbols:
                    text.append(symbol.text)
                box = [(v.x, v.y) for v in word.bounding_box.vertices]
                box.append("".join(text))
                boxes.append(box)
    return boxes
    
def average_xy(boxes):
    words = []
    for box in boxes:
        word = []
        xs = [box[0][0],box[1][0],box[2][0],box[3][0]]
        ys = [box[0][1],box[1][1],box[2][1],box[3][1]]
        average_x = sum(xs)/4
        average_y = sum(ys)/4
        word.append(average_x)
        word.append(average_y)
        word.append(box[4])
        words.append(word)
    return words

# どれくらいyの差異を許容するか
gap = 20

def get_lines(words):
    lines = []
    i = 0
    for word in words:
        lines.append([])
        for target in words[:]:
            if gap > abs(word[1] - target[1]):
                lines[i].append(target)
                words.remove(target)
            else:
                pass
        i += 1
    return lines
            
            
                



if __name__ == '__main__':
    boxes = get_sorted_lines(response)
    words = average_xy(boxes)
    lines = get_lines(words)
    print(lines)