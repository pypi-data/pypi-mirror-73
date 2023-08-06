import redis
import jgconfig.config


class RedisPoolTools:
    selfpool = redis.ConnectionPool(host= jgconfig.config.ConfigJson['redishost'], port=jgconfig.config.ConfigJson['redisport'],password=int(jgconfig.config.ConfigJson['redispass']), decode_responses=True)
    
    def __init__(self):
        self.rd = redis.Redis(connection_pool=RedisPoolTools.selfpool)

    def StringSet(self,key,val,ex=None):
        self.rd.set(key, val,ex=ex)
    
    def StringGet(self,key):
        return self.rd.get(key)

    def HasSet(self,haskey,key,val,ex=None):
        self.rd.hset(haskey,key,val,ex)

    def HasGet(self,haskey,key):
        return self.rd.hget(haskey,key)

    # def timeout(self):
    #     self.rd.t

    def HasAll(self,name):
        return self.rd.hgetall(name)