# Higor Viana, Josué Batista & Ygor Kaique

# Uses the custom pip package gym-parking_lot at: https://github.com/breurlucas/gym-parking_lot

# Resources for the Q-learning section: https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/

# Com a ajuda do Grupo Beatriz Paiva e Lucas Breur

# Com base no artigo de S. Kansal e B. Martin: https://colab.research.google.com/drive/1VTT05l8qjHJJtoliMJ4mjcvVWe-BaYag


import gym
import sys, os, time
import numpy as np
import random

# animacao
def animacao(frames):
    clear_console = 'clear' if os.name == 'posix' else 'CLS'

    while True:
        for frame in frames:
            # Write the current frame on stdout and sleep
            sys.stdout.write(frame)
            sys.stdout.flush()
            time.sleep(1)
        break

env = gym.make("gym_parking_lot:parking_lot-v0").env # Começa no estado inicial (Ponto onde o carro fica)


q_table = np.zeros([env.observation_space.n, env.action_space.n]) # Inicialização com a tabela de valores Q

# Hiperparâmetros
alpha = 0.1 # taxa de aprendizagem
gamma = 0.6 # fator de desconto
epsilon = 0.1 # chance de escolha aleatória  

frames = []


for i in range(1, 100001): # Vai rodar 100000 diferentes versões do problema

    estado = env.reset() # Inicialização aleatoria do ambient
    recompensa = 0
    acabou = False
    
    while not acabou:
        if random.uniform(0, 1) < epsilon:
            acao = env.action_space.sample() # Escolhe ação aleatoriamente
        else:
            acao = np.argmax(q_table[estado])  # Escolhe ação com base no que já aprendeu

        prox_estado, recompensa, acabou, info = env.step(acao) # Aplica a ação
        
        outro_valor = q_table[estado, acao] # Valor da ação escolhida no estado atual
        prox_max = np.max(q_table[prox_estado]) # Melhor valor no próximo estado
        
        # Atualize o valor Q usando a fórmula principal do Q-Learning
        novo_valor = (1 - alpha) * outro_valor + alpha * (recompensa + gamma * prox_max)
        q_table[estado, acao] = novo_valor

        estado = prox_estado

        if i == 100000:
            frames.append(env.render(mode='ansi'))

print("Treinamento finalizado.\n")
animacao(frames)