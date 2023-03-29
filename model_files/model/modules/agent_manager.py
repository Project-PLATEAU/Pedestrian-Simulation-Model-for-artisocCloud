class AgentManager:
    
    # エージェント全体を管理するオブジェクト
    
    def __init__(self, file):
        self.agent_count = 0  # データの読み込み位置を記憶する
        self.data = []
        self.agent_num = 0  # エージェント数
        self.read_data(file)
        self.age_speed_dict = dict()

    def read_data(self, file):
        
        # エージェントデータを読み込む
        
        import csv
        
        with open(file, mode="r", encoding="shift-jis") as f:
            reader = csv.DictReader(f)
            for line in reader:
                if int(line['time'].split(":")[0]) < int(Universe.start_hour):
                    pass
                else:
                    self.data.append(line)
                    self.agent_num += 1

    def create_agent_if_needed(self, G, node_dict):
        
        # 必要に応じてエージェントを生成する
        
        if self.is_create_agent_time():
            
            # 生成する時刻であれば、生成
            self.create_agent(G, node_dict)
            
            # 再帰的に呼ぶ（同時刻に複数人生成することがあるため）
            self.create_agent_if_needed(G, node_dict)
    
    def is_create_agent_time(self):
        
        # エージェントを生成する時刻かどうかを返す
        
        # エージェントを全て生成し終わったら、何もしない
        if self.agent_count >= self.agent_num:
            return
        
        next_agent = self.data[self.agent_count]  # 次のエージェントデータ
        t = next_agent["time"].split(":")  # 発生時刻[h:m:s]
        now = Universe.time_manager.get_time()
        
        return Universe.time_manager.compare_time(now, t)  # 生成時刻よりも今が進んでいればTrue
        
    def create_agent(self, G, node_dict):
        
        # エージェントを生成する
        
        next_agent = self.data[self.agent_count]  # 次のエージェント
        a = create_agt(Universe.map.agent)
        
        a.agent_id = next_agent["agent_id"]
        a.time = Universe.time_manager.get_time_from_string(next_agent["time"])  # 出発時刻

        # トリップの設定
        a.trip = a.set_agent_trip(next_agent["origin_1"], next_agent["destination_1"], next_agent["waiting_time_1"],
                                  next_agent["destination_2"], next_agent["waiting_time_2"])
      
        a.link_sequence = a.set_link_sequence(G, a.current_trip_number, node_dict).split(", ")
        
        a.x = node_dict[a.link_sequence[0]].x
        a.y = node_dict[a.link_sequence[0]].y
        
        a.agent_type = next_agent['agent_type']
        a.speed = a.get_agent_walking_speed(self.age_speed_dict[a.agent_type[0]])
        a.width_sensitivity = a.set_width_sensitivity_parameter(a.agent_type)
        a.attractor_sensitivity = a.set_attractor_sensitivity_parameter(a.agent_type)
        
        # カウントを進める
        self.agent_count += 1
        
        # ログ
        time = Universe.time_manager.show_time()
        l = f'{time} create_agent ID: {a.agent_id} link_sequence: {a.link_sequence}'

    def set_walk_speed_dict(self, walk_speed_file_path):
        
        # 歩行速度を定義する
        
        import csv
        with open(walk_speed_file_path, mode="r", encoding="utf-8-sig") as f:
            columns = ["age", "speed_ms"]
            walk_speed_data = csv.DictReader(f)

            for row in walk_speed_data:
                age = row[columns[0]]
                speed = row[columns[1]]

                self.age_speed_dict[str(age)] = float(speed)