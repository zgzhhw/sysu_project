import gym
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from torch import nn, optim
import wandb
import matplotlib.pyplot as plt


class QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(QNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) #从输入层到隐藏层
        self.fc2 = nn.Linear(hidden_size, output_size)  #从隐藏层到输出层

    def forward(self, x):
        x = torch.Tensor(x) #转化为tensor张量
        x = F.relu(self.fc1(x)) #激活函数
        x = self.fc2(x) #激活后的数据通过第二个线性层进行线性变换
        return x


class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = []
        self.capacity = capacity

    def len(self):
        return len(self.buffer)

    def push(self, *transition):
        if len(self.buffer) == self.capacity:
            self.buffer.pop(0)
        self.buffer.append(transition)

    def sample(self, n):
        index = np.random.choice(len(self.buffer), n)
        batch = [self.buffer[i] for i in index] #根据选中的索引，从缓存器中获取对应的训练数据，形成一个批次
        return zip(*batch)  #将列表 batch 中的每个元素按照索引转置，相当于将每个训练数据的相同位置的元素组成一个元组

    def clean(self):
        self.buffer.clear()


class DQN:
    def __init__(self, env, input_size, hidden_size, output_size):
        self.env = env
        self.eval_net = QNet(input_size, hidden_size, output_size)
        self.target_net = QNet(input_size, hidden_size, output_size)
        self.optim = optim.Adam(self.eval_net.parameters(), lr=args.lr)
        self.eps = args.eps
        self.buffer = ReplayBuffer(args.capacity)
        self.loss_fn = nn.MSELoss()
        self.learn_step = 0
     
    def choose_action(self, obs):
        # epsilon-greedy
        if np.random.uniform() <= self.eps:
            # 随机选择 [0, self.env.action_space.n) 之间的一个动作
            action = np.random.randint(0, self.env.action_space.n)
        else:
            # 根据观察值 "obs" 使用 "eval_net" 获取一个动作
            obs_tensor = torch.FloatTensor(obs)
            with torch.no_grad():
                q_values = self.eval_net(obs_tensor)
            action = q_values.argmax().item()
        return action

    def store_transition(self, *transition):
        self.buffer.push(*transition)
        
    def learn(self):
        if self.eps > args.eps_min:
            self.eps *= args.eps_decay

        if self.learn_step % args.update_target == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step += 1 
        
        obs, actions, rewards, next_obs, dones = self.buffer.sample(args.batch_size)
        actions = torch.LongTensor(actions)  # 使用 LongTensor 来进行 gather 操作
        dones = torch.FloatTensor(dones)
        rewards = torch.FloatTensor(rewards)

        q_eval = self.eval_net(np.array(obs)).gather(1, actions.unsqueeze(1)).squeeze(1)
        # 使用 eval_net 对观察值 obs 进行前向传播，得到相应的 Q 值
        # np.array(obs) 将观察值转换为 NumPy 数组
        # gather(1, actions.unsqueeze(1)) 选择与 actions 对应的 Q 值
        # squeeze(1) 去除不必要的维度

        q_next = self.target_net(np.array(next_obs)).max(dim=1)[0]
        # 使用 target_net 对下一个观察值 next_obs 进行前向传播，得到最大的 Q 值
        # np.array(next_obs) 将下一个观察值转换为 NumPy 数组
        # torch.max(..., dim=1)[0] 选择沿着第 1 维度（动作）的最大 Q 值

        q_target = rewards + args.gamma * (1 - dones) * q_next
        # 根据贝尔曼方程计算目标 Q 值
        # Q_target = rewards + gamma * (1 - dones) * max(Q_next)

        loss = self.loss_fn(q_eval, q_target)
        # 计算 q_eval 和 q_target 之间的损失，使用损失函数 loss_fn

        self.optim.zero_grad()
        # 清除优化器中的梯度信息

        loss.backward()
        # 反向传播计算梯度

        self.optim.step()
        # 更新网络参数

def plot_avg_rewards(rewards):
    avg_rewards = []
    for i in range(len(rewards)):
        start_idx = max(0, i - 9)
        avg_reward = sum(rewards[start_idx:i+1]) / (i - start_idx + 1)
        avg_rewards.append(avg_reward)
    
    plt.plot(avg_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Average Reward")
    plt.title("Average Reward over Last 10 Episodes")
    plt.show()


def main():
    env = gym.make(args.env)

    o_dim = env.observation_space.shape[0]
    a_dim = env.action_space.n
    agent = DQN(env, o_dim, args.hidden, a_dim) 
    
    rewards = []  # 记录每一轮次的奖励值
    
    for i_episode in range(args.n_episodes):
        obs = env.reset()[0]
        episode_reward = 0
        done = False
        step_cnt = 0
        while not done and step_cnt < 500:
            step_cnt += 1
            action = agent.choose_action(obs)
            next_obs, reward, done, info, _ = env.step(action) 
            agent.store_transition(obs, action, reward, next_obs, done)
            episode_reward += reward
            obs = next_obs
            if agent.buffer.len() >= args.capacity:
                agent.learn()
        rewards.append(episode_reward)
        print(f"Episode: {i_episode}, Reward: {episode_reward}")
        
    if i_episode >= 9:plot_avg_rewards(rewards)

    
        
    # 数据可视化
    plt.plot(rewards)
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("DQN Training")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", default="CartPole-v1", type=str)
    parser.add_argument("--lr", default=1e-3, type=float)
    parser.add_argument("--hidden", default=64, type=int)
    parser.add_argument("--n_episodes", default=500, type=int)
    parser.add_argument("--gamma", default=0.99, type=float)
    parser.add_argument("--log_freq", default=100, type=int)
    parser.add_argument("--capacity", default=5000, type=int)
    parser.add_argument("--eps", default=1.0, type=float)
    parser.add_argument("--eps_min", default=0.05, type=float)
    parser.add_argument("--batch_size", default=300, type=int)
    parser.add_argument("--eps_decay", default=0.999, type=float)
    parser.add_argument("--update_target", default=100, type=int)
    args = parser.parse_args()
    main()
