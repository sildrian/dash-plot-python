from sqlalchemy import create_engine

# set params
# conn = create_engine(os.environ['DB_URI']) #original
def conn():
    return create_engine("mysql+mysqldb://lia:lia201289@10.0.1.10/report")