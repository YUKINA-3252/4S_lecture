% matplotlib inline
import numpy as np
import math
import matplotlib.pyplot as plt
import random

Num = 5  # picture size is 5 * 5
pattern_num = 6
average = 0
answer_num = 0

data_all = np.zeros((pattern_num, Num * Num))
data_all[0] = [-1, -1, 1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, -1]
data_all[1] = [1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1]
data_all[2] = [-1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1, -1, 1, -1,-1, 1, 1, 1, -1]
data_all[3] = [1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1]
data_all[4] = [1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1]
data_all[5] = [1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1]

class HopfieldNetwork:

  def __init__(self):
    self.w = np.zeros((Num*Num, Num*Num))
    global data_all
    self.data_all = data_all

  def memorize(self, data, num):
    for a in range(num):
      for i, _ in enumerate(data[a]):
        for j, _ in enumerate(data[a]):
          self.w[i][j] += data[a][i] * data[a][j]
    self.w[i][j] /= num
    """
    for i, _ in enumerate(data[0]):
      self.w[i][i] = 0
    """

  def remember(self, test, num):
    #draw(self.data_all[0])
    energy = np.inf
    energy_array = []
    energy_array.append(energy)
    self.nodes = test
    while True:
      #print(self.nodes)
      self.nodes_dash = np.zeros(Num * Num)
      for i, _ in enumerate(self.nodes):
        for j, _ in enumerate(self.nodes):
          self.nodes_dash[i] += self.w[i][j] * self.nodes[j]
        if self.nodes_dash[i] > 0:
          self.nodes[i] = 1
        elif self.nodes_dash[i] < 0:
          self.nodes[i] = -1
        """
        else:
          self.nodes[i] = self.nodes_dash[i]
        """

      new_energy = self.energy_function()
      energy_array.append(new_energy)
      if abs(energy - new_energy) < 0.001:
        # draw graph
        """
        x = np.arange(0, len(energy_array))
        plt.plot(x, energy_array)
        plt.xticks(x)
        plt.show()
        """

        # calculate answer_rate
        distance_array = []
        for i in range(num):
          a = self.data_all[i] - self.nodes
          sum = 0
          for j, _ in enumerate(a):
            sum += abs(a[j])
          distance_array.append(sum / 2)
        global average
        average += Num * Num - np.amin(distance_array)
        if np.amin(distance_array) == 0.0:
          global answer_num
          answer_num += 1

        return
      else:
        energy = new_energy

  def energy_function(self):
    energy = 0
    for i, _ in enumerate(self.nodes):
      for j, _ in enumerate(self.nodes):
        energy += self.w[i][j] * self.nodes[i]* self.nodes[j]
    energy = energy / 2.0 * -1
    return energy

def draw(array_data):
  print("##########")
  for i, _ in enumerate(array_data):
    if array_data[i] == 1:
      print("■", end="")
    else:
      print("□", end="")
    if i % 5 == 4:
      print("\n", end="")
  print("##########")

if __name__ == "__main__":

  data_num = 6
  data_raw = data_all.copy()
  data_raw = data_raw[:data_num, :]

  hn = HopfieldNetwork()

  # memorize
  hn.memorize(data_raw, data_num)

  for i in range(1000):
    #create test_data with 20% noise
    noise_num = int(Num * Num * 1.0)
    noise_index = []

    for i in range(noise_num):
      while True:
        idx = random.randint(0, (Num * Num -1))
        if i == 0:
          noise_index.append(idx)
          break
        else:
          check = 1
          for j in range(len(noise_index)):
            if idx == noise_index[j]:
              check = 0
              break
          if check == 1:
            noise_index.append(idx)
            break
          else:
            continue

    test_idx = random.randint(0, data_num - 1)
    test_data = data_raw.copy()
    test_data = test_data[test_idx, :]
    for i in range(noise_num):
      test_data[noise_index[i]] = test_data[noise_index[i]] * -1

    hn.remember(test_data, data_num)

  answer_rate = answer_num / 1000.0 * 100
  average /= 1000.0
  print(average)
  print(answer_rate)
