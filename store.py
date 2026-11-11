import time
class Store:
    def __init__(self):
        self.data={}
        self.expires={}
        self.log_path='data/appendonly.log'

        try:
            with open(self.log_path, 'r',encoding='utf-8') as f:
                for line in f:
                    parts=line.strip().split()
                    if not parts:
                        continue
                    if parts[0]=='SET':
                        self.data[parts[1]]=parts[2]
                    elif parts[0]=='DEL':
                        self.data.pop(parts[1],None)
                    elif parts[0]=='EXPIRE':
                        key=parts[1]
                        seconds=int(parts[2])
                        if key in self.data:
                            self.expires[key]=time.time()+seconds
        except FileNotFoundError:
            pass

    def set(self,key,value):
        self.data[key]=value
        self.expires.pop(key,None)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(f'SET {key} {value}\n')

    def get(self,key):
        if key in self.expires:
            if time.time()>self.expires[key]:
                self.data.pop(key,None)
                self.expires.pop(key,None)
                return None
        return self.data.get(key)

    def delete(self,key):
        self.data.pop(key,None)
        self.expires.pop(key,None)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(f'DEL {key}\n')

    def expire(self,key,seconds):
        if key in self.data:
            self.expires[key]=time.time()+seconds
            with open(self.log_path,'a',encoding='utf-8') as f:
                f.write(f'EXPIRE {key} {seconds}\n')
            return True
        return False

