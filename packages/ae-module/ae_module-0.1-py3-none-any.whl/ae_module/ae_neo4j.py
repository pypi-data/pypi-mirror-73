import pandas as pd
from py2neo import Graph
from ae_db import aws_db
from ae_top30.get_data import ae_data_manager; am = ae_data_manager.instance()
from ae_telegram_message import ae_tele_message

user_name = 'neo4j'
password =  'xBoUD6vuWV1FS6vf' # gcp
bolt_url_1 = 'bolt://34.64.157.195:7687'
bolt_url_2 = 'bolt://34.64.238.13:7687'
bolt_url_3 = 'bolt://34.64.241.139:7687'
g_1 = Graph(bolt_url_1, auth=(user_name,password))
g_2 = Graph(bolt_url_2, auth=(user_name, password))
g_3 = Graph(bolt_url_3, auth=(user_name, password))

l_graphs = [g_1, g_2, g_3]

# bolt_url_sb ='bolt://34.239.207.167:35634'
# pw_sb = 'meeting-dot-scissors'
# g_sb = Graph(bolt_url_sb, auth=(user_name, pw_sb))

def get_LEADER(l_graphs):
    for g in l_graphs:
        check_str = str(g.run('call dbms.cluster.role("neo4j")').to_table())
        print(check_str)
        if 'LEADER' in check_str:
            ae_tele_message.send_message(f'current LEADER on neo4j is {g}')
            return g
    print('something wrong')

    return 'something wrong'

def send_dataframe(graph, df, statement):
    print(f'sending dataframe of {df.shape}')
    # tx = graph.auto() # v5에 들어간 내용
    tx = graph.begin(autocommit=True)
    params = df.to_dict(orient='records')

    print(
        tx.evaluate(statement, parameters = {"params" : params})
    )
def get_batches(l, batch_size = 100):
    return ((i, l[i:i+batch_size]) for i in range(0, len(l), batch_size))

def send_dataframe_batch(graph, df, statement, batch_size):
    # dataframe is indexed with numerical indexes
    # lis_edge = df.to_dict(orient='records')

    batches = get_batches(df, batch_size)
    for i, df in batches:
        print(f'batch size {df.shape}')
        send_dataframe(graph, df, statement)

g_l = get_LEADER(l_graphs)

if __name__ == '__main__':
    # date_ref = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    # date_ref = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    print(g_l)