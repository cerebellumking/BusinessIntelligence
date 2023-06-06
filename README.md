# 商务智能项目文档

- [商务智能项目文档](#商务智能项目文档)
  - [1. 项目介绍](#1-项目介绍)
  - [2. 数据集分析](#2-数据集分析)
  - [3. 模拟日志产生](#3-模拟日志产生)
    - [3.1. 数据集处理](#31-数据集处理)
    - [3.2. 日志生成](#32-日志生成)
  - [4. 数据采集](#4-数据采集)
    - [4.1. Flume日志采集](#41-flume日志采集)
    - [4.2. Structured Streaming实时流计算](#42-structured-streaming实时流计算)
  - [5. 数据存储设计](#5-数据存储设计)
    - [5.1. t\_news](#51-t_news)
    - [5.2. t\_news\_browse\_record](#52-t_news_browse_record)
    - [5.3. t\_news\_daily\_category](#53-t_news_daily_category)
  - [6. 功能实现](#6-功能实现)
    - [6.1. 标题模糊查询](#61-标题模糊查询)
    - [6.2. 查询单个新闻的生命周期](#62-查询单个新闻的生命周期)
    - [6.3. 查询某些种类的新闻的变化情况](#63-查询某些种类的新闻的变化情况)
    - [6.4. 查询用户兴趣变化](#64-查询用户兴趣变化)
    - [6.5. 组合查询](#65-组合查询)
    - [6.6. 实时新闻推荐](#66-实时新闻推荐)
    - [6.7. 查询日志](#67-查询日志)
  - [7. 加分项](#7-加分项)
    - [7.1. 支持大规模的日志数据实时采集与存储](#71-支持大规模的日志数据实时采集与存储)
    - [7.2. 提高查询性能](#72-提高查询性能)
      - [7.2.1. 数据反规范化](#721-数据反规范化)
      - [7.2.2. 设置索引](#722-设置索引)
    - [7.3. 用户端优化](#73-用户端优化)
      - [7.3.1. 实时数据更新](#731-实时数据更新)
      - [7.3.2. 数据可视化](#732-数据可视化)


## 1. 项目介绍

本项目实现了一个新闻实时动态变化分析系统，为PENS数据提供新闻话题实时动态变化分析、各类新闻的历史与实时统计，新闻话题推荐等功能。有如下几个模块：

1. 模拟日志产生程序：采用PENS中提供的新闻曝光日志数据构建模拟日志产生程序，模拟时序的日志产生。
2. 数据采集：使用Flume框架采集模拟产生的新闻曝光日志，通过Kafka消息队列进行流量控制，使用Structured Streaming流计算处理并存储到存储系统中。
3. 存储系统：使用Mysql搭建数据仓库，存储新闻点击流数据以及新闻数据，为查询系统提供高性能的查询服务。
4. 后端查询系统：使用flask框架与websocket技术提供高效率的查询服务。
5. 前端可视化界面：为新闻动态变化查询结果提供可视化展示界面。

## 2. 数据集分析

PENS数据集包含113,762篇新闻，其主题分为15个类别。每个新闻包括新闻ID、标题、正文和由编辑手动标记的类别。新闻标题和正文的平均长度分别为10.5和549.0。数据集覆盖的时间为：**2019年6月13日-2019年7月3日。**数据集具体内容如下：

news.tsv 中包含了新闻文章的信息

| **字段**       | **示例**                                                     | **含义**                                                     |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Category       | sports                                                       | 新闻所属的15个类别之一                                       |
| Entity content | {'Atlanta United FC': {...}}                                 | 实体的详细信息，包括实体类型、标签、描述、别名、属性和站点链接等 |
| Headline       | Predicting Atlanta United's lineup against Columbus Crew in the U.S. Open Cup | 新闻标题                                                     |
| News body      | Only FIVE internationals allowed, count em, FIVE! So first off we should say, per our usual Atlanta United lineup predictions, this will be wrong... | 新闻正文内容                                                 |
| News ID        | N10000                                                       | 新闻的唯一ID                                                 |
| Title entity   | {"Atlanta United's": 'Atlanta United FC'}                    | 新闻标题中包含的实体，以字典形式表示，包括实体在标题中的文本和对应的Wikidata实体ID |
| Topic          | soccer                                                       | 新闻的具体主题                                               |

train.tsv 是用于训练的用户点击历史记录和展示日志

valid.tsv 是用于验证的用户点击历史记录和展示日志

| **字段**      | **示例**                     | **含义**                                                     |
| ------------- | ---------------------------- | ------------------------------------------------------------ |
| UserID        | U335175                      | 用户的唯一ID，用于标识不同的用户                             |
| ClicknewsID   | N41340 N27570 N83288 ...     | 用户历史点击的新闻ID列表，以空格分隔。该字段用于记录用户的兴趣偏好 |
| dwelltime     | 116 23 59 ...                | 用户历史点击的新闻浏览时长，以空格分隔。该字段可用于评估用户对不同新闻的兴趣程度 |
| exposure_time | 6/19/2019 5:10:01 AM#TAB#... | 历史点击新闻的曝光时间，以“#TAB#”分隔。该字段可用于分析用户对不同时间段新闻的兴趣程度 |
| pos           | N55476 N103556 N52756 ...    | 本次展示日志中用户点击的新闻ID列表，以空格分隔。该字段用于记录用户在本次展示中点击的新闻 |
| neg           | N48119 N92507 N92467 ...     | 本次展示日志中未被用户点击的新闻ID列表，以空格分隔。该字段用于记录用户在本次展示中未点击的新闻 |
| start         | 7/3/2019 6:43:49 AM          | 本次展示日志的开始时间，用于记录用户开始阅读的时间           |
| end           | 7/3/2019 7:06:06 AM          | 本次展示日志的结束时间，用于记录用户结束阅读的时间           |
| dwelltime_pos | 34 83 79 ...                 | 本次展示日志中用户点击新闻的浏览时长，以空格分隔。该字段用于评估用户对本次展示中点击新闻的兴趣程度 |

## 3. 模拟日志产生

### 3.1. 数据集处理

对于news.tsv，我们删去了无用字段Title entity和Entity content，并将news_id字段去除前导N，转换为int存储，方便后续在数据库中设置主键和建立索引。除此以外，我们针对所有英文字段进行了清洗，去除了换行符、制表符、转义符等无用数据。

```Python
news = pd.read_csv("./datatest/news.csv", sep='\t', encoding='utf-8')
news.drop(["Title entity", "Entity content"], axis=1, inplace=True)
news.rename(columns={
    "News ID": "news_id",
    "Category": "category",
    "Topic": "topic",
    "Headline": "headline",
    "News body": "content",
    }, inplace=True)
news["news_id"] = news["news_id"].apply(lambda n: int(n[1:]) - 10000)
def etl_f(x):
    x = str(x)
    x = x.replace("\'", '').replace('\"', '')
    x = x.replace('"', '').replace("'", '')
    x = x.replace('\n', '').replace('\r', '').replace('\t', '')
    return x
news['category'] = news['category'].apply(lambda x: etl_f(x))
news['topic'] = news['topic'].apply(lambda x: etl_f(x))
news['headline'] = news['headline'].apply(lambda x: etl_f(x))
news['content'] = news['content'].apply(lambda x: etl_f(x))
```

最后我们得到了113762条新闻，每条新闻包含category、topic、headline和content字段。

![img](./resource/(null)-20230606132447874.(null))

对于点击记录，我们将train.tsv和valid.tsv合并，得到50万条记录（该记录每当用户点开新闻页面产生一条），通过分析每条记录的各个字段，可以将他们分成两部分：

1、用户历史点击记录，指在当前时刻，用户的历史中所有曾经点击过新闻ID、对应的点击事件和浏览的持续时间；

2、当前页面点击记录，指只针对当前浏览页面存在的新闻，用户点击和没有点击的新闻ID、点击过新闻的浏览持续时间、以及当前记录的最初始时间。

针对这两个部分，我们发现前者可以精确到每次点击的时间点和该次浏览的持续时间，但后者只能精确到打开该页面的时间点，对于该页面上点击的新闻，只有浏览的持续时间。并且我们发现历史点击记录包含了当前页面点击记录，并且前者总数远远大于后者。因此最后我们使用用户历史点击记录，即字段ClicknewsID、dwelltime和exposure_time。

我们使用`.split`函数将其分割为4元组，即`(user_id`**`, `**`news_id`**`, `**`start_ts`**`, `**`duration)`，分别表示用户ID、新闻ID、新闻点击时间戳、浏览时间，这里我们将诸如`6/19/2019 5:10:01 AM`的字符串转换为时间戳，用`unsigned int`，从而便于排序和查询速度。

```Python
import pandas as pd
train = pd.read_csv("./datatest/train.tsv", sep='\t')
valid = pd.read_csv("./datatest/valid.tsv", sep='\t')
logdata = pd.concat([train, valid], axis=0) # 合并train和valid

# 去除UserID的前导U，并转换为int
logdata['UserID'] = logdata['UserID'].apply(lambda x: int(x[1:]))

# 将诸如6/19/2019 5:10:01 AM#TAB#6/19/2019 5:11:58 AM的字段以#TAB拆分，并转换为时间戳
def f1(str_t):
    str_t_list = str_t.split('#TAB#')
    timestamp_list = list(map(lambda str_t: str(int(datetime.strptime(str_t, '%m/%d/%Y %I:%M:%S %p').timestamp())), str_t_list))
    return ' '.join(timestamp_list)
logdata['exposure_time'] = logdata['exposure_time'].apply(lambda str_t: f1(str_t))

# 去除冗余的UserID行
logdata = logdata.drop_duplicates(subset='UserID', keep='last')


from tqdm import tqdm
# 创建一个新的DataFrame
df = pd.DataFrame(columns=['user_id', 'news_id', 'start_ts', 'duration'])

# 遍历行，将历史数据字段用空格拆分为四元组，并存入新的dataframe
for _, row in tqdm(logdata.iterrows(), total=len(logdata)):
    user_id = int(row['UserID'])
    news_id_list = row['ClicknewsID'].split(' ')
    duration_list = row['dwelltime'].split(' ')
    start_timestamp_list = row['exposure_time'].split(' ')
    
    # 判断list个数是否匹配
    assert len(news_id_list) == len(duration_list)
    assert len(news_id_list) == len(start_timestamp_list)
    
    for i in range(len(news_id_list)):
        news_id = int(news_id_list[i][1:]) - 10000
        duration_time = int(duration_list[i])
        start_timestamp = int(start_timestamp_list[i])
        # 新增一行四元组
        df.loc[len(df)] = [user_id, news_id, start_timestamp, duration_time]
df = df.sort_values('start_timestamp', ascending=True)
```

最后保存得到27182788条点击记录，我们将其按照start_ts进行排序，并存储在csv文件中。

![img](./resource/(null)-20230606132452466.(null))

### 3.2. 日志生成

我们直接读取上述处理过后的csv文件，将其使用`.iterrows()`按行迭代。我们设置一个当前时间戳，每当新读取一行点击时间，我们用新时间戳减去当前时间戳得到时差delta，并让程序睡眠delta秒，睡眠完成后再将其写入到log.txt文件中。由flume监视log.txt的改变，当有新的内容在文件末尾写入时，就将其采集给kafka消息队列中。

```Python
logfile = pd.read_csv("./PENS/log.csv")
current_timestamp = logfile.iloc[0]['start_ts']
for idx, row in logfile.iterrows():
    time.sleep(row['start_ts'] - current_timestamp)
    with open('./click.log', '+a') as f:
        f.write(" ".join(list(map(lambda x: str(x), row.to_list()))) + '\n')
    current_timestamp = row['start_ts']
```

## 4. 数据采集

### 4.1. Flume日志采集

我们将Flume与模拟日志产生程序部署在同一台服务器上，因此Flume可以使用`tail -F` 命令实时读取生成的log文件，但是由于`exec` 类型的读取无法实现断点续传，因此我们使用了`taildir` 作为Flume的输入源。

Memory Channel在使用的过程中受内存容量的限制不能缓存大量的消息，并且如果Memory Channel中的消息没来得及写入Sink，此时Agent出现故障就会造成数据丢失。File Channel虽然能够缓存更多的消息，但如果缓存下来的消息还没有写入Sink，此时Agent出现故障则File Channel中的消息不能被继续使用，直到该Agent重新恢复才能够继续使用File Channel中的消息。Kafka Channel相对于Memory Channel和File Channel存储容量更大、容错能力更强，弥补了其他两种Channel的短板。因此，我们认为在实时计算的场景下使用Kafka Channel是较优的选择，通过搭建Kafka伪分布式集群的方法在廉价的硬件条件下完成高效的消息发布和订阅。

```Bash
#agent_name
a1.sources=r1
a1.sinks=k1
a1.channels=c1

#source的配置
# source类型
a1.sources.r1.type = TAILDIR
# 元数据位置
a1.sources.r1.positionFile = /usr/local/work/generate/streaming_access.log
# 监控的目录
a1.sources.r1.filegroups = f1
a1.sources.r1.filegroups.f1=/usr/local/work/generate/.*log
a1.sources.r1.fileHeader = true
a1.sources.r1.interceptors = i1
a1.sources.r1.interceptors.i1.type = timestamp

#channel的配置
a1.channels.c1.type = org.apache.flume.channel.kafka.KafkaChannel
a1.channels.c1.kafka.bootstrap.servers = 100.81.9.75:9092,100.81.9.75:9093，100.81.9.75:9094
a1.channels.c1.kafka.topic = kafka_streaming_topic
a1.channels.c1.kafka.consumer.group.id = kafka_streaming_topic_01
a1.channels.c1.kafka.consumer.timeout.ms = 70000
a1.channels.c1.kafka.consumer.request.timeout.ms = 80000
a1.channels.c1.kafka.consumer.fetch.max.wait.ms=7000
a1.channels.c1.kafka.consumer.offset.flush.interval.ms = 50000
a1.channels.c1.kafka.consumer.session.timeout.ms = 70000
a1.channels.c1.kafka.consumer.heartbeat.interval.ms = 60000
a1.channels.c1.kafka.consumer.enable.auto.commit = false

#用channel链接source
a1.sources.r1.channels = c1
```

![img](./resource/(null)-20230606132500701.(null))

因为我们使用了Kafka Channel，所以能在日志收集层只配置Source组件和Kafka Channel组件，不需要再配置Sink组件，只需要在Kafka Channel中标出消费者对列的服务器IP以及端口即可，减少了日志收集层启动的进程数并且有效降低服务器内存、磁盘等资源使用率，日志汇聚层可以只配置Kafka Channel和Sink，不需要再配置Source，减少日志汇聚层的进程数，这样的配置既能降低服务器的资源使用率又能减少Event在网络之间的传输，有效提高日志采集系统的性能。

### 4.2. Structured Streaming实时流计算

针对时刻都在产生的新闻流点击记录，我们需要使用流计算工具，在数据到达的时候就立即对其进行处理，计算存储到数据库中。我们使用Apache Spark的Structured Streaming来实现实时流计算，当消息生产者发送的消息到达某个topic的消息队列时，就会触发计算。相比于 Spark Streaming 建立在 RDD数据结构上面，Structured Streaming 是建立在 SparkSQL基础上，DataFrame的绝大部分API也能够用在流计算上，实现了流计算和批处理的一体化，并且由于SparkSQL的优化，具有更好的性能，容错性也更好。

当读取到Kafka中的新闻点击流数据时，将数据存储到t_news_browse_record浏览记录表中，并根据news_id增加t_news中对应新闻的总浏览量和浏览时长；过一天就立刻统计前一天各个category新闻的浏览量与浏览时长。

## 5. 数据存储设计

### 5.1. t_news

```SQL
create table t_news
(
    news_id               int          not null
        primary key,
    headline              varchar(256) null,
    content               mediumtext   null,
    category              varchar(16)  not null,
    topic                 varchar(64)  not null,
    total_browse_num      int unsigned not null,
    total_browse_duration int unsigned not null,
    constraint t_news_news_id_uindex
        unique (news_id)
);
```

该表存储了所有的新闻信息，包含新闻ID、标题headline、内容content、类别category、主题topic，以及用于统计的总浏览次数total_browse_num和总浏览时长total_browse_duration。

我们将new_id设置为主键，使其自动添加了索引，从而加快针对某个或某些new_id的查询；在考虑针对某个新闻类别或主题的查询时，我们尝试过将category和topic也建立索引，但是我们发现这两个字段存在大量相等项，如在113762条新闻中，只有15个类别和372个主题，这样建立的索引对速度的提升微乎其微，并且由于是针对字符串建立索引，会造成较大的空间消耗，因此最后没有选择针对这两项建立索引。

### 5.2. t_news_browse_record

```SQL
create table t_news_browse_record
(
    user_id   int          not null,
    news_id   int          not null,
    start_ts  int unsigned not null,
    duration  int          not null,
    start_day int unsigned not null
);

create index t_news_browse_record_news_id_index
    on t_news_browse_record (news_id);

create index t_news_browse_record_start_day_index
    on t_news_browse_record (start_day);

create index t_news_browse_record_start_ts_index
    on t_news_browse_record (start_ts);

create index t_news_browse_record_user_id_index
    on t_news_browse_record (user_id);
```

该表存储用户的新闻浏览记录，包括用户ID、新闻ID、浏览时间戳、浏览持续时间和浏览的天戳，这里的天戳指距离1970年的天数，是将时间戳整除24*60*60得到。该表会在kafka队列出口的实时流计算程序中被不断添加新的行。

我们将以秒和天作为最小单位的时间都以整数表示，在具体需要显示时再将其转换，目的是便于建立索引、加快诸如根据天数统计相关信息等等。

我们针对用户ID、新闻ID、时间戳start_ts、天戳start_day都建立了索引，分别加快了：

1. 用户ID索引：加快针对某些用户浏览情况的查询
2. 新闻ID索引：加快针对某些/某类新闻被点击情况的查询
3. 时间戳start_ts和天戳start_day索引：加快针对某个时间段的用户浏览情况和新闻被点击情况的查询

该表的行数很多，最多时可达27182788行，因此若进行综合查询（如先查询某一类别的新闻被点击情况），当涉及到表的join时，速度会变得非常慢；因此我们添加了下列表用于实时存储一些冗余信息。

### 5.3. t_news_daily_category

```SQL
create table t_news_daily_category
(
    day_stamp       int         not null,
    category        varchar(16) not null,
    browse_count    int         null,
    browse_duration int         null,
    constraint t_news_daily_category_pk
        unique (day_stamp, category)
);
```

该表存储某天某类别的新闻被浏览的次数和持续时间。作为冗余表，他可以被t_news_browse_record中被直接计算出来，但是由于t_news_browse_record的行数过多，如果按照类别查询，则会与t_news进行join操作，导致查询时间大量增加。因此我们设置定时任务，在kafka队列出口的实时流计算程序中判断是否进入了新的一天（根据四元组中的时间戳），如果进入新的一天，则统计前一天的新闻类别点击情况，并存入本表格，大大提升查询效率。

我们可以根据不同查询任务设置不同的冗余表，并设置类似定时任务程序来从主表中统计相关数据，进而存储到冗余表中，在查询相关任务时直接针对冗余表进行查询，大大提升效率。

## 6. 功能实现

### 6.1. 标题模糊查询

根据用户输入的标题返回五条最为匹配的新闻标题。

```SQL
select news_id,headline 
from t_news 
where headline 
like '%ideal%' limit 5;
```

![img](./resource/(null)-20230606132516639.(null))

### 6.2. 查询单个新闻的生命周期

根据新闻标题，查找指定新闻在指定时间内（可选）的日浏览量变化，前端使用折线图进行展示。

```SQL
select count(*), from_unixtime(tnbr.start_ts,"%Y-%m-%d") 
from t_news_browse_record tnbr 
where 1560355200 <= tnbr.start_ts and tnbr.start_ts <= 1562083200 and news_id = 12 
group by tnbr.news_id ,from_unixtime(tnbr.start_ts,"%Y-%m-%d");
```

![img](./resource/(null)-20230606132520005.(null))

### 6.3. 查询某些种类的新闻的变化情况

查询选择的新闻种类在指定时间内日浏览数的变化，单种类查询结果如下图所示：

![img](./resource/(null)-20230606132523287.(null))

同时能支持选取多个新闻种类进行查询，多查询结果如下：

```SQL
select day_stamp,category,browse_count 
from t_news_daily_category 
where day_stamp>=18059 and day_stamp<=18078 
and (category = 'autos' or category = 'entertainment' or category = 'finance') 
group by day_stamp,category;
```

![img](./resource/(null)-20230606132526066.(null))

### 6.4. 查询用户兴趣变化

查询指定用户在指定时间内不同种类新闻的浏览数量。

```SQL
select count(*),n.category 
from t_news as n 
join (select tnbr.news_id,tnbr.start_ts 
      from t_news_browse_record as tnbr 
      where tnbr.user_id=12000 and tnbr.start_ts>=1560355200 and tnbr.start_ts<=1561996800) as t 
on n.news_id=t.news_id 
group by n.category;
```

![img](./resource/(null)-20230606132529313.(null))

### 6.5. 组合查询

根据用户id、新闻标题长度、新闻内容长度、新闻种类、新闻主题、起始时间组合查询用户浏览过的所有新闻。示例如下：

![img](./resource/(null)-20230606132532018.(null))

```SQL
select distinct new.headline, new.news_id 
from t_news_browse_record as tnbr join t_news as new 
on tnbr.news_id = new.news_id 
where tnbr.start_ts >= 1560355200 and tnbr.start_ts <= 1561996800 and user_id >= 1008 and user_id <= 1008 
and  tnbr.news_id in 
    (select news_id from t_news n 
    where LENGTH(n.headline) >= 7  and LENGTH(n.headline) <= 245 
    and LENGTH(n.content) >= 2 and LENGTH(n.content) <= 5000 and n.topic like '%soccer%');
```

同时，我们可以查看新闻的具体内容。

![img](./resource/(null)-20230606132534695.(null))

### 6.6. 实时新闻推荐

在该界面中，我们使用websocket实时从后端获取用户最新点击的新闻记录，并根据用户最近二十条中浏览最多的两个新闻种类向用户进行推荐。

因为我们在`t_news`表中实时记录了每一条新闻的总浏览量和总浏览时间，所以我们根据总浏览量和总浏览时间的一个加权值（0.9*总浏览量+0.1*总浏览时长）对用户最近喜欢的两个新闻种类降序排列，选取其中的十条向用户进行推荐。

![img](./resource/(null)-20230606132539933.(null))

![img](./resource/(null)-20230606132543230.(null))

### 6.7. 查询日志

我们在调用api进行实时查询或者静态查询时，将使用到的sql语句和执行时间记录下来，能够记录所有的SQL查询记录和查询时间，便于对性能指标进行检验和优化以及对bug的定位。

![img](./resource/(null)-20230606132547317.(null))

![img](./resource/(null)-20230606132553238.(null))

## 7. 加分项

### 7.1. 支持大规模的日志数据实时采集与存储

使用`taildir` 作为Flume的输入源，能够实时监控多个日志文件，其断点续传的功能使得日志数据的采集更加稳定，即使在中断和重启的情况下也能够继续采集日志数据，确保了数据的完整性和可靠性；同时，我们使用了相对于Memory Channel和File Channel存储容量更大、容错能力更强的Kafka Channel，通过搭建Kafka伪分布式集群的方法在廉价的硬件条件下完成高效的消息发布和订阅从而支持了更大规模日志数据的采集。

为了进一步提高计算效率，我们将存储系统和Spark实时计算系统部署在两台不同的服务器上。这样做可以充分利用服务器的算力和内存资源，实现更高效的Spark结构化流实时计算。通过将计算和存储分离，我们可以针对特定的任务需求调配更多的计算资源或存储资源，以优化整个系统的性能。这种部署方式还能够有效避免资源竞争和冲突，提高系统的稳定性和可靠性。

综上所述，通过使用taildir作为输入源、Kafka通道作为存储通道，并将存储系统和Spark实时计算系统分别部署在不同的服务器上，我们能够充分发挥各项技术的优势，实现高效、稳定和可扩展的大规模日志数据采集和实时计算。

### 7.2. 提高查询性能

#### 7.2.1. 数据反规范化

我们根据具体需求，对数据进行规范化或反规范化。规范化可以减少数据冗余和维护复杂性，但在查询性能方面可能存在一定的影响而反规范化可以提高查询性能。

我们设置了t_news_daily_category表，该表存储某天某类别的新闻被浏览的次数和持续时间。作为冗余表，他可以被t_news_browse_record中被直接计算出来，但是由于t_news_browse_record的行数过多，如果按照类别查询，则会与t_news进行join操作，导致查询时间大量增加。因此我们设置定时任务，在kafka队列出口的实时流计算程序中判断是否进入了新的一天（根据四元组中的时间戳），如果进入新的一天，则统计前一天的新闻类别点击情况，并存入本表格，大大提升查询效率。效率对比如下：

优化前，在t_news_browse_record表中进行查询：

```SQL
select count(tnbr.news_id),start_day
from (t_news_browse_record tnbr join (select news_id from t_news where category='autos') as n on tnbr.news_id = n.news_id)
where tnbr.start_day>=18061 and tnbr.start_day<=18072
group by tnbr.start_day;
```

![img](./resource/(null)-20230606132557258.(null))

优化后：

```SQL
select day_stamp,category,browse_count 
from t_news_daily_category 
where day_stamp>=18061 and day_stamp<=18072 
and (category = 'autos') 
group by day_stamp,category;
```

![img](./resource/(null)-20230606132600502.(null))

我们可以根据不同查询任务设置不同的冗余表，并设置类似定时任务程序来从主表中统计相关数据，进而存储到冗余表中，在查询相关任务时直接针对冗余表进行查询，大大提升效率。

#### 7.2.2. 设置索引

在t_news表中，我们将new_id设置为主键，使其自动添加了索引，从而加快针对某个或某些new_id的查询。

在t_news_browse_record表中，我们针对用户ID、新闻ID、时间戳start_ts、天戳start_day都建立了索引，分别加快了：

1. 用户ID索引：加快针对某些用户浏览情况的查询
2. 新闻ID索引：加快针对某些/某类新闻被点击情况的查询
3. 时间戳start_ts和天戳start_day索引：加快针对某个时间段的用户浏览情况和新闻被点击情况的查询

### 7.3. 用户端优化

#### 7.3.1. 实时数据更新

通过WebSocket等实时通信技术，将新闻的动态变化实时推送给用户，让用户能够及时了解新闻的最新动态。

#### 7.3.2. 数据可视化

利用数据可视化工具将新闻随着时间的动态变化以图表等形式展示给用户，提升用户体验和可交互性。

![img](./resource/(null)-20230606132604791.(null))