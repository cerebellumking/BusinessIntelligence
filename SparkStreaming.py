import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types as T
from pyspark.sql import functions as F
import time
import os
import random
import pandas as pd
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
import tqdm
from flask_cors import CORS
import pymysql

const_start_day = 18073
# 处理一个batch的数据
def getBatchData(batch_df):
    global const_start_day
    batch_df = batch_df.toPandas()
    # 如果为空，直接返回
    if batch_df.empty:
        return
    db = pymysql.connect(host='100.81.9.75', port=3306, user='hive',
                         password='shizb1207', database='bi_test', charset='utf8')
    cursor = db.cursor()
   
    # 将pandas的value导出为list
    batch_df = batch_df['value'].tolist()
    for i in batch_df:
        value = i.split(' ')
        user_id, news_id, start_ts, duration = int(value[0]), int(value[1]), int(value[2]), int(value[3])
        start_day = start_ts // 86400
        # 批处理：昨日各个category新闻的浏览量
        if start_day > const_start_day:
            print(start_day)
            sql = """
            insert into t_news_daily_category
                    (select tnbr.start_day,n.category,count(tnbr.news_id),sum(tnbr.duration)
                    from (t_news_browse_record tnbr join (select news_id,category from t_news) as n on tnbr.news_id = n.news_id)
                    where tnbr.start_day=%s
                    group by n.category);""" %(const_start_day)
            cursor.execute(sql)
            const_start_day = const_start_day + 1
        # 流计算：插入浏览记录并实时更改指定新闻的浏览数
        sql1 = """
        insert into t_news_browse_record(user_id,news_id,start_ts,duration,start_day) values(%s,%s,%s,%s,%s)""" %(user_id,news_id,start_ts,duration,start_day)
        sql2 = """
        update t_news set total_browse_num = total_browse_num + 1,total_browse_duration = total_browse_duration +%s where news_id = %s""" %(duration,news_id)
        cursor.execute(sql1)
        cursor.execute(sql2)
    db.commit() 
    cursor.close()
    db.close()


# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 testSparkStreaming.py'
scala_version = '2.12'
spark_version = '3.3.2'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.4.0'
]
spark = SparkSession.builder \
    .appName("structured streaming") \
    .config("spark.jars.packages", ",".join(packages))\
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.default.parallelism", "8") \
    .config("master", "local[*]") \
    .config("spark.driver.memory", '4G')\
    .config("spark.executor.memory", '4G')\
    .enableHiveSupport() \
    .getOrCreate()

sc = spark.sparkContext

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "100.81.9.75:9092") \
    .option("subscribe", "kafka_streaming_topic") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

query = df.writeStream.foreachBatch(getBatchData).start()
query.awaitTermination()
