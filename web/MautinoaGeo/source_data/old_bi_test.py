from sqlalchemy import create_engine, MetaData, func, case, literal_column
from sqlalchemy.orm import sessionmaker
import pandas as pd
import glob
import os

# remove any existing database that may share a name with your intended file

if 'indeed.db' in os.listdir('.'):
    os.remove('indeed.db')

# Create Pandas dataframes via Glob
# and sanitise for PSQL / SQLite usage

engine = create_engine('sqlite:///indeed.db')

for dataset in glob.glob('./*.csv'):

    table_name = dataset.strip(".").strip("/").strip(".csv").lower()
    table_data = pd.read_csv(dataset)

    print "Currently working on: {0} ".format(table_name)
    for c in list(table_data):
        new_column = c.lower().replace('#', 'number').replace(' ', '_')
        table_data.rename(columns={c: new_column}, inplace=True)

    table_data.to_sql(name=table_name, con=engine, index=False)

# get the tables that were just built usable by SQLAlchemy for Querying

metadata = MetaData()
metadata.reflect(bind=engine)

diagnosis_code = metadata.tables['diagnosiscode']
body_part = metadata.tables['bodypart']
neiss2014 = metadata.tables['neiss2014']
disposition = metadata.tables['disposition']

# create a session to query

Session = sessionmaker(bind=engine)
session = Session()

# start writing queries

"""Question 1
What are the top three body parts most frequently represented in this dataset?
What are the top three body parts that are least frequently represented?
SELECT
  count(*) AS amount,
  bp.bodypart AS body_part
FROM
  neiss2014 n
LEFT JOIN
  bodypart bp
ON
    n.body_part = bp.code
GROUP BY
  body_part
ORDER BY
  amount DESC

"""

top_three = session.query(func.count(neiss2014), body_part.c.bodypart) \
                .join(body_part, neiss2014.c.body_part == body_part.c.code) \
                .group_by(body_part.c.bodypart) \
                .order_by(func.count(neiss2014).desc()) \
                .all()[:3]

least_three = session.query(func.count(neiss2014), body_part.c.bodypart) \
                  .join(body_part, neiss2014.c.body_part == body_part.c.code) \
                  .group_by(body_part.c.bodypart) \
                  .order_by(func.count(neiss2014).asc()) \
                  .all()[:3]

print "The top three are: \n %s \n and the bottom three are: \n %s" % (top_three, least_three)

"""
Question 2
How many injuries in this dataset involve a skateboard?
Of those injuries, what percentage were male and what percentage were female?
What was the average age of someone injured in an incident involving a skateboard?
"""

skateboard = session.query(func.count(neiss2014)) \
    .filter(neiss2014.c.narrative.like('%SKATEBOARD%')) \
    .all()

print "The number of cases with a skateboard is : %s" % (skateboard)

sqlite_sex_distribution = """SELECT
  SUM(CASE sex
      WHEN 'Female'
        THEN 100.0
      ELSE 0 END) / COUNT(*) AS female_percentage,
  SUM(CASE sex
      WHEN 'Male'
        THEN 100.0
      ELSE 0 END) / COUNT(*) AS male_percentage,
  COUNT(*)                   AS total_count,
  SUM(CASE sex
      WHEN 'Female'
        THEN 1
      ELSE 0 END)  AS female_count,
  SUM(CASE sex
      WHEN 'Male'
        THEN 1
      ELSE 0 END) AS male_count

FROM
  neiss2014 n;"""

centuriser = literal_column("100.0")
sex_distribution = session.query(

    func.sum(case(
        [
            (neiss2014.c.sex == 'Female', centuriser),
        ],
        else_=0
    )
    ) / func.count(neiss2014).label('female_percentage'),

    func.sum(case(
        [
            (neiss2014.c.sex == 'Male', centuriser),
        ],
        else_=0
    )
    ) / func.count(neiss2014).label('male_percentage'),

    func.count(neiss2014).label('total_count'),
    func.sum(case(
        [
            (neiss2014.c.sex == 'Female', 1),
        ],
        else_=0
    )
    )
    .label('female_count'),

    func.sum(case(
        [
            (neiss2014.c.sex == 'Male', 1),
        ],
        else_=0
    )
    )
    .label('male_count'),

).all()

print sex_distribution
