from sqlalchemy import create_engine

# set params
# conn = create_engine(os.environ['DB_URI']) #original
def conn():
    return create_engine("mysql+mysqldb://admin:admin@127.0.0.1/soccer-stats")