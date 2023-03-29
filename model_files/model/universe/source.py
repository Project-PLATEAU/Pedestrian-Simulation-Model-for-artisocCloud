def univ_init(self):
    
    # シミュレーション開始時の処理
    
    from time_manager import TimeManager
    from agent_manager import AgentManager
    from network_manager import NetworkManager
    from output_log import OutputLog
    
    # 1マスが何メートルか
    Universe.meter_per_grid = 1.0
    
    # 時刻マネージャ生成
    Universe.time_manager = TimeManager()
    
    # 道路マネージャ生成
    import networkx as nx
    Universe.network = nx.Graph()
    Universe.network_manager = NetworkManager('network_node.csv', 'network_link.csv')
    
    # 立ち寄り率は初期値0に設定
    Universe.drop_rate = 0
    
    # 平日かつイベント有りの場合
    if Universe.day_type == "平日" and Universe.event_type == "イベントあり":
        
        # 平日のエージェントデータを読み込み
        agent_data = 'agent_list_scenario_weekday.csv'
        
        # イベント用のネットワークを追加読み込み
        network_event_node_data = 'network_node_event.csv'
        network_event_link_data = 'network_link_event.csv'
        
        # エージェントマネージャ生成
        Universe.agent_manager = AgentManager(agent_data)
        Universe.agent_manager.set_walk_speed_dict('age_to_walk_speed.csv')
        
        # ノードリンク追加
        Universe.network_manager.read_nodes_and_links(network_event_node_data, network_event_link_data)
        Universe.node_dict = Universe.network_manager.nodes
        
        if Universe.ad_type == "広告なし":
            Universe.network_manager.update_signage_value_to_None()  # 広告がなければsignageの値を0にする
        else:
            pass
    
    # 平日かつイベント無しの場合
    elif Universe.day_type == "平日" and Universe.event_type == "イベントなし":
        
        # 平日のエージェントデータを読み込み
        agent_data = 'agent_list_scenario_weekday.csv'
        
        # エージェントマネージャ生成
        Universe.agent_manager = AgentManager(agent_data)
        Universe.agent_manager.set_walk_speed_dict('age_to_walk_speed.csv')
        
        # ノードリンク追加
        Universe.node_dict = Universe.network_manager.nodes
        
        if Universe.ad_type == "広告なし":
            Universe.network_manager.update_signage_value_to_None()  # 広告がなければsignageの値を0にする
        else:
            pass
    
    # 休日かつイベント有の場合
    elif Universe.day_type == "土日祝日" and Universe.event_type == "イベントあり":
        
        # 休日のエージェントデータを読み込み
        agent_data = 'agent_list_scenario_weekend.csv'
        
        # イベント用のネットワークを追加読み込み
        network_event_node_data = 'network_node_event.csv'
        network_event_link_data = 'network_link_event.csv'
        
        # エージェントマネージャ生成
        Universe.agent_manager = AgentManager(agent_data)
        Universe.agent_manager.set_walk_speed_dict('age_to_walk_speed.csv')
        
        # ノードリンク追加
        Universe.network_manager.read_nodes_and_links(network_event_node_data, network_event_link_data)
        Universe.node_dict = Universe.network_manager.nodes
        
        if Universe.ad_type == "広告なし":
            Universe.network_manager.update_signage_value_to_None()  # 広告がなければsignageの値を0にする
        else:
            pass
        
    # 休日かつイベント無の場合
    elif Universe.day_type == "土日祝日" and Universe.event_type == "イベントなし":
        
        # 休日のエージェントデータを読み込み
        agent_data = 'agent_list_scenario_weekend.csv'
        
        # エージェントマネージャ生成
        Universe.agent_manager = AgentManager(agent_data)
        Universe.agent_manager.set_walk_speed_dict('age_to_walk_speed.csv')
        
        # ノードリンク追加
        Universe.node_dict = Universe.network_manager.nodes
        
        if Universe.ad_type == "広告なし":
            Universe.network_manager.update_signage_value_to_None()  # 広告がなければsignageの値を0にする
        else:
            pass
    
    # アトラクタ確認（当該時間となっているか）
    Universe.network_manager.update_node_attractor(Universe.start_hour)
    
    # ログマネージャ作成
    Universe.output_log = OutputLog()
    
    # ダミーログファイル出力（定期的にネットワーク接続を行うため）
    Universe.fo = open("log.csv", mode='w')

def univ_step_begin(self):
    
    # シミュレーション内の各ステップ開始時の処理
    
    # 時刻表示
    Universe.time = Universe.time_manager.show_time()
    
    # エージェント生成（生成するエージェントがデータとして存在していれば生成する）
    Universe.agent_manager.create_agent_if_needed(Universe.network, Universe.node_dict)
    
    # ダミーログファイル出力
    Universe.fo.write('.')

def univ_step_end(self):
    
    # シミュレーション内の各ステップ終了時の処理
    
    # 時刻を進める
    Universe.time_manager.time_step()
    
    # ログファイル吐き出し（10秒に1回）
    h = Universe.time_manager.get_hour()
    m = Universe.time_manager.get_min()
    s = Universe.time_manager.get_sec()
    if (int(m) % 10) == 0 and s == 0:
        t = f'{str(h).zfill(2)}{str(m).zfill(2)}{str(s).zfill(2)}'
        print(t)
        self.output_log.output_agent_log_file(f"agent_log_{t}.csv")
        
    if (int(m) % 60) == 0 and s == 0:
        # イベント等の時刻が対象時間内かを確認（対象時間外であればアトラクタを最小化）
        Universe.network_manager.update_node_attractor(h)
    
    # 終了時刻になったらおわり
    t = h + m / 60  # 時刻を時間単位で表す（22時30分は22.5)
    if t >= self.end_hour:
        time = str(int(h))
        self.output_log.output_agent_log_file(f"agent_log_{time}_end.csv")
        exit_simulation()

def univ_finish(self):
    
    # シミュレーション終了時の処理
    
    Universe.fo.close()

