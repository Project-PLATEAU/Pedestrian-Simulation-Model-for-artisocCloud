from time_manager import TimeManager


class OutputLog(object):
    
    # ログ出力を管理するオブジェクト
    
    def __init__(self):
        
        self.columns = [
            'agent_id',
            "step",
            "time",
            "agent_type",
            "x",
            "y",
            "z", 
            "current_link",
            "walking_distance",
            "mode"
        ]
        self._data = list()

    def add_agent_log(self, agent):
        
        # エージェントログを追記する
        
        s = Universe.time_manager.get_sec()
        
        if int(s) % 10 == 0:  # 10秒おきにログを吐き出す
            try: 
                data = {
                'agent_id': agent.agent_id,
                "step": count_step(),
                "time": Universe.time_manager.show_time(),
                "agent_type": agent.agent_type,
                "x": agent.x,
                "y": agent.y,
                "z": Universe.network_manager.links_height[agent.current_edge],
                "current_link": agent.current_edge,
                "walking_distance": agent.walking_distance,
                "mode": agent.move_mode
                }
            
                self._data.append(data)
            except KeyError:
                pass
        else:
            pass
       
    def output_agent_log_file(self, file_title):
        
        # ログファイルを出力する
        
        import csv

        print(f'output {file_title}')
        with open(file_title, "w", encoding="shift-jis") as f:
            writer = csv.DictWriter(f, self.columns)
            writer.writeheader()
            for data in self._data:
                writer.writerow(data)
        self._data = list()