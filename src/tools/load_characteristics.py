def load_characteristics():
  characteristics = []
  with open('./data/topics.txt', "r") as f:
    for line in f:
      line = line.strip()
      characteristics.append(line)

  return characteristics