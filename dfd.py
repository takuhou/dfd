from PIL import Image
import numpy as np
import cv2

class Dfd:
  def __init__(self, target, depth, position, dimension):
    self.position = position
    self.dimension = dimension
    self.origin = cv2.imread(target,1)
    self.origin_ycrcb = cv2.cvtColor(self.origin, cv2.COLOR_BGR2YCR_CB)

    self.depthmap = cv2.imread(depth,1)
    self.depthmap_ycrcb = cv2.cvtColor(self.depthmap, cv2.COLOR_BGR2YCR_CB)

    if len(self.depthmap.shape) == 3:
      height, width, channels = self.depthmap.shape[:3]
    else:
      height, width = self.depthmap.shape[:2]
      channels = 1

    self.mesh = np.zeros((height, width), np.uint8)

    min_color_per_row = np.min(self.depthmap_ycrcb, axis=0)
    min_color = np.min(min_color_per_row, axis=0)
    min_color = np.uint8(min_color)
    self.y_min = min_color[0]

    max_color_per_row = np.max(self.depthmap_ycrcb, axis=0)
    max_color = np.max(max_color_per_row, axis=0)
    max_color = np.uint8(max_color)
    self.y_max = max_color[0]

    y_range_unit = (self.y_max - self.y_min) / dimension
    self.y_range = []

    for num in range(self.dimension):
      if num == self.dimension-1:
        self.y_range.append(self.y_max)
      else:
        self.y_range.append(self.y_min+(y_range_unit*(num+1)))

    i = 0
    for col in self.depthmap:
      j = 0
      for row in col:
        y = (0.299*row[0]) + (0.587*row[1]) + (0.114*row[2])  
        for num in range(self.dimension):
          if y <= self.y_range[num]:
            self.mesh[i,j] = num
            break;
        j = j + 1
      i = i + 1

    self.output = []
    for num in range(self.dimension):
      self.output.append(np.zeros((height, width, 3), np.uint8))

  def separate(self):
    i = 0
    for col in self.origin:
      j = 0
      for row in col:
        ratio = self.mesh[i,j]
        for num in range(self.dimension):
          if ratio <= num:
            self.output[num][i,j] = [row[0],row[1],row[2]]
            break;
        j = j + 1
      i = i + 1

  def set_gamma(self):
    self.gamma = [];
    gamma_unit = 2*1.0/self.dimension
    for num in range(self.dimension):
      if self.position == 0:
        if num == 0:
          self.gamma.append(2.0);
        else:
          self.gamma.append(2-gamma_unit*num);
      elif self.position == 1:
        if num == 0:
          self.gamma.append(0.2);
        else:
          self.gamma.append(gamma_unit*num);

  def set_lookuptable(self):
    self.look_up_table = [];
    for num in range(self.dimension):
      self.look_up_table.append(np.ones((256, 1), dtype = 'uint8' ) * 0)
      for i in range(256):
        self.look_up_table[num][i][0] = 255 * pow(float(i) / 255, 1.0 / self.gamma[num])

  def write_image(self):
    for num in range(self.dimension):
      cv2.imwrite("out/"+str(num)+".png", cv2.LUT(self.output[num], self.look_up_table[num]));

  def transparent(self):
    output = []
    for num in range(self.dimension):
      origin = 'out/'+str(num)+'.png'
      output.append(Image.open(origin).convert('RGBA'))
      output[num].save(origin)
      output[num] = cv2.imread(origin, cv2.IMREAD_UNCHANGED)
      i = 0
      for col in output[num]:
        j = 0
        for row in col:
          color = int(row[0])+int(row[1])+int(row[2])
          if color == 0:
            row[3] = 0
          j = j + 1
        i = i + 1

      if num == 1:
        self.back = cv2.addWeighted(output[num-1], 1.0, output[num], 1.0, 1.0)
      elif num > 1:
        self.back = cv2.addWeighted(self.back, 1.0, output[num], 1.0, 1.0)

    i = 0
    for col in self.back:
      j = 0
      for row in col:
        if row[3] < 255:
          row[3] = 255
        j = j + 1
      i = i + 1
    if self.position == 0:
      back = 'out/front.png'
    elif self.position == 1:
      back = 'out/back.png'
    cv2.imwrite(back, self.back);

dfd_front = Dfd('rgb.jpg','depth.jpg',0,20)
dfd_front.separate()
dfd_front.set_gamma()
dfd_front.set_lookuptable()
dfd_front.write_image()
dfd_front.transparent()

dfd_back = Dfd('rgb.jpg','depth.jpg',1,20)
dfd_back.separate()
dfd_back.set_gamma()
dfd_back.set_lookuptable()
dfd_back.write_image()
dfd_back.transparent()
