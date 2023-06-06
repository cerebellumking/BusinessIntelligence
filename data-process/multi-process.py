import pandas as pd
import argparse

# 多线程操作，单个线程处理一部分数据
# start和end表示的起始行和终止行
# 使用process.sh运行

parser = argparse.ArgumentParser()
parser.add_argument("--start", required=True, type=int)
parser.add_argument("--end", required=True, type=int)
args = parser.parse_args()

# 读取数据
path = "./datatest/single_userid_log.csv"
logdata = pd.read_csv(path)
logdata = logdata[args.start:args.end]

# 创建一个新的DataFrame
from tqdm import tqdm
df = pd.DataFrame(columns=['user_id', 'news_id', 'start_ts', 'duration'])

total_lines = 0
for idx, row in tqdm(logdata.iterrows(), total=len(logdata), ncols=80):
    user_id = int(row['UserID'])
    news_id_list = row['ClicknewsID'].split(' ')
    duration_list = row['dwelltime'].split(' ')
    start_timestamp_list = row['exposure_time'].split(' ')
    total_lines += len(news_id_list)
    # print(f"{user_id}: {len(news_id_list)}")
    for i in range(len(news_id_list)):
        news_id = int(news_id_list[i][1:]) - 10000
        duration_time = int(duration_list[i])
        start_timestamp = int(start_timestamp_list[i])
        df.loc[len(df)] = [user_id, news_id, start_timestamp, duration_time]
# df = df.sort_values('start_ts', ascending=True)
df.to_csv(f"./logcsvs/userid_{args.start}_{args.end}.csv", index=False)