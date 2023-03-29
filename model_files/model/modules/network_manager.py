class NetworkManager:
    
    def __init__(self, node_data, link_data):
        
        self.nodes = {}
        self.links_height = {}
        self.read_nodes_and_links(node_data, link_data)
    
    def read_nodes_and_links(self, node_data, link_data):
        
        # ノードとリンクを読み込む
        
        import networkx as nx
        import csv
        
        # ノードの読み込み
        with open(node_data, mode="r", encoding="shift-jis") as f:
            reader = csv.DictReader(f)
            
            # データの格納
            for data in reader:
                node = create_agt(Universe.map.node)
                node.node_id = str(data['node_id'])
                node.x = float(data['x'])
                node.y = float(data['y'])
                node.signage_point = int(data['signage'])
                node.attractor_point_init = float(data['attractor'])  # 初期値
                node.attractor_point = float(data['attractor'])  # 変更のある場合に使用する
                node.attractor_event_node_id = str(data['attractor_node_id'])
                node.attractor_to_id = str(data['attractor_to_id'])
                node.self_attractor = data['self_attractor']
                node.lower_staytime = data['lower_staytime']
                node.upper_staytime = data['upper_staytime']
                node.from_time = data['from_time']
                node.to_time = data['to_time']
                self.nodes[node.node_id] = node
                
        # リンクの読み込み
        with open(link_data, mode="r", encoding="shift-jis") as f:
            reader = csv.DictReader(f)
            
            # データの格納
            for data in reader:
                link_id = str(data['link_id'])
                fromNID = str(data['from_node_id'])
                toNID = str(data['to_node_id'])
                from_node = self.nodes[fromNID]
                to_node = self.nodes[toNID]
                distance = measure_agt_distance(from_node, to_node)
                visible_area = float(data['visible_area'])
                path_code = int(data['path'])
                z = float(data['z'])
                Universe.network.add_edge(
                    from_node, to_node, weight=distance, visible_area=visible_area, link_id=link_id, path_code=path_code, z=z
                )
                self.links_height[link_id] = z
    
    def update_node_attractor(self, hour: int):
        
        # ノードのアトラクタ情報を更新する
        
        for node_id, node_object in self.nodes.items():
            if int(node_object.from_time) <= int(hour) <= int(node_object.to_time):
                node_object.attractor_point = node_object.attractor_point_init
            else:
                # print("ノードアトラクタ調整極小")
                node_object.attractor_point = 0.00001  # 極小にして通行しにくくする
    
    def update_signage_value_to_None(self):
        
        # 広告が存在しないときはsignageの値を0にする
        
        for node_id, node_object in self.nodes.items():
            node_object.signage_point = 0
           