# Modified from https://github.com/openai/gym/blob/master/gym/envs/toy_text/taxi.py

# The taxi environment was adapted in order to solve the autonomous vehicle in a parking lot problem proposed by Rishal Hurbans in his book Artificial Intelligence Algorithms, 2020, ISBN 9781617296185.


import sys
from io import StringIO
from gym import utils
from gym_parking_lot.envs import discrete
import numpy as np
from contextlib import closing

MAP = [
    "+-------------------+",
    "| :c:c:c: :c: : :c: |",
    "| :p: : : : : :p: :p|",
    "| :c:c: :c:c: : : :c|",
    "| : : : : : :c:c: :c|",
    "|c:p:p:c: :p: : : : |",
    "| : : :c: : :c:c:c: |",
    "| :c:c:c:p: :c:c:p: |",
    "| : : :p:c: :p: : : |",
    "|c:p: : : : : : : :c|",
    "|p:c: :c:c:f: :c: :p|",
    "+-------------------+",
]


class ParkingLotEnv(discrete.DiscreteEnv):

  metadata = {"render.modes": ["human", "ansi"]}
  
  def __init__(self):
    
    #  Descrição do mapa usado para avaliação de posição
    self.desc = np.asarray(MAP, dtype="c")

    states = 100
    rows = 10
    columns = 10
    row_limit = rows - 1
    col_limit = columns - 1
    states_arr = np.zeros(states) 
    actions = 4

    P = {
        state: {action: [] for action in range(actions)}
        for state in range(states)
    }

    for row in range(rows):
      for col in range(columns):
        # Codificar novo estado de lote 
        state = self.encode(row, col)
        if self.desc[1 + row, 2 * col + 1] != b"f": # Não atropelou a Vanessa
          states_arr[state] += 1
        for action in range(actions):
          # defaults
          new_row, new_col= row, col
          done = False

          # Sul
          if action == 0:
              new_row = min(row + 1, row_limit)

          # Norte
          if action == 1:
              new_row = max(row - 1, 0)

          # Leste
          if action == 2:
              new_col = min(col + 1, col_limit)

          # Oeste
          if action == 3:
              new_col = max(col - 1, 0)

          if self.desc[1 + new_row, 2 * new_col + 1] == b"c": # Bater em um carro
            reward = -100
          elif self.desc[1 + new_row, 2 * new_col + 1] == b"p": # Bater em uma pessoa
            reward = -1000
          elif self.desc[1 + new_row, 2 * new_col + 1] == b"f": # Chegou
            reward = 500
            done = True
          else:
            reward = 100 # Blocos vazios

          new_state = self.encode(new_row, new_col)

          P[state][action].append((1.0, new_state, reward, done))

    states_arr /= states_arr.sum()
    discrete.DiscreteEnv.__init__(
        self, states, actions, P, states_arr
    )


  def encode(self, car_row, car_col):
      i = car_row
      i *= 10
      i += car_col
      return i

  def decode(self, i):
        out = []
        out.append(i % 10)
        i = i // 10
        out.append(i)
        assert 0 <= i < 10
        return reversed(out)

  def render(self, mode="human"):
      outfile = StringIO() if mode == "ansi" else sys.stdout

      out = self.desc.copy().tolist()
      out = [[c.decode("utf-8") for c in line] for line in out]
      car_row, car_col = self.decode(self.s)

      def ul(x):
          return "_" if x == " " else x

      if self.desc[1 + car_row, 2 * car_col + 1] != b"f":
          out[1 + car_row][2 * car_col + 1] = utils.colorize(
              out[1 + car_row][2 * car_col + 1], "red", highlight=True
          )
      else:  # Arrived
          out[1 + car_row][2 * car_col + 1] = utils.colorize(
              ul(out[1 + car_row][2 * car_col + 1]), "green", highlight=True
          )

      outfile.write("\n".join(["".join(row) for row in out]) + "\n")
      
      if self.lastaction is not None:
          outfile.write(
              f"  ({['Sul', 'Norte', 'Leste', 'Oeste'][self.lastaction]})\n"
          )
      else:
          outfile.write("\n")

      if mode != "human":
          with closing(outfile):
              return outfile.getvalue()