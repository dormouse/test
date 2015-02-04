# !/usr/bin/env python
# -*- coding: UTF-8 -*

"""
安装 pandas
sudo apt-get install python-pandas
sudo apt-get install python-scipy python-matplotlib python-tables python-numexpr python-xlrd python-statsmodels python-openpyxl python-xlwt python-bs4
"""

import pandas as pd
import numpy as np

# 读入数据
df = pd.read_csv('test.csv')

# 打印列类型
types = df.columns.to_series().groupby(df.dtypes).groups
print types

# 转换列类型
df['出生日期'] = df['出生日期'].astype(str)
types = df.columns.to_series().groupby(df.dtypes).groups
print types

# 改变列头
# 方式一
df.columns = ['name', 'sex', 'BOD', 'score']
print df.tail(3)

# 方式二
# 大写转小写
df.columns = [c.lower() for c in df.columns]

# 方式三
# 大写转小写
df = df.rename(columns=lambda x: x.lower())
print df.tail(3)

# 方式四
# 改变特定的列头
df = df.rename(columns={'name': u'姓名', 'sex': u'性别'})
print df.tail(3)

# 复制一个 DataFrame
df_1 = df.copy()
print df_1

# 插入列
# 方式一：在末尾添加
df['team'] = pd.Series('', index=df.index)
print df.tail(3)


# 方式二：在中间插入
df.insert(loc=3, column='age', value='')
print df.tail(3)


# 根据列类型来选择
# 只选择字符串型的列
print df.loc[:, (df.dtypes == np.dtype('O')).values].head()

# 根据现有值生成一个新的列
df.insert(loc = 5 , column='score1', value=df['score']-1)
print df.tail(3)


# 根据现有值生成多个新的列
# 方法一
def process_bod_col(text):
    #根据出生日期生成年，月，日三个新的列
    year = text[:4]
    month = text[4:6]
    day = text[6:]
    return pd.Series([year, month, day])

df[['bod_year', 'bod_month', 'bod_day']] = df.bod.apply(process_bod_col)
print df.head()

# 方法二(没有方法一好)
for idx, row in df.iterrows():
    year, month, day = process_bod_col(row['bod'])
    df.ix[idx, 'bod_year'], df.ix[idx, 'bod_month'], df.ix[idx, 'bod_day'] = year, month, day
print df.head()


# 改变一列的值
df['score'] = df['score'].apply(lambda x: x + 1)

# 同时改变多个列的值
cols = ['score', 'score1']
df[cols] = df[cols].applymap(lambda x: x-10)
print df.head()

# 空值处理（NaN）
# 计数有空值的行
nans = df.shape[0] - df.dropna().shape[0]
print(u'一共有 %d 行出现空值' % nans)

# 选择`性别`为空值的行
print df[df[u'性别'].isnull()]

# 选择`性别`为非空值的行
print df[df[u'性别'].notnull()]

# 填充`性别`的空值为`未明确`
df.fillna(value=u'未明确', inplace=True)
print df


# 添加一个空行
df = df.append(pd.Series(
                [np.nan]*len(df.columns), # Fill cells with NaNs
                index=df.columns),
                ignore_index=True)
print df.tail(3)

# 单元格赋值
# 单个单元格赋值
df.loc[df.index[-1], u'姓名'] = '新名字'
df.loc[df.index[8], u'bod'] = '19990512'
print df.tail(3)

# 多单个单元格赋值
df.loc[df.index[0:2], 'score'] = [33.0, 44.0]
print df.head(3)

# 排序
# 根据某一列排序（由高到低, 空值被视为最高）
df.sort('score', ascending=False, inplace=True)
print df.head()

# 排序后重新编制索引
df.index = range(1,len(df.index)+1)
print df.head()

# 使用另一个 DataFrame 来更新数据
print u'现有的 DataFrame'
print df
print u'新的 DataFrame'
print df_1
df.set_index(u'姓名', inplace=True)
df_1.set_index(u'姓名', inplace=True)
df.update(other=df_1['score'], overwrite=True)

# 重置 index
df.reset_index(inplace=True)
print df

# 根据条件过滤
print u'男性或分数大于80'
print  df[ (df[u'性别'] == '男') | (df['score'] >= 80) ]

print u'男性且分数大于80'
print  df[ (df[u'性别'] == '男') & (df['score'] >= 80) ]
