def agt_init(self):
    
    # エージェント生成時の動作

    # 通行リンク数（初期化）
    self.link_seq_count = 1
    # 現在のリンク（初期化）
    self.current_edge = None
    # 歩行距離（初期化）
    self.walking_distance = 0
    # エージェント移動速度（初期化）
    self.speed = 0
    # 存在するステップ数のカウント（初期化）
    self.step_count = 0

    # エージェント種別（初期化）
    # 年齢、性別、職業、目的、消費額、幅員感度、アトラクタ感度、歩行モデル（通常OD、昼食、回遊
    self.agent_type = None
    
    # 幅員感度パラメータ（初期化）
    self.width_sensitivity = 0
    # アトラクタ感度パラメータ（初期化）
    self.attractor_sensitivity = 0
    # アトラクタ感度の度合いを示す（広告による変化）
    self.attractor_degree = 0
    
    # イベント立ち寄り率（2.3%で固定）
    self.drop_rate = 0.023
    
    # エージェントの色を表示するための情報
    self.change_history_color_dict = {True: COLOR_RED, False: COLOR_BLUE}
    # アトラクタ感度の変更履歴（変更したらTrue）
    self.attractor_change_history = False
    self.attractor_color = COLOR_BLUE
    # イベント立ち寄り履歴（立ち寄ったらTrue）
    self.event_drop_history = False
    self.event_color = COLOR_BLUE
    # イベント立ち寄り箇所のリスト
    self.event_drop_list = list()
    # エージェントが存在中にイベントに立ち寄ったか（立ち寄っていたらTrue）
    self.event_all = False
    self.event_all_color = COLOR_BLUE
    
    # トリップ数の表示
    self.current_trip_number = 1

    self.trip = {1: {"origin": None, "destination": None, "waiting_time": int},
                 2: {"origin": None, "destination": None, "waiting_time": int},
                 3: {"origin": None, "destination": None, "waiting_time": int}}

    # 歩行か停止かのモード設定
    self.move_mode = "FORWARD"
    self.move_mode_color_dict = {"FORWARD": COLOR_BLUE, "STOP": COLOR_RED}
    self.move_mode_color = self.move_mode_color_dict[self.move_mode]

    # 停止時間をカウントするためのカウンタ
    self.stop_counter = 0
    self.current_stop_time = 0

def agt_step(self):
    
    # 各ステップのエージェントの挙動

    # 歩行モードの時の処理
    if self.move_mode == "FORWARD":
        try:
            target = Universe.node_dict[self.link_sequence[self.link_seq_count]]
            prev_target = Universe.node_dict[self.link_sequence[self.link_seq_count - 1]]

            # 現在いるリンクID
            self.current_edge = Universe.network.edges[prev_target, target]['link_id']
            
            if "NI" in target.node_id:  # イベントノードに向かっているとき
                self.event_drop_history = True
                self.event_all = True
    
            # ターゲットに向かって進み、到着したらターゲットを更新
            forward_grid_distance = Universe.second_per_step * self.speed / Universe.meter_per_grid  # 1ステップで進む距離（マス）
            
            if self.pursue(target, forward_grid_distance) != -1:
                self.link_seq_count += 1
                self.event_drop_history = False
    
                # ノードに広告があればリンク再計算
                if self.attractor_change_history is True and self.event_drop_history is True:
                    self.usual_status_update(target, forward_grid_distance)
        
                elif self.attractor_change_history is True and self.event_drop_history is False:
                    self.update_event_drop_status(target, Universe.drop_rate, forward_grid_distance)
        
                elif self.attractor_change_history is False and self.event_drop_history is True:
                    if target.signage_point == 1:
                        self.update_attractor_parameter_status(prev_target)
                    else:

                        self.usual_status_update(target, forward_grid_distance)
        
                else:
                    if target.signage_point == 1:
                        self.update_attractor_parameter_status(prev_target)
                        self.update_event_drop_status(target, Universe.drop_rate, forward_grid_distance)
        
                    else:
                        # 立ち寄り更新フロー
                        self.update_event_drop_status(target, Universe.drop_rate, forward_grid_distance)
        except IndexError:
                del_agt(self)

        # 歩行距離を積算
        self.walking_distance += Universe.second_per_step * self.speed  # 1ステップで進んだ距離（m）

    # 停止モードの時の処理
    elif self.move_mode == "STOP":
        if self.current_stop_time <= self.stop_counter:
            # リセット
            self.move_mode = "FORWARD"
            self.current_stop_time = 0
            self.stop_counter = 0

        else:
            self.stop_counter += 1

    # 色の変更
    self.attractor_color = self.change_history_color_dict[self.attractor_change_history]
    self.event_color = self.change_history_color_dict[self.event_drop_history]
    self.move_mode_color = self.move_mode_color_dict[self.move_mode]

    # 自分が生まれて何秒目かをカウントする
    self.step_count += 1

    # ログにデータを追加
    Universe.output_log.add_agent_log(self)
    
def usual_status_update(self, target, forward_grid_distance):
    
    # ステータス更新
    import random

    if self.link_seq_count == len(self.link_sequence):  # 到着処理
        if self.current_trip_number != 3:  # 1,2番目のトリップの場合
            self.current_trip_number += 1

            # ODをチェックする
            # もしOがNoneなら、エージェント消去
            if self.trip[self.current_trip_number]["destination"] == "None":
                del_agt(self)
            else:
                self.link_sequence = self.set_link_sequence(Universe.network, self.current_trip_number,
                                                            Universe.node_dict).split(", ")

                # リンクシーケンスカウントのリセット
                self.link_seq_count = 1
                # 停止モードに変更
                self.move_mode = "STOP"
                # 停止時間の設定
                self.current_stop_time = int(
                    self.trip[self.current_trip_number - 1]["waiting_time"]) * 60 / Universe.second_per_step

        else:
            del_agt(self)

    elif str(target.self_attractor) == "1":
            self.move_mode = "STOP"
            self.current_stop_time = random.randint(int(target.lower_staytime), int(target.upper_staytime) + 1)  # 一様分布で滞在時間を設定する

def update_attractor_parameter_status(self, origin_object):
    
    # アトラクタパラメータを更新する

    self.attractor_sensitivity = self.change_attractor_parameter()

    # リンクシーケンスの更新
    self.link_sequence = self.edit_link_sequence(
        Universe.network,
        self.current_trip_number,
        Universe.node_dict,
        origin_object
    ).split(", ")
    self.link_seq_count = self.link_sequence.index('{}'.format(origin_object.node_id)) + 1

def update_event_drop_status(self, target, drop_rate, forward_grid_distance):
    
    # イベント立ち寄りによるパラメータ更新
    
    drop_rate = self.drop_rate

    if target.attractor_event_node_id != "":
        target_index = self.link_sequence.index(target.node_id)

        if target.attractor_to_id == self.link_sequence[target_index + 1]:
            attractor_id = target.attractor_event_node_id
            to_id = target.attractor_to_id

            if self.link_seq_count + 2 != len(self.link_sequence):

                if attractor_id not in self.event_drop_list:

                    # 昼間なら時間制約がつく
                    if self.agent_type[7] == 2:  # 昼食限定
                        step_limit = 60 * 60 / Universe.second_per_step  # お昼休みは60分

                        next_waiting_step = self.trip[self.current_trip_number][
                                                "waiting_time"] * 60 / Universe.second_per_step

                        if self.step_count + next_waiting_step + 15 * 60 * 60 / Universe.second_per_step < step_limit:
                             # 15分の余裕をもって立ち寄るかを決める
                            self.event_drop_history = True

                            if self.drop_rate * target.attractor_point / 100 > random.random():
                                
                                # イベント立ち寄り
                                
                                to_id_index = self.link_sequence.index(to_id)
                                attractor_string = str(attractor_id)
                                self.link_sequence.insert(to_id_index, attractor_string)
                                self.event_drop_list.append(attractor_id)
                                self.event_all = True
                                self.event_all_color = self.change_history_color_dict[self.event_all]
                            else:
                                self.usual_status_update(target, forward_grid_distance)
                        else:
                            self.usual_status_update(target, forward_grid_distance)
                    else:
                        
                        # イベント立ち寄り
                        
                        self.event_drop_history = True
                        if self.drop_rate * target.attractor_point / 100> random.random():
                            to_id_index = self.link_sequence.index(to_id)
                            attractor_string = str(attractor_id)
                            self.link_sequence.insert(to_id_index, attractor_string)
                            self.event_drop_list.append(attractor_id)
                            self.event_all = True
                            self.event_all_color = self.change_history_color_dict[self.event_all]
                            
                        else:
                            self.usual_status_update(target, forward_grid_distance)
                else:
                    self.usual_status_update(target, forward_grid_distance)
            else:
                self.usual_status_update(target, forward_grid_distance)
        else:
            self.usual_status_update(target, forward_grid_distance)
    else:
        self.usual_status_update(target, forward_grid_distance)

def get_agent_walking_speed(self, walking_speed: float):

    # 移動速度を取得する

    return walking_speed


def set_width_sensitivity_parameter(self, agent_type: str):

    # 幅員感度パラメータを設定する

    import random
    width_rep_parameter_dict = {0: 0.2, 1: 0.4, 2: 0.6, 3: 0.8}
    sd = 0.2
    width_average = width_rep_parameter_dict[int(agent_type[5])]

    width = width_average

    return width


def set_attractor_sensitivity_parameter(self, agent_type: str):

    # アトラクタ感度パラメータを設定する

    import random
    attractor_rep_parameter_dict = {0: 0.25, 1: 0.5, 2: 0.75}
    sd = 0.25
    self.attractor_degree = int(agent_type[6])
    attractor_average = attractor_rep_parameter_dict[int(agent_type[6])]

    attractor = attractor_average

    return attractor

def set_agent_trip(self, o1, d1, wt1, d2, wt2):

    # エージェントのトリップを設定

    self.trip = {1: {"origin": o1, "destination": d1, "waiting_time": wt1},
                 2: {"origin": d1, "destination": d2, "waiting_time": wt2},
                 3: {"origin": d2, "destination": o1, "waiting_time": 0}}

    return self.trip

def set_speed(self, speed: float):

    # エージェントの速度を設定

    # 1秒あたりの移動速度(m/s)を設定する
    speed_ms = speed

    time_manager = Universe.time_manager

    # 1ステップあたりに進むグリッド数を計算
    self.speed_sim = self.speed_ms * time_manager.second_per_step / Universe.meter_per_grid

    # 時速を計算
    self.speed_real_kmh = speed_ms * 3.6

def change_attractor_parameter(self):

    # アトラクタ感度パラメータを変更する

    import random

    attractor_rep_parameter_dict = {0: 0.25, 1: 0.5, 2: 0.75}
    sd = 0.25

    self.attractor_change_history = True

    if self.attractor_degree != 2:
        change_rate = 0.5
        if change_rate > random.random():
            self.attractor_degree += 1
            random_val = random.gauss(0, sd) / 3

            attractor = attractor_rep_parameter_dict[self.attractor_degree] + random_val

            return attractor
        else:
            return self.attractor_sensitivity

    else:
        return self.attractor_sensitivity

def set_link_sequence(self, G, trip_number: int, node_dict: dict):

    # リンクシーケンスを設定する
    
    import networkx as nx
    my_graph = G.copy()

    # 各エッジの自分にとっての距離を計算する
    for edge in my_graph.edges(data=True):
        # 階段があれば（link_idに"LUF"か"LFS"が入っていれば）距離の係数をかける
        if "LUF" in str(edge[2]['link_id']):
            link_coefficient = 12.0
        elif "LFS" in str(edge[2]['link_id']):
            link_coefficient = 12.0
        else:
            link_coefficient = 1.0
            
        # 横断歩道負荷の設定
        if int(edge[2]['path_code']) == int(0):
            cross_coefficient = 1.0
        elif int(edge[2]['path_code']) == int(10):
            cross_coefficient = 4.0
        elif int(edge[2]['path_code']) == int(11):
            cross_coefficient = 12.0
        elif int(edge[2]['path_code']) == int(20):
            cross_coefficient = 4.0
            link_coefficient = 12.0
        elif int(edge[2]['path_code']) == int(30):
            cross_coefficient = 1.0
            link_coefficient = 1.0
        else:
            cross_coefficient = 1.0
        
        # 幅員の係数
        width_coefficient = 1.0
        
        my_distance = edge[2]['weight'] * link_coefficient * cross_coefficient * \
            (1 * width_coefficient / (edge[2]['visible_area'] ** self.width_sensitivity)) * \
                (1 / (edge[1].attractor_point ** self.attractor_sensitivity))
        edge[2]['my_distance'] = my_distance

    origin = node_dict[str(self.trip[trip_number]["origin"])]
    destination = node_dict[str(self.trip[trip_number]["destination"])]

    # ダイクストラ法による計算
    link_sequence = nx.dijkstra_path(
        my_graph, origin, destination, weight='my_distance'
    )

    return ', '.join(map(str, link_sequence))

def edit_link_sequence(self, G, trip_number: int, node_dict: dict, origin_object):
    
    # リンクシーケンスを編集する
    
    import networkx as nx
    my_graph = G.copy()

    # 各エッジの自分にとっての距離を計算する
    for edge in my_graph.edges(data=True):
        # 階段があれば（link_idに"LUF"か"LFS"が入っていれば）距離の係数をかける
        if "LUF" in str(edge[2]['link_id']):
            link_coefficient = 12.0
        elif "LFS" in str(edge[2]['link_id']):
            link_coefficient = 12.0
        else:
            link_coefficient = 1.0
            
        # 横断歩道負荷の設定
        if int(edge[2]['path_code']) == int(0):
            cross_coefficient = 1.0
        elif int(edge[2]['path_code']) == int(10):
            cross_coefficient = 4.0
        elif int(edge[2]['path_code']) == int(11):
            cross_coefficient = 12.0
        elif int(edge[2]['path_code']) == int(20):
            cross_coefficient = 4.0
            link_coefficient = 12.0
        elif int(edge[2]['path_code']) == int(30):
            cross_coefficient = 1.0
            link_coefficient = 1.0
        else:
            cross_coefficient = 1.0
        
        # 幅員の係数
        width_coefficient = 1
        
        my_distance = edge[2]['weight'] * link_coefficient * cross_coefficient * \
            (1 * width_coefficient / (edge[2]['visible_area'] ** self.width_sensitivity)) * \
                (1 / (edge[1].attractor_point ** self.attractor_sensitivity))
        edge[2]['my_distance'] = my_distance

    origin = origin_object

    destination = node_dict[str(self.trip[trip_number]["destination"])]

    # ダイクストラ法による計算
    link_sequence = nx.dijkstra_path(
        my_graph, origin, destination, weight='my_distance'
    )

    return ', '.join(map(str, link_sequence))
