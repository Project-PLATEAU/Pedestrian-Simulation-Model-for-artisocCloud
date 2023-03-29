class TimeManager:
    
    # 時刻管理をするマネージャ
    
    def __init__(self):
        
        # 1ステップあたりの秒を定義
        self.second_per_step = Universe.second_per_step
        
        # シミュレーション開始時の秒（0時から数えて）
        self.total_second = 60 * 60 * Universe.start_hour
    
    def time_step(self):
        # 1ステップ進める
        self.total_second += self.second_per_step

    def get_time(self):
        # 現在の時刻を[h, m, s]のリストで返す
        return self.convert_total_second_to_time(self.total_second)
    
    def get_sec(self):
        # 現在の時刻の秒を返す
        return self.get_time()[2]
    
    def get_min(self):
        # 現在の時刻の分を返す
        return self.get_time()[1]
    
    def get_hour(self):
        # 現在の時刻の時間を返す
        return self.get_time()[0]
    
    def show_time(self):
        # ステップからh:m:s形式の時刻を返す
        t = self.get_time()
        
        return self.convert_time_to_string(t)

    def get_time_from_string(self, s_time):
        # "h:m:s"形式の文字列から時刻を[h, m, s]のリストで返す
        
        s_list = s_time.split(":")
        h = int(s_list[0])
        m = int(s_list[1])
        s = int(s_list[2])
        
        return [h, m, s]

    def get_time_difference(self, t1, t2):
        # [h, m, s]で渡された時刻の差を[h, m, s]で返す（ただしt1<t2）
        
        t1_total_s = 3600 * t1[0] + 60 * t1[1] + t1[2]
        t2_total_s = 3600 * t2[0] + 60 * t2[1] + t2[2]
        
        # 差の秒
        total_s_diff = t2_total_s - t1_total_s
        
        return self.convert_total_second_to_time(total_s_diff)

    def convert_total_second_to_time(self, total_s):
        # トータル秒で与えられた時間を[h, m, s]になおす
        
        s = total_s % 60  # 秒（60で割ったあまり）
        total_m = total_s // 60  # トータルの分（トータルの秒数を60で割った商）
        m = total_m % 60  # 分（トータルの分数を60で割ったあまり）
        h = total_m // 60  # 時（トータルの分数を60で割った商）
        
        return [h, m, s]
 
    def convert_time_to_string(self, t):
        # [h, m, s]から"h:mm:ss"に変換する 
        
        if t[1] < 10:
            t[1] = "0" + str(round(t[1]))
        if t[2] < 10:
            t[2] = "0" + str(round(t[2], 1))
        else:
            t[2] = round(t[2], 1)
            
        return str(round(t[0])) + ":" + str(t[1]) + ":" + str(t[2])

    def compare_time(self, t1, t2):
        # 時刻の比較
        
        # t1 > t2ならTrue
        if int(t1[0]) > int(t2[0]):
            return True
        elif int(t1[0]) < int(t2[0]):
            return False
        elif int(t1[1]) > int(t2[1]):
            return True
        elif int(t1[1]) < int(t2[1]):
            return False
        elif float(t1[2]) > float(t2[2]):
            return True
        else:
            # 同時刻ならFalseを返す
            return False